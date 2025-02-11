import boto3
import json


# Scenario 1 - Invoke Claude
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
