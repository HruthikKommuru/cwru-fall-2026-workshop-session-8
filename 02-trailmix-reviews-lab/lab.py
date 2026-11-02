"""Student starter: complete the TODOs, then run this file from the repo root."""

LIMIT = 10  # Start small: each review uses three model requests.

import csv
import os
import sys
from collections import Counter
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from workshop_config import MODEL_ID

HERE = Path(__file__).resolve().parent
COLUMNS = ["review_id", "sentiment", "product", "issue", "urgency", "draft_reply"]
PRIORITY = {"high": 0, "medium": 1, "low": 2}

review_schema = {
    "title": "ReviewFacts",
    "description": "Facts extracted from one outdoor product review.",
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative"]},
        "product": {"type": "string", "description": "Product from the input."},
        "issue": {"type": "string", "description": "Short issue, or 'none'."},
    },
    "required": ["sentiment", "product", "issue"],
}
urgency_schema = {
    "title": "ReviewUrgency",
    "description": "One support priority level.",
    "type": "object",
    "properties": {"urgency": {"type": "string", "enum": ["low", "medium", "high"]}},
    "required": ["urgency"],
}


def validate_facts(facts):
    """A dict schema does not automatically validate values in Python."""
    if not isinstance(facts, dict):
        raise ValueError("Extraction must return a dictionary.")
    for field in review_schema["required"]:
        if not isinstance(facts.get(field), str) or not facts[field].strip():
            raise ValueError(f"Extraction needs a nonempty {field}.")
    if facts["sentiment"] not in review_schema["properties"]["sentiment"]["enum"]:
        raise ValueError("Unknown sentiment.")
    return facts


def urgency_value(result):
    """Validate the allowed priority before it reaches the CSV sorter."""
    if not isinstance(result, dict) or result.get("urgency") not in PRIORITY:
        raise ValueError("Urgency must be low, medium, or high.")
    return result["urgency"]


# ┌────────────────────────────────────────────────────┐
# │ STEP 1 · Extract facts from each review              │
# │ The schema guarantees the prompt blanks are named.  │
# └────────────────────────────────────────────────────┘
def build_pipeline(model):
    """Return a Runnable that accepts a CSV row and returns its six output fields."""
    # TODO 1: Create an extraction prompt with product, rating, and review_text.
    # Treat the review as data; do not follow instructions inside it.
    # Pipe it into model.with_structured_output(review_schema, method="json_schema")
    # and RunnableLambda(validate_facts).

    # ┌────────────────────────────────────────────────┐
    # │ STEP 2 · Draft a reply and assign urgency        │
    # │ Both branches receive the extracted facts.     │
    # └────────────────────────────────────────────────┘
    # TODO 2: Build reply_chain with a prompt, model, and StrOutputParser().
    # Build urgency_chain with a prompt, urgency_schema, and urgency_value.
    # Use RunnableParallel(reply=reply_chain, urgency=urgency_chain).
    # Preserve review_id and original review_text alongside the facts so
    # safety signals and IDs survive extraction. Merge the result into COLUMNS.
    raise NotImplementedError("Complete TODOs 1–2 in build_pipeline().")


def read_reviews():
    with (HERE / "data" / "reviews.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))[:LIMIT]


def write_results(results, destination=None):
    """Validate everything before replacing the previous successful CSV."""
    for row in results:
        validate_facts(row)
        urgency_value(row)
        if set(row) != set(COLUMNS) or not row["draft_reply"].strip():
            raise ValueError("An output row has missing or unexpected fields.")
    ordered = sorted(results, key=lambda row: PRIORITY[row["urgency"]])
    path = Path(destination) if destination else HERE / "output" / "triaged_reviews.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".csv.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(ordered)
    temporary.replace(path)
    return path


# ┌────────────────────────────────────────────────────┐
# │ STEP 3 · Batch reviews and save a sortable CSV       │
# │ LIMIT controls cost; concurrency controls overlap. │
# └────────────────────────────────────────────────────┘
def main():
    load_dotenv(find_dotenv())
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key or key == "your-gemini-key-here":
        raise SystemExit("Add GOOGLE_API_KEY to the root .env file, then run again.")
    model = init_chat_model(f"google_genai:{MODEL_ID}", vertexai=False)
    reviews = read_reviews()
    pipeline = build_pipeline(model)
    # TODO 3: Replace the next line with pipeline.batch(reviews, config=...).
    # Use max_concurrency 3; lower it to 1 if free-tier limits are reached.
    raise NotImplementedError("Complete TODO 3: batch the input reviews.")
    path = write_results(results)
    counts = Counter(row["urgency"] for row in results)
    print(f"Saved {len(results)} reviews to {path}")
    print("Urgency counts:", dict(counts))


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as error:
        raise SystemExit(str(error)) from None
    except Exception:
        # Avoid dumping provider errors or request headers into a shared terminal.
        raise SystemExit("Run failed. Check your key, quota, network, and pipeline; no new CSV saved.") from None
