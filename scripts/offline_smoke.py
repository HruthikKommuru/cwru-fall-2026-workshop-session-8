"""Run with python scripts/offline_smoke.py. No network or real key is used."""

import contextlib
import csv
import importlib.util
import io
import itertools
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import nbformat
from langchain.chat_models import init_chat_model
from langchain_core.language_models import GenericFakeChatModel
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workshop_config import MODEL_ID

FACTS = {"sentiment": "positive", "product": "hiking socks", "issue": "none"}


def fake_structured(self, schema, *, method="json_schema", include_raw=False, **kwargs):
    """GenericFakeChatModel lacks native schemas; emulate that boundary only."""
    assert method == "json_schema"
    assert set(schema["required"]) <= set(schema["properties"])

    def respond(value):
        text = value.to_string() if hasattr(value, "to_string") else str(value)
        text = text.lower()
        if "urgency" in schema["properties"]:
            level = "high" if "valve" in text else "medium" if "zipper" in text else "low"
            result = {"urgency": level}
        elif "valve" in text:
            result = {"sentiment": "negative", "product": "Camping stove", "issue": "valve leaks fuel"}
        elif "zipper" in text:
            result = {"sentiment": "negative", "product": "Tent", "issue": "zipper jams"}
        else:
            result = FACTS.copy()
        # Exercise a real LangChain chat model and parser without contacting Gemini.
        raw = GenericFakeChatModel(messages=iter([json.dumps(result)])).invoke(value)
        parsed = JsonOutputParser().invoke(raw)
        return {"raw": raw, "parsed": parsed, "parsing_error": None} if include_raw else parsed

    return RunnableLambda(respond)


def check_notebook():
    path = ROOT / "01-langchain-basics" / "langchain_basics.ipynb"
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    fake = GenericFakeChatModel(messages=itertools.repeat(json.dumps(FACTS)))
    scope = {"__name__": "__offline_notebook__"}
    captured = io.StringIO()
    with contextlib.chdir(ROOT), contextlib.redirect_stdout(captured), \
            patch.dict(os.environ, {"GOOGLE_API_KEY": "offline-placeholder", "LANGSMITH_TRACING": "false"}), \
            patch("langchain.chat_models.init_chat_model", return_value=fake), \
            patch.object(GenericFakeChatModel, "with_structured_output", fake_structured):
        count = 0
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type != "code":
                continue
            assert len(cell.source.splitlines()) <= 15
            assert not cell.outputs and cell.execution_count is None
            preceding = notebook.cells[index - 1]
            assert preceding.cell_type == "markdown"
            for label in ["**Concept**", "**What this cell does**", "**What to look for**"]:
                assert label in preceding.source
            exec(compile(cell.source, f"notebook-cell-{index}", "exec"), scope)
            count += 1
    assert isinstance(scope["answers"], list) and len(scope["answers"]) == 2
    assert scope["diagnostic"]["parsing_error"] is None
    assert all(isinstance(item, str) for item in scope["list_chain"].invoke({}))
    print(f"PASS: all {count} notebook code cells execute offline; outputs remain cleared.")


def load_lab():
    path = ROOT / "02-trailmix-reviews-lab" / "lab.py"
    spec = importlib.util.spec_from_file_location("trailmix_lab", path)
    lab = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lab)
    return lab


def check_provider_adapter(provider):
    """Keep the real provider's schema/parser wiring; replace only generation."""
    lab = load_lab()

    def generate(self, messages, **kwargs):
        return GenericFakeChatModel(messages=iter([json.dumps(FACTS)]))._generate(messages)

    with patch.object(type(provider), "_generate", generate):
        structured = provider.with_structured_output(lab.review_schema, method="json_schema")
        assert structured.invoke("Warm socks") == FACTS
        diagnostic = provider.with_structured_output(
            lab.review_schema, method="json_schema", include_raw=True
        ).invoke("Warm socks")
        assert diagnostic["parsed"] == FACTS and diagnostic["parsing_error"] is None

    def malformed(self, messages, **kwargs):
        return GenericFakeChatModel(messages=iter(["not JSON"]))._generate(messages)

    with patch.object(type(provider), "_generate", malformed):
        failed = provider.with_structured_output(
            lab.review_schema, method="json_schema", include_raw=True
        ).invoke("Malformed reply test")
        assert failed["parsed"] is None and failed["parsing_error"] is not None
    print("PASS: real Google adapter schema and include_raw success/failure parser paths, with fake generation.")


def check_lab():
    lab = load_lab()
    with (lab.HERE / "data" / "reviews.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 50 and len({r["review_id"] for r in rows}) == 50
    assert {int(r["rating"]) for r in rows} == {1, 2, 3, 4, 5}
    assert len(lab.read_reviews()) == lab.LIMIT == 10
    for bad in [{}, {"sentiment": "happy", "product": "boots", "issue": "none"},
                {"sentiment": "positive", "product": "boots", "issue": ""}]:
        try:
            lab.validate_facts(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid extraction was accepted.")
    try:
        lab.urgency_value({"urgency": "critical"})
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid urgency was accepted.")
    print("PASS: 50 unique reviews, all ratings, LIMIT=10, and schema guards.")

    fake = GenericFakeChatModel(messages=itertools.repeat("Thank you; please contact support."))
    with patch.object(GenericFakeChatModel, "with_structured_output", fake_structured):
        try:
            pipeline = lab.build_pipeline(fake)
        except NotImplementedError:
            print("PASS: main is an intentional TODO starter; full pipeline smoke runs on solution.")
            return
        inputs = [
            {"review_id": "T1", "product": "hiking socks", "rating": "5", "review_text": "Warm socks."},
            {"review_id": "T2", "product": "Tent", "rating": "2", "review_text": "The zipper jams."},
            {"review_id": "T3", "product": "Camping stove", "rating": "1", "review_text": "The valve leaks fuel."},
            {"review_id": "T4", "product": "hiking socks", "rating": "5", "review_text": "Warm socks again."},
        ]
        results = pipeline.batch(inputs, config={"max_concurrency": 3})
        assert [r["review_id"] for r in results] == ["T1", "T2", "T3", "T4"]
        assert [r["urgency"] for r in results] == ["low", "medium", "high", "low"]
        assert results[2]["product"] == "Camping stove" and results[2]["issue"] == "valve leaks fuel"
        assert all(r["draft_reply"] for r in results)
        with tempfile.TemporaryDirectory() as temporary:
            path = lab.write_results(results, Path(temporary) / "triaged_reviews.csv")
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                assert reader.fieldnames == lab.COLUMNS
                saved = list(reader)
            assert [r["review_id"] for r in saved] == ["T3", "T2", "T1", "T4"]
            original = path.read_bytes()
            try:
                lab.write_results([{**results[0], "urgency": "critical"}], path)
            except ValueError:
                pass
            else:
                raise AssertionError("Invalid output was accepted.")
            assert path.read_bytes() == original
            # Exercise the script's actual main path with five supplied rows.
            real_write = lab.write_results
            with patch.dict(os.environ, {"GOOGLE_API_KEY": "offline-placeholder"}), \
                    patch.object(lab, "LIMIT", 5), \
                    patch.object(lab, "init_chat_model", return_value=fake), \
                    patch.object(lab, "write_results", side_effect=lambda data:
                                 real_write(data, Path(temporary) / "main.csv")), \
                    contextlib.redirect_stdout(io.StringIO()):
                lab.main()
            with (Path(temporary) / "main.csv").open(newline="", encoding="utf-8") as handle:
                assert len(list(csv.DictReader(handle))) == 5
    print("PASS: solution extraction → parallel → batch; IDs, stable urgency sort, CSV, and LIMIT=5 main run.")


if __name__ == "__main__":
    # Instantiate the real provider adapter, but make no network request.
    provider = init_chat_model(f"google_genai:{MODEL_ID}", api_key="offline-placeholder", vertexai=False)
    check_provider_adapter(provider)
    check_notebook()
    check_lab()
    print("Offline verification complete. Gemini behavior and live quota still need a real-key run.")
