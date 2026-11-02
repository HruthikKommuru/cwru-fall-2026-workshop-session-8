# CWRU Fall 2026 Workshop — Session 8

Learn LangChain essentials with the Gemini API. Start with a guided notebook,
then build a review-triage pipeline for the fictional TrailMix Outdoors store.
All 50 reviews are invented. Use Python 3.11.5+; Python 3.13 is the tested version.
The latest IPython/ipykernel no longer support Python 3.10, and the pinned
Beautiful Soup dependency requires at least Python 3.11.5.

## Setup: macOS / Linux

Run these commands in a terminal:

```sh
git clone https://github.com/HruthikKommuru/cwru-fall-2026-workshop-session-8.git
cd cwru-fall-2026-workshop-session-8
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cp .env.example .env
python -m ipykernel install --user --name session8 --display-name "Session 8 (LangChain)"
```

## Setup: Windows PowerShell

```powershell
git clone https://github.com/HruthikKommuru/cwru-fall-2026-workshop-session-8.git
cd cwru-fall-2026-workshop-session-8
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m ipykernel install --user --name session8 --display-name "Session 8 (LangChain)"
```

If PowerShell blocks activation, use Command Prompt and `.venv\Scripts\activate.bat`,
or invoke `.venv\Scripts\python.exe` directly in place of `python`.

## Add your key and run

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com).
Open the local `.env` file in your editor and replace the placeholder after
`GOOGLE_API_KEY=` with your key. Never paste it into a notebook, screenshot, or Git commit.

```sh
python -m jupyter notebook 01-langchain-basics/langchain_basics.ipynb
```

Select **Session 8 (LangChain)**, then run cells from top to bottom using Shift+Enter.
The notebook makes multiple API calls. Free-tier access and limits vary by model
and account; check AI Studio before class. A 429 response means a quota or rate
limit was reached: pause, reduce concurrency, and retry the affected cell later.
LangChain `batch()` sends separate requests; it is not Google's discounted Batch API.

Next read [the TrailMix lab](02-trailmix-reviews-lab/README.md), fill in its TODOs,
and run from this repository root:

```sh
python 02-trailmix-reviews-lab/lab.py
```

`main` intentionally contains incomplete student code. The instructor's completed
lab is on the `solution` branch at the same path. Commit or stash your own work
before switching with `git switch solution` (after cloning, use
`git switch --track origin/solution` the first time). Then run the same command.
Drafts require a human review before use; the script does not send replies.

## How the code fits together

- A **prompt** fills blanks in instructions.
- A **model** sends those instructions to Gemini and returns an `AIMessage`.
- A **parser** converts the reply into a string, list, or dictionary.
- A **Runnable** is a step with methods such as `invoke`, `batch`, and `stream`.
- The pipe `|` passes one step's result into the next step.

`workshop_config.py` is the single place to change `MODEL_ID`. No temperature is
set, following the Gemini 3 defaults. `LIMIT = 10` in `lab.py` keeps the first run
small (three model requests per review). Raise it to 50 when ready.

## Documentation decisions

Official docs were checked on November 1, 2026:

- [Models](https://docs.langchain.com/oss/python/langchain/models)
- [Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [Messages](https://docs.langchain.com/oss/python/langchain/messages)
- [Google integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai)
- [Gemini model list](https://ai.google.dev/gemini-api/docs/models)

Google lists the selected stable Flash model as fast and cost efficient. Flash-Lite
is a cheaper separate option; this workshop uses the current full Flash model.
The structured-output overview focuses on agents; this workshop follows the
standalone model examples linked from it. Google's integration recommends
`method="json_schema"`, which is explicit in our code. Plain dictionaries do not
provide Python-side validation automatically, so the lab includes small checks.
Examples use `.text` to read message text. No deprecated chain APIs are needed.

## Verification and secrets

Run `python scripts/offline_smoke.py` without an API key. It executes notebook
cells with LangChain's `GenericFakeChatModel`; on `solution` it also checks the
actual lab pipeline, batching, schema validation, CSV writing, and priority order.
Fake replies verify wiring, not Gemini quality or server-side schema enforcement.
See `VERIFICATION.md` for the recorded results and remaining live checks.

Before **every** push, both checks below must succeed (the second prints nothing):

```sh
git check-ignore -v .env
git ls-files | grep -E '(^|/)\.env$'
```

The second command normally exits with status 1 because there are no matches.
Stop and fix the ignore rules if the first command fails or the second prints a path.
Generated CSVs and executed notebooks belong in ignored `output/` folders.
