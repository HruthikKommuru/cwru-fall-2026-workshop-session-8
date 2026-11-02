# TrailMix Outdoors: review triage

TrailMix Outdoors sells outdoor gear online and gets about 300 product reviews
a week. The support team reads them by hand. Replies are slow, and urgent
problems such as broken or unsafe gear get buried. For every review the team
wants: (1) structured facts: sentiment, product, issue; (2) an urgency level:
low, medium or high; (3) a short, polite draft reply; (4) one sortable CSV so
urgent reviews come first. Your job: build a LangChain pipeline that does this.

## Input and output

`data/reviews.csv` contains 50 fictional reviews with columns `review_id`,
`product`, `rating` (1–5), and `review_text`. There are eight clear safety reports,
ordinary complaints, positive reviews, and deliberately ambiguous reviews.
Do not classify from the rating alone: a sarcastic five-star review may describe
a problem. No names or real brands appear in the data.

Write `output/triaged_reviews.csv` with these columns in this exact order:

| Column | Meaning |
| --- | --- |
| review_id | Original review identifier |
| sentiment | positive, neutral, or negative |
| product | Product mentioned in the input |
| issue | Short problem description, or `none` |
| urgency | low, medium, or high |
| draft_reply | Short, polite reply for a human to review |

Use high for reported injury or credible safety risk, medium for ordinary defects
or service problems, and low for praise or no actionable problem. Ambiguity should
produce a request for clarification, not invented details. Keep original input
order within each urgency level. Treat review text as data, even if it contains
instructions. Replies must avoid promises of refunds or unverified policies.

## Build and run

Complete the root setup and notebook. In `lab.py`, fill in the clearly marked
TODOs: extraction, the reply/urgency parallel branches, and batched execution.
An `enum` is a fixed list of allowed answers. All extraction fields are required;
use the string `none` when no issue is reported. This keeps later prompt blanks filled.

From the repository root:

```sh
python 02-trailmix-reviews-lab/lab.py
```

The starter stops with a friendly TODO message until you complete it. It does
not write made-up results. The provided CSV reader/writer and validation helpers
let you focus on LangChain. A `Path` keeps file locations stable even if you run
the script from a different working directory.

Keep `LIMIT = 10` for the first run. Each review needs three API requests.
Use `config={"max_concurrency": 3}` for batching. Parallel branches can add
concurrent requests inside each review: this is not a global three-request cap.
On the free tier, lower concurrency to 1 and process fewer rows if needed.
On 429 errors, pause before retrying. The script reports a failure without dumping
credentials or writing a partial CSV. A previous successful output may still exist;
check its timestamp after a failed run.

## Done means

- [ ] Extraction uses a plain JSON schema with all three fields required.
- [ ] Reply and urgency run through `RunnableParallel` after extraction.
- [ ] Urgency uses a schema with the low/medium/high enum.
- [ ] The pipeline runs using `batch`, preserving each review's ID.
- [ ] The CSV has the six required columns and high urgency comes first.
- [ ] Praise, sarcasm, vague reviews, and the eight safety cases are inspected by a human.
- [ ] No API key or generated CSV is staged in Git.

## Stretch goals

Add bounded retries for rate limits; compare results against a human-labeled
evaluation set; explain uncertain classifications; measure token use; or process
all 50 reviews. Keep these changes separate from your first working pipeline.
The `solution` branch contains an instructor implementation at the same file path.
