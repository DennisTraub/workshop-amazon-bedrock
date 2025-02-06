import boto3
import json

# Exercise 1 - Invoke Model
def invoke_model(user_input: str, session):

    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        claude_haiku = "anthropic.claude-3-haiku-20240307-v1:0"
        nova_micro = "amazon.nova-micro-v1:0"

        request_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": user_input}],
                }
            ],
        }

        response = client.invoke_model(
            modelId=claude_haiku,
            body=json.dumps(request_payload)
        )

        response_payload = json.loads(response["body"].read())
        response_text = response_payload["content"][0]["text"]

        return response_text, None


    except Exception as e:
        return None, e
