from app.types import Module, Scenarios, Scenario

from module_1 import invoke_claude, invoke_llama, invoke_llama_with_chat_template
from module_2 import converse_api_with_claude, converse_api_with_llama, system_prompt, conversation_history
from module_3 import simple_rag, vector_rag, tool_use


module_1 = Module("1", "Basic model invocation with native payloads")
module_2 = Module("2", "The Converse API, system prompts, and conversation history")
module_3 = Module("3", "Retrieval-augmented generation (RAG) and tool-use")
module_4 = Module("4", "Amazon Bedrock Inline Agents")

scenarios = Scenarios([
    Scenario("1", module_1, "Invoke Claude 3.5 Haiku", invoke_claude),
    Scenario("2", module_1, "Invoke Llama 3.1 without a chat template", invoke_llama),
    Scenario("3", module_1, "Invoke LLama 3.1 with Meta's chat template", invoke_llama_with_chat_template),
    Scenario("4", module_2, "Invoke Claude 3.5 Haiku with the Converse API", converse_api_with_claude),
    Scenario("5", module_2, "Invoke LLama 3.1 with the Converse API", converse_api_with_llama),
    Scenario("6", module_2, "Provide additional context through a system prompt", system_prompt),
    Scenario("7", module_2, "Remember the conversation history across invocations", conversation_history),
    Scenario("8", module_3, "Basic RAG: Load additional data into the context", simple_rag),
    Scenario("9", module_3, "Vector RAG: Retrieve relevant data from a vector database", vector_rag),
    Scenario("10", module_3, "Tool use (a.k.a. function calling)", tool_use)
])
