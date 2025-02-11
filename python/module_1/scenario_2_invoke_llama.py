import boto3
import json


# Scenario 1 - Basic invocation of Llama 3.1 without a chat template
def invoke_llama(user_input: str):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "us.meta.llama3-1-8b-instruct-v1:0"

        # Prepare the request payload with model parameters
        # Note: Llama has a different input format compared to Claude
        request_payload = {
            "prompt": user_input,
            "max_gen_len": 500,
            "temperature": 0.5
        }

        # Make the API call to generate a response
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_payload)
        )

        # Extract and return the generated text from the response
        # Note: Llama has a different response format compared to Claude
        response_payload = json.loads(response["body"].read())
        response_text = response_payload["generation"]

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
