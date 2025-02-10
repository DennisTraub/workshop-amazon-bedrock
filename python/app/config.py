from app.types import Module, Modules, Scenarios, Scenario

from module_1_basic_invocation import (
    invoke_claude,
    invoke_llama,
    invoke_llama_with_chat_template,
    invoke_with_the_converse_api
)

from module_2_context_and_memory import (
    invoke_with_system_prompt,
    invoke_with_conversation_history
)


modules = Modules(
    [
        Module("1", "Basic model invocation"),
        Module("2", "Adding context and memory"),
        Module("3", "RAG and Tool Use"),
        Module("5", "Amazon Bedrock Inline Agents"),
    ]
)

scenarios = Scenarios([
    Scenario(
        "1",
        Module("1", "Basic model invocation"),
        "Invoke Claude 3.5 Haiku",
        invoke_claude,
        description="Scenario 1: Send a message to Claude 3.5 Haiku using InvokeModel",
        file_location="module_1_basic_invocation/invoke_model.py"
    ),
    Scenario(
        "2",
        Module("1", "Basic model invocation"),
        "Invoke Llama 3.1 without Meta's chat template",
        invoke_llama,
        description="Scenario 2: Send a message to Llama 3.1 using InvokeModel (no chat template)",
        file_location="module_1_basic_invocation/invoke_model.py"
    ),
    Scenario(
        "3",
        Module("1", "Basic model invocation"),
        "Invoke LLama 3.1 with Meta's chat template",
        invoke_llama_with_chat_template,
        description="Scenario 3: Send a message to Llama 3.1 with Llama's chat template",
        file_location="module_1_basic_invocation/invoke_model.py"
    ),
    Scenario(
        "4",
        Module("1", "Basic model invocation"),
        "Invoke LLama 3.1 with the converse API",
        invoke_with_the_converse_api,
        ["us.meta.llama3-1-8b-instruct-v1:0"],
        description="Scenario 4: Send a message to Llama using the Bedrock Converse API",
        file_location="module_1_basic_invocation/converse.py"
    ),
    Scenario(
        "5",
        Module("1", "Basic model invocation"),
        "Invoke Claude 3.5 Haiku with the converse API",
        invoke_with_the_converse_api,
        ["anthropic.claude-3-haiku-20240307-v1:0"],
        description="Scenario 5: Send a message to Claude using the Bedrock Converse API",
        file_location="module_1_basic_invocation/converse.py"
    ),
    Scenario(
        "6",
        Module("2", "Adding context and memory"),
        "Provide additional context using a system prompt",
        invoke_with_system_prompt,
        description="Scenario 6: Provide additional context using a system prompt",
        file_location="module_2_context_and_memory/system_prompt.py"
    ),
    Scenario(
        "7",
        Module("2", "Adding context and memory"),
        "Remember the conversation history",
        invoke_with_conversation_history,
        description="Scenario 7: Manage the conversation history to simulate an ongoing chat",
        file_location="module_2_context_and_memory/conversation_history.py"
    )
])
