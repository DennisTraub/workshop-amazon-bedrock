import boto3
from datetime import date

def invoke_with_system_prompt(user_input):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        # Format today's date, e.g. February 10, 2024
        today = date.today().strftime("%B %d, %Y")

        system = [{
            "text": f"Today's date is {today}. "
                    f"Your are a friendly travel assistant. "
                    f"Keep your responses short, with a maximum of three sentences."
        }]

        conversation = [{
            "role": "user",
            "content": [{"text": user_input}],
        }]

        response = client.converse(
            modelId=model_id,
            system=system,
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
