from agent.loop import rule_based_model, run_agent

for q in ["calculate 2 + 3 * 4", 'how many words in "tool calling is fun"', "capital of Egypt?", "calculate __import__('os')", "tell me a joke"]:
    print(q, "->", run_agent(q, rule_based_model)["answer"])
