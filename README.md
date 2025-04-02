# Modules and scenarios

```
Module 1: Basic model invocation with native payloads
====================================================================
1 - Invoke Llama 3.1 without a chat template
2 - Invoke LLama 3.1 with Meta's chat template
3 - Invoke Amazon Nova

Module 2: The Converse API, system prompts, and conversation history
====================================================================
4 - Invoke Amazon Nova with the Converse API
5 - Invoke LLama 3.1 with the Converse API
6 - Provide additional context through a system prompt
7 - Remember the conversation history across invocations

Module 3: Retrieval-augmented generation (RAG) and tool-use
====================================================================
8 - Basic RAG: Load additional data into the context
9 - Vector RAG: Retrieve relevant data from a vector database
10 - Tool use (a.k.a. function calling)
```

# Prerequisites
- Python 3.12 or higher
- An AWS account
- The AWS CLI locally installed and configured
- Access configured for Claude 3.5 Haiku and Llama 3.1 in us-east-1

# Installation Instructions (pip)

## Initial setup

### 1. Navigate to the python directory
```bash
cd python
```

### 2. Create a virtual environment
 ```bash
   python -m venv .venv
```
### 3. Activate the virtual environment

```bash
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

### 4. Install the required dependencies
```bash
  pip install -r requirements.txt
```

## Run the app

### 1. List the available scenarios
```bash
  python app.py list
```

### 2. Run a specific scenario
```bash
  # python app.py run [SCENARIO_NUMBER], e.g.:
  python app.py run 1
```

# Installation Instructions (uv)

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
1. `uv sync`
1. Run like: `uv run app.py list` or `uv run app.py run 1`
