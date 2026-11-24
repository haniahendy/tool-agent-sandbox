import pytest

from agent.loop import call_tool, rule_based_model, run_agent
from agent.tools import calculator


def test_calculator_precedence_and_unary():
    assert calculator("2 + 3 * 4") == 14
    assert calculator("-2 ** 2") == -4
    assert calculator("10 / 4") == 2.5


@pytest.mark.parametrize("bad", ["__import__('os').system('x')", "open('f')", "1 + a"])
def test_calculator_rejects_unsafe(bad):
    with pytest.raises((ValueError, SyntaxError)):
        calculator(bad)


def test_call_tool_validation_errors():
    assert "unknown tool" in call_tool("nope", {})["error"]
    assert "expected args" in call_tool("calculator", {})["error"]
    assert "must be str" in call_tool("word_count", {"text": 5})["error"]
    assert "KeyError" in call_tool("lookup", {"key": "zzz"})["error"]


def test_end_to_end_answers():
    assert run_agent("calculate 2 + 3 * 4", rule_based_model)["answer"] == "14"
    assert run_agent('how many words in "a b c"', rule_based_model)["answer"] == "3"
    assert run_agent("capital of Egypt?", rule_based_model)["answer"] == "Cairo"


def test_tool_error_is_reported_not_raised():
    ans = run_agent("calculate __import__('os')", rule_based_model)["answer"]
    assert ans.startswith("Error")


def test_max_steps_guard():
    loop_forever = lambda msgs: {"tool": "word_count", "args": {"text": "x"}}
    r = run_agent("hi", loop_forever, max_steps=3)
    assert r["answer"] is None and r["error"] == "max_steps reached" and r["steps"] == 3
