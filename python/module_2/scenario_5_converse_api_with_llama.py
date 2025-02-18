import boto3


# Scenario 5: Invoke Llama with the Converse API
def converse_api_with_llama(user_input):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "us.meta.llama3-1-8b-instruct-v1:0"

        # Format the conversation using the messages structure
        # Note: There's no difference to the previous example with Claude,
        # the Converse API provides a unified interface across different models
        conversation = [
            {"role": "user", "content": [{"text": user_input}]}
        ]

        # Make the API call to generate a response
        # Note: The same API structure works for Claude, Llama, and any other supported model
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
