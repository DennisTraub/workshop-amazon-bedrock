import boto3


def converse_api_with_llama(user_input):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    model_id = "us.meta.llama3-1-8b-instruct-v1:0"

    conversation = [{
        "role": "user",
        "content": [{"text": user_input}],
    }]

    try:
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
