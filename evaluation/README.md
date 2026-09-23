# QuantNova AI Evaluation

See [REPORT.md](REPORT.md) for the measured 28-case evaluation, gold answers,
quality and behavior metrics, real HTTP latency, and k=1/3/5 retrieval ablation.
[responses.md](responses.md) contains every baseline answer and tool trace.

Run from the repository root in Command Prompt:

```cmd
.venv\Scripts\python.exe -m evaluation.run_benchmark
```

`benchmark_cases.json` is the executed evaluation set, defined in `build_cases.py`.
`results/benchmark.json` contains all three configurations, source hashes, and
individual latency samples. `results/qualitative_review.json` records the
single-evaluator baseline groundedness and citation relevance review.

The prior `questions.json` remains as a historical draft, not the executed rubric.
The current web app does not support ticket creation, PostgreSQL, or model calls.

After changing the app, re-review the qualitative annotations in `write_report.py`
before running `python -m evaluation.write_report`; those judgments are specific
to the saved responses and must not be carried forward without inspection.
