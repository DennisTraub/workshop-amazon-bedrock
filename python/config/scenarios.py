from collections.abc import Callable
from dataclasses import dataclass, field
from typing import List

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

@dataclass
class Module:
    key: str
    title: str

    def __str__(self):
        return f"Module {self.key}: {self.title}"


@dataclass
class Modules:
    _modules: List[Module]

    def get(self, key: str):
        return next((m for m in self._modules if m.key == key), None)


module_1 = Module("1", "Basic model invocation")
module_2 = Module("2", "Real-world context and memory")
module_3 = Module("3", "Retrieval-augmented generation (RAG)")
module_4 = Module("4", "Tool use (a.k.a. function calling")
module_5 = Module("5", "Amazon Bedrock Inline Agents")


modules = Modules([module_1, module_2])


@dataclass
class ScenarioDetails:
    number: str


@dataclass
class Scenario:
    key: str
    module: Module
    title: str
    function: Callable
    args: List[str] = field(default_factory=list)
    description: str = ""
    file_location: str = ""


@dataclass
class Scenarios:
    _scenarios: List[Scenario]

    def __iter__(self):
        return iter(self._scenarios)

    def __str__(self):
        result: str = ""
        current_module = None
        for scenario in scenarios:
            if scenario.module != current_module:
                current_module = scenario.module
                result += f"\n{current_module}\n"
                result += ("=" * 56) + "\n"
            result += f"{scenario.key} - {scenario.title}\n"

        return result

    def keys(self):
        return [s.key for s in self._scenarios]

    def get(self, key: str):
        return next((s for s in self._scenarios if s.key == key), None)

    def format_available_scenario_numbers(self, delimiter="|"):
        return delimiter.join(list(self.keys()))


scenarios = Scenarios([
    Scenario(
        "1",
        module_1,
        "Invoke Claude 3.5 Haiku",
        invoke_claude,
        description="Scenario 1: Send a message to Claude 3.5 Haiku using the InvokeModel API and Claude's native"
                    "request/response payloads",
        file_location="module_1_basic_invocation/invoke_model.py"
    ),
    Scenario(
        "2",
        module_1,
        "Invoke Llama 3.1 without Meta's chat template",
        invoke_llama,
        description="Scenario 2: Send a message to Llama 3.1 using InvokeModel without a chat template",
        file_location="module_1_basic_invocation/invoke_model.py"
    ),
    Scenario(
        "3",
        module_1,
        "Invoke LLama 3.1 with Meta's chat template",
        invoke_llama_with_chat_template,
        description="Scenario 3: Send a message to Llama 3.1 with Llama's chat template",
        file_location="module_1_basic_invocation/invoke_model.py"
    ),
    Scenario(
        "4",
        module_1,
        "Invoke LLama 3.1 with the converse API",
        invoke_with_the_converse_api,
        ["us.meta.llama3-1-8b-instruct-v1:0"],
        description="Scenario 4: Send a message to Llama using the Bedrock Converse API",
        file_location="module_1_basic_invocation/converse.py"
    ),
    Scenario(
        "5",
        module_1,
        "Invoke Claude 3.5 Haiku with the converse API",
        invoke_with_the_converse_api,
        ["anthropic.claude-3-haiku-20240307-v1:0"],
        description="Scenario 5: Send a message to Claude using the Bedrock Converse API",
        file_location="module_1_basic_invocation/converse.py"
    ),
    Scenario(
        "6",
        module_2,
        "Provide additional context using a system prompt",
        invoke_with_system_prompt,
        description="Scenario 6: Provide additional context using a system prompt",
        file_location="module_2_context_and_memory/system_prompt.py"
    ),
    Scenario(
        "7",
        module_2,
        "Remember the conversation history",
        invoke_with_conversation_history,
        description="Scenario 7: Manage the conversation history to simulate an ongoing chat",
        file_location="module_2_context_and_memory/conversation_history.py"
    )
])
