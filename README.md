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

The lab is in **`02-trailmix-reviews-lab/`**:

```text
02-trailmix-reviews-lab/
  data/reviews.csv             Your 10 input reviews
  lab.py                       Complete code, ready to run
  output/triaged_reviews.csv   Your results, created after a successful run
```

All code is complete on **`main`**. After setup, you only need to run it.

1. Open a terminal in the repository folder (the folder containing this README).
   Use the virtual environment and `.env` key from step 1 above.
2. Run:

   ```sh
   python 02-trailmix-reviews-lab/lab.py
   ```

3. When you see **`Saved 10 reviews to ...`**, open
   **`02-trailmix-reviews-lab/output/triaged_reviews.csv`** in your editor or Excel.
   It contains 10 results, with high urgency first.

Read [the lab walkthrough](02-trailmix-reviews-lab/README.md) and the comments in
[lab.py](02-trailmix-reviews-lab/lab.py) to understand each step.

The script creates the output folder and CSV automatically. Your results are
saved **on your computer**, inside the lab's `output` folder. They do not appear
on GitHub because generated CSVs are ignored. Running the script again replaces
the previous CSV.

Each example keeps its model setting beside its setup code so it can be read
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
