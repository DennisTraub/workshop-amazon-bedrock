import boto3
import json


# Scenario 3 - Basic invocation of Amazon Nova
def invoke_nova(user_input: str):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "amazon.nova-lite-v1:0"

        # Format the input following Claude's message structure
        # Claude expects an array of messages, each with a role and content
        messages = [{
            "role": "user",
            "content": [{"text": user_input}]
        }]

        # Prepare the request payload
        request_payload = {
            "schemaVersion": "messages-v1",
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": 500,
                "temperature": 0.5
            }
        }

        # Make the API call to generate a response
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_payload)
        )

        # Extract and return the generated text from the response
        response_payload = json.loads(response["body"])
        response_text = response_payload["output"]["message"]["content"][0]["text"]

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
