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
  lab.py                       The code you edit and run
  output/triaged_reviews.csv   Your results, created after a successful run
```

1. Open [the lab instructions](02-trailmix-reviews-lab/README.md), then open
   [lab.py](02-trailmix-reviews-lab/lab.py).
2. Fill in the **three TODOs** using the basics notebook. Save the file.
3. In the terminal, stay in the repository folder (the folder containing this
   README). Use the virtual environment and `.env` key from step 1 above. Run:

   ```sh
   python 02-trailmix-reviews-lab/lab.py
   ```

4. Wait for the message **`Saved 10 reviews to ...`**.
5. Open **`02-trailmix-reviews-lab/output/triaged_reviews.csv`** in your editor
   or Excel. Check the 10 results, with high urgency first.

The script creates the output folder and CSV automatically. Your results are
saved **on your computer**, inside the lab's `output` folder. They do not appear
on GitHub because generated CSVs are ignored. Running the script again replaces
the previous CSV.

If you see **`Complete TODO...`**, finish that TODO, save, and run the same command
again. No results are written until the TODOs are complete and the run succeeds.

<details>
<summary>Instructor: completed lab</summary>

`main` contains the student starter. The complete lab is on the
[`solution` branch](https://github.com/HruthikKommuru/cwru-fall-2026-workshop-session-8/blob/solution/02-trailmix-reviews-lab/lab.py).

</details>

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
