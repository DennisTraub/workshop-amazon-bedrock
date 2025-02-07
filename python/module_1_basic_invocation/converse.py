import boto3

def converse(user_input, model_id):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        conversation = [{
            "role": "user",
            "content": [{"text": user_input}],
        }]

        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        return response_text, None

    except Exception as e:
        return None, e
