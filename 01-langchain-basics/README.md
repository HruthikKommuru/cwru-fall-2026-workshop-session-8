# LangChain basics

Complete the setup in the root README and put your Gemini key in `.env`.
From the repository root, open the notebook:

```sh
python -m jupyter notebook 01-langchain-basics/langchain_basics.ipynb
```

Select **Session 8 (LangChain)**. Run one cell at a time with **Shift+Enter**.
Later cells reuse earlier variables, so start at the top.

| Notebook section | What you learn | Lecture slides |
| --- | --- | --- |
| 1 | Call Gemini and read its reply; system and human messages | 5–16 |
| 2 | Fill a prompt's named blank | 11, 17–18 |
| 3 | Parse text, connect a chain, recognize Runnables | 8–10, 13, 20 |
| 4 | invoke, batch, and stream | 21–22 |
| 5 | Extract sentiment, product, and issue into a dictionary | 24–27 |
| 6 | Pass extracted facts to a reply chain | 31, 33 |
| 7 | Generate a reply and urgency in parallel | 32–33 |
| 8 | Reuse these pieces in the 10-review lab | 35–38 |

The main lesson has 14 short code cells. Each has an explanation, an action,
and a result to look for. Read the printed result before moving on.
For a small change, edit the review text and rerun from that point.

Five optional examples at the end cover the other prompt types, list and JSON
parsers, and parsing errors. You can do the lab without them.

The exercises call real Gemini using your `.env` key. If a cell fails, check the
message, the selected kernel, and your key. For a 429 error, wait before retrying.
Responses can vary. A correctly shaped dictionary can still contain a wrong fact.

When you finish section 8, open the [TrailMix lab](../02-trailmix-reviews-lab/README.md).
