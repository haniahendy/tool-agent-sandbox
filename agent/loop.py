"""Tool-calling loop with a pluggable "model".

The model is any callable (messages -> dict). It returns either
{"tool": name, "args": {...}} or {"final": text}. A real LLM client can be plugged in;
this repo only ships a rule-based planner, so no LLM reasoning is claimed.
"""
import re

from .tools import REGISTRY


def call_tool(name: str, args: dict, registry=REGISTRY) -> dict:
    """Validate and run a tool. Errors are returned as data so the model can recover."""
    if name not in registry:
        return {"error": f"unknown tool: {name}"}
    spec = registry[name]["args"]
    if set(args) != set(spec):
        return {"error": f"expected args {sorted(spec)}, got {sorted(args)}"}
    for k, typ in spec.items():
        if not isinstance(args[k], typ):
            return {"error": f"arg {k} must be {typ.__name__}"}
    try:
        return {"result": registry[name]["fn"](**args)}
    except Exception as e:  # tool failure is an observation, not a crash
        return {"error": f"{type(e).__name__}: {e}"}


def run_agent(question: str, model, max_steps: int = 5) -> dict:
    messages = [{"role": "user", "content": question}]
    for step in range(max_steps):
        action = model(messages)
        if "final" in action:
            return {"answer": action["final"], "steps": step, "trace": messages}
        obs = call_tool(action["tool"], action["args"])
        messages.append({"role": "assistant", "action": action})
        messages.append({"role": "tool", "observation": obs})
    return {"answer": None, "steps": max_steps, "trace": messages, "error": "max_steps reached"}


def rule_based_model(messages: list[dict]) -> dict:
    """Deterministic stand-in for an LLM: simple pattern rules."""
    last = messages[-1]
    if last["role"] == "tool":
        obs = last["observation"]
        return {"final": f"Error: {obs['error']}"} if "error" in obs else {"final": str(obs["result"])}
    q = last["content"]
    m = re.search(r"calculate\s+(.+)", q, re.I)
    if m:
        return {"tool": "calculator", "args": {"expression": m.group(1).strip(" ?.")}}
    m = re.search(r"how many words in\s+\"(.+)\"", q, re.I)
    if m:
        return {"tool": "word_count", "args": {"text": m.group(1)}}
    if "capital of egypt" in q.lower():
        return {"tool": "lookup", "args": {"key": "capital_of_egypt"}}
    return {"final": "I can calculate, count words, or look up a few facts."}
