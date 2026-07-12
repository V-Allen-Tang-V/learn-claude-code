import os
import json
import platform
import subprocess


def tools_setting():
    return [
        {
            "type": "function",
            "function": {
                "name": "exec_bash",
                "description": "execute bash command",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "command to execute",
                        }
                    }
                },
                "required": ["command"]
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_system",
                "description": "get system info",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]

# run bash
def exec_bash(command: str) -> str:
    command_black_list = ["rm -rf /", "sudo", "shutdown", "reboot", ">> /dev/"]

    if any(cmd in command for cmd in command_black_list):
        return 'Error: command is not allowed'
    try:
        result = subprocess.run(command, shell=True, cwd=os.getcwd(), capture_output=True,
                                text=True, timeout=60)
        out = (result.stdout + result.stderr).strip()
        return out if out else 'no output'
    except subprocess.TimeoutExpired:
        return 'Error: timeout (60s)'
    except Exception as e:
        return f"execute bash error: {e}, perhaps the command is incompatible with the system."

# get current system
def get_current_system() -> str:
    return platform.system()

# executor
def tool_executor(tool_calls) -> list[dict]:
    tool_execute_result = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        if tool_name == "exec_bash":
            print(f"execute the command: {tool_args["command"]}")
            output = exec_bash(tool_args["command"])
        elif tool_name == "get_current_system":
            print("get system info")
            output = get_current_system()
        else:
            print(f"unknown tool: {tool_name}")
            output = "tool name error: no such tool"
        tool_execute_result.append({"role": "tool", "tool_call_id": tool_call.id, "content": output})
    return tool_execute_result