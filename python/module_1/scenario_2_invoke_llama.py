import boto3
import json


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

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
