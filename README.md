# tool-agent-sandbox

A minimal tool-calling agent loop: a tool registry with argument validation, a safe calculator (AST-based, no `eval`), error-as-observation handling, a max-steps guard, and a pluggable "model" callable.

## Important limit
The only model included is a **rule-based planner** (regex rules), not an LLM. This repo demonstrates the agent plumbing (tool schemas, validation, loop, failure handling, tests). It does not show LLM reasoning. To use a real model, pass a function that takes the message list and returns `{"tool", "args"}` or `{"final"}`.

## Run
```bash
pip install -r requirements.txt
python -m pytest -q   # 8 test cases
python run.py
```

## Limits
No parallel tool calls, memory, streaming or retries. Three toy tools. The calculator allows `**`, so a huge exponent could use a lot of CPU; a production tool would cap it.

## Provenance
A learning and portfolio project.
