# Session 8: LangChain essentials

Learn one idea at a time with Gemini, then use the same ideas to triage
**10 fictional TrailMix reviews**. Use Python 3.11.5 or newer (tested with 3.13).

## 1. Set up once

Download or clone this repository, then open a terminal in its folder.

**macOS / Linux**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m ipykernel install --user --name session8 --display-name "Session 8 (LangChain)"
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m ipykernel install --user --name session8 --display-name "Session 8 (LangChain)"
```

If PowerShell blocks activation, use Command Prompt with
`.venv\Scripts\activate.bat`, then run the remaining Python commands there.

Open `.env` in your editor. Replace the placeholder with your key from
[Google AI Studio](https://aistudio.google.com). Keep the key in that file.

The four requirements are LangChain with Gemini support, python-dotenv (loads
the key), Jupyter (opens the notebook), and ipykernel (runs notebook cells).
Pip installs their supporting packages automatically.

## 2. Work through the basics

```sh
python -m jupyter notebook 01-langchain-basics/langchain_basics.ipynb
```

Select **Session 8 (LangChain)**. Run cells in order with **Shift+Enter**.
The notebook uses one tent review to teach prompts, models, parsers, chains,
batching, structured output, and parallel branches. Imports appear when needed.
Finish sections 1–8, then move to the lab. The final optional examples can wait.

## 3. Do the TrailMix lab

Read [the lab instructions and flow diagram](02-trailmix-reviews-lab/README.md).
Fill three TODOs in `lab.py`, then run from the repository root:

```sh
python 02-trailmix-reviews-lab/lab.py
```

Open `02-trailmix-reviews-lab/output/triaged_reviews.csv`. It should have
10 rows, with high urgency first. Read the drafts before using them.
`main` contains the student starter. The `solution` branch has the complete lab.

Each exercise keeps its model setting beside its setup code so it can be read
on its own. Both use the same Gemini Flash model. No key goes in Python code.
If you see a 429 error, pause before retrying. Lower batch concurrency to 1
if needed. Re-running model cells makes new API requests.

<details>
<summary>For the instructor: source and Git checks</summary>

The notebook follows the supplied Session 8 slides, with advanced examples
marked optional. We use the current LangChain model and structured-output APIs:
[models](https://docs.langchain.com/oss/python/langchain/models),
[Google integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai).

Before every push, run both checks. The first must show that `.env` is ignored.
The second must print nothing (exit status 1 means no matches).

```sh
git check-ignore -v .env
git ls-files | grep -E '(^|/)\.env$'
```

Notebook outputs are cleared in Git. Generated CSVs are ignored.

</details>
