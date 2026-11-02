# LangChain basics

Finish the root README setup first. From the repository root, run:

```sh
python -m jupyter notebook 01-langchain-basics/langchain_basics.ipynb
```

Select **Session 8 (LangChain)** from the kernel menu. A kernel is the Python
process that runs your cells. Use Shift+Enter to run one cell and move down.
Read each explanation before running its code. Start at section 0; later cells
reuse earlier variables. You can restart the kernel to begin again.

Only sections that invoke, batch, or stream a model use quota. Creating prompts,
formatting them, and parsing hard-coded replies happen locally. The debugging
section deliberately calls the model again so students can see each intermediate
result. A missing-key message means you need to edit the root `.env` file.

Outputs are cleared in Git. Before committing your own notebook, use
**Edit → Clear Outputs of All Cells**, then save. Never display your key.
If you get a 429 error, wait and retry later; reduce batch concurrency to 1.
Some model replies vary between runs, even with the same prompt.
