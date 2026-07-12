import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
model_name = os.getenv("MODEL_NAME")

# build OpenAI client
def build_client() -> OpenAI:
    api_key = os.environ.get('MODELSCOPE_SDK_TOKEN')
    base_url = os.getenv('MODEL_SCOPE_BASE_URL')
    if not api_key:
        raise ValueError("missing model API key")
    if not base_url:
        raise ValueError("missing model base url")
    client = OpenAI(api_key=api_key, base_url=base_url)
    return client

# build conversation
def build_conversation_response(client, message, tools=None):
    if not model_name:
        raise ValueError("missing model name")
    print(message)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=message,
            stream=False,
            tools=tools if tools else None,
            timeout=60,
            max_tokens=500
        )
        if not response or not response.choices:
            raise ValueError("model response is empty")
        response_content = response.choices[0]
        return response_content
    except Exception as e:
        print(f"failed to call open ai api: {str(e)}")
        raise