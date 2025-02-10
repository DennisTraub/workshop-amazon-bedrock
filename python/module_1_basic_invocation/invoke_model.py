import boto3
import json

# Scenario 1 - Invoke Model
def invoke_claude(user_input: str):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        messages = [{
            "role": "user",
            "content": [{"type": "text", "text": user_input}],
        }]

        request_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.5
        }

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_payload)
        )

        response_payload = json.loads(response["body"].read())
        response_text = response_payload["content"][0]["text"]

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}


# Scenario 2 - Invoke Llama 3.1 without a chat template
def invoke_llama(user_input: str):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        model_id = "us.meta.llama3-1-8b-instruct-v1:0"

        request_payload = {
            "prompt": user_input,
            "max_gen_len": 500,
            "temperature": 0.5
        }

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_payload)
        )

        response_payload = json.loads(response["body"].read())
        response_text = response_payload["generation"]

        return response_text, None

    except Exception as e:
        return None, e

# Scenario 3 - Invoke Llama 3.1 with Llama's chat template
def invoke_llama_with_chat_template(user_input: str):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        model_id = "us.meta.llama3-1-8b-instruct-v1:0"

        formatted_user_input = (
            "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
            f"{user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        )

        request_payload = {
            "prompt": formatted_user_input,
            "max_gen_len": 500,
            "temperature": 0.5
        }

        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_payload)
        )

        response_payload = json.loads(response["body"].read())
        response_text = response_payload["generation"]

        return response_text, None

    except Exception as e:
        return None, e
