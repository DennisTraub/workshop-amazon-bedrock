# Installation Instructions (Traditional)

## Prerequisites
- Python 3.12 or higher
- An AWS account
- The AWS CLI locally installed and configured
- Access configured for Claude 3.5 Haiku and Llama 3.1 in us-east-1

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
1. Run like: `uv run app.py list`
