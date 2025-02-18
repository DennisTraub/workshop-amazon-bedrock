import boto3


# Scenario 4: Invoke Amazon Nova with the Converse API
def converse_api_with_nova(user_input):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "amazon.nova-lite-v1:0"

        # Format the conversation using the messages structure
        # The Converse API expects an array of messages with role and content
        conversation = [
            {"role": "user", "content": [{"text": user_input}]}
        ]

        # Make the API call to generate a response
        # Note: converse() is a higher-level API compared to invoke_model()
        # It handles message formatting and response parsing automatically
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        # Extract and return the response text from the structured output
        response_text = response["output"]["message"]["content"][0]["text"]
        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
