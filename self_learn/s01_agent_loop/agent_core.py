import tools as self_tools
from self_learn.model_client import *

def convert_model_response_message(model_response) -> str:
    if model_response.finish_reason != "tool_calls":
        return model_response.message.content
    else:
        return model_response.message.reasoning_content or model_response.message.content or ""

def agent_loop(message: list):
    agent_client = build_client()
    tools = self_tools.tools_setting()
    while True:
        response = build_conversation_response(agent_client, message, tools)
        print(response)
        message.append({"role": "assistant", "content": convert_model_response_message(response)})
        # no need to use the tool, return
        if response.finish_reason != "tool_calls":
            return
        tool_message = self_tools.tool_executor(response.message.tool_calls)
        message.extend(tool_message)