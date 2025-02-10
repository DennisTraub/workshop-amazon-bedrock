import boto3
import json
import os
from datetime import date


def load_context(file_name):
    script_path = os.path.abspath(__file__)
    file_path = os.path.join(os.path.dirname(script_path), file_name)

    with open(file_path, 'r') as file:
        return json.load(file)

# Scenario 8 - Basic RAG: Load external data into the context
def basic_rag(user_input, conversation=None):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        # Format today's date, e.g. February 10, 2024
        today = date.today().strftime("%B %d, %Y")

        system = [{
            "text": f"Today's date is {today}. You are a travel assistant."
                    f"Your are a friendly travel assistant. "
                    f"Keep your responses short, with a maximum of three sentences."
                    f"You will be given JSON data embedded in <data> tags about travel destinations and activities."
                    f"With that information, answer the user's question, embedded in <question> tags."
        }]

        if conversation is None:
            conversation = []

        data = json.dumps(load_context("files/travel_info.json"))

        augmented_prompt = f"<data>{data}</data>\n"\
                           f"<question>{user_input}</question>"

        conversation.append({
            "role": "user",
            "content": [{"text": augmented_prompt}],
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
