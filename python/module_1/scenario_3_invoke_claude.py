import boto3
import json


# Scenario 3 - Basic invocation of Claude 3 Haiku
def invoke_claude(user_input: str):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        # Format the input following Claude's message structure
        # Claude expects an array of messages, each with a role and content
        messages = [{
            "role": "user",
            "content": [{"type": "text", "text": user_input}],
        }]

        # Prepare the request payload
        request_payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.5
        }

        # Make the API call to generate a response
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_payload)
        )

        # Extract and return the generated text from the response
        response_payload = json.loads(response["body"].read())
        response_text = response_payload["content"][0]["text"]

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
