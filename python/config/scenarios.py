from bedrock import (
    invoke_claude,
    invoke_llama,
    invoke_llama_with_chat_template,
    converse
)

modules = {
    "1": "Basic model invocation",
    "2": "Simplify model switching with the Converse API",
}

scenarios = {
    "1": {
        "function": invoke_claude,
        "description": "Invoke Claude 3.5 Haiku",
        "module": modules["1"]
    },
    "2": {
        "function": invoke_llama,
        "description": "Invoke Llama 3.1 without Meta's chat template",
        "module": modules["1"]
    },
    "3": {
        "function": invoke_llama_with_chat_template,
        "description": "Invoke LLama 3.1 with Meta's chat template",
        "module": modules["1"]
    },
    "4": {
        "function": converse,
        "args": ["anthropic.claude-3-haiku-20240307-v1:0"],
        "description": "Invoke Claude 3.5 Haiku with the converse API",
        "module": modules["2"]
    },
    "5": {
        "function": converse,
        "args": ["us.meta.llama3-1-8b-instruct-v1:0"],
        "description": "Invoke LLama 3.1 with the converse API",
        "module": modules["2"]
    },
}
