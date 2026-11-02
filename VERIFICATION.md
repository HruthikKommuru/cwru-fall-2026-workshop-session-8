# Verification record

Checked November 1, 2026 on macOS with Python 3.13.12.

## Environment

| Package | Tested version |
| --- | --- |
| langchain | 1.4.7 |
| langchain-core | 1.7.3 |
| langchain-google-genai | 4.4.2 |
| google-genai | 2.34.0 |
| python-dotenv | 1.2.4 |
| jupyter | 1.1.1 |
| notebook | 7.6.4 |
| ipykernel | 7.4.0 |

All installed application dependencies are pinned in `requirements.txt`.
macOS/Unix-only dependencies have platform markers for Windows installs.
Python 3.11.5 is the minimum allowed by these package metadata; only Python
3.13.12 on macOS was executed. Windows and Linux instructions were reviewed,
but not run on those operating systems.

## Passed checks

- Installed the latest stable requested packages in `.venv`, then installed the
  exact requirements into a second, fresh `output/verification-venv`.
- `python -m pip check` reports no broken requirements in both environments.
- Registered the user kernel `session8`, displayed as **Session 8 (LangChain)**.
- All imports and real Google model construction succeed without a network call.
- Real Google adapter schema and `include_raw` parsing paths pass with
  `GenericFakeChatModel` replacing generation.
- All 24 notebook code cells execute with fake replies. Notebook structure is
  valid; every code cell has its three-part explanation and at most 15 lines.
  The saved notebook has no outputs or execution counts.
- The dataset has 50 unique review IDs, ratings 1–5, and eight clear safety cases
  at R001, R005, R008, R015, R020, R025, R030, and R035.
- `main` stops at explicit TODOs. The `solution` pipeline passes extraction,
  reply/urgency parallel branches, batching with concurrency 3, preserved IDs,
  high/medium/low sorting, and stable ordering within a priority.
- A five-review call through the solution's `main()` produces the six expected
  CSV columns with fake generation. Temporary test CSVs are discarded.
- Invalid required fields, invalid enum values, and invalid output urgency are
  rejected before overwriting an existing successful CSV.
- `.env` is ignored and is not tracked. The example contains only the placeholder.
  Root and lab output directories ignore generated CSVs and executed notebooks.

Run `python scripts/offline_smoke.py` on each branch to repeat its applicable checks.
The fake structured-output adapter emulates the model boundary: it checks wiring,
not Gemini's schema enforcement, response quality, or safety judgment.

## Remaining live checks

No configured Gemini key was available; `.env` contains the supplied placeholder.
No paid or free-tier Gemini requests were made. With a valid key in `.env`:

1. Activate `.venv` and run the notebook into an ignored copy:

   ```sh
   python -m jupyter nbconvert --to notebook --execute 01-langchain-basics/langchain_basics.ipynb --output executed-basics --output-dir output --ExecutePreprocessor.timeout=180
   ```

2. Switch to `solution`. Temporarily change `LIMIT = 10` to `LIMIT = 5` in
   `02-trailmix-reviews-lab/lab.py`, then run:

   ```sh
   python 02-trailmix-reviews-lab/lab.py
   ```

3. Inspect `02-trailmix-reviews-lab/output/triaged_reviews.csv` for the six expected
   columns, five reviews, priority order, and polite drafts. Restore `LIMIT = 10`.
4. Before class, test model availability and quota for the intended student accounts.
   Human-review the eight safety cases with a larger LIMIT when quota permits.

Provider calls can still fail because of access, quota, network, or refusals.
The offline tests cannot establish that every live cell succeeds.

## Documentation differences

The current structured-output overview documents agents; its linked standalone
model section is the applicable API here. Native `method="json_schema"` is
recommended by the Google integration. Plain dict schemas still need local
validation. The current model list identifies a newer stable Flash model than
older lecture examples. No deprecated chain APIs or Pydantic classes are used.
The requested Python 3.10 baseline was raised to 3.11.5 because the latest
installed notebook dependencies require it.
