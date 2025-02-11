import boto3
from datetime import date

def conversation_history(user_input, conversation=None):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        # Format today's date, e.g. "Tuesday 03 December 2024"
        today = date.today().strftime("%A %d %B %Y")

        system = [{
            "text": f"Today's date is {today}. "
                    f"Your are a friendly travel assistant. "
                    f"Keep your responses short, with a maximum of three sentences."
        }]

        if conversation is None:
            conversation = []

        conversation.append({
            "role": "user",
            "content": [{"text": user_input}],
        })

        response = client.converse(
            modelId=model_id,
            system=system,
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        model_response = response["output"]["message"]
        response_text = model_response["content"][0]["text"]

        conversation.append(model_response)

        return {
            "response_text": response_text,
            "conversation": conversation
        }

    except Exception as e:
        return {"error": e}
