import boto3
import json


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

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
