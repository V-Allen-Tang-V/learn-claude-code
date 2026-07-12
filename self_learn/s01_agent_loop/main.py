import agent_core

SYSTEM_PROMPT = """You are a coding agent, Use bash to solve tasks. Act, don't explain."""

if __name__ == "__main__":
    print("Please enter your question")
    user_history_content = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            query = input()
        except (EOFError, KeyboardInterrupt):
            break

        if query.lower().strip() in ("q", "exit", ""):
            break
        user_history_content.append({"role": "user", "content": query})
        agent_core.agent_loop(user_history_content)

        agent_answer = user_history_content[-1]["content"]
        if isinstance(agent_answer, str):
            print(agent_answer)
        elif isinstance(agent_answer, list):
            for block in agent_answer:
                if isinstance(block, dict) and "text" in block:
                    print(block["text"])
                elif isinstance(block, str):
                    print(block)
        print()