import boto3
import click

from datetime import date

from _app.utils import retrieve_from_vector_db


def vector_rag(user_input, conversation=None):
    try:
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        model_id = "anthropic.claude-3-haiku-20240307-v1:0"

        # Format today's date, e.g. "Tuesday 03 December 2024"
        today = date.today().strftime("%A %d %B %Y")

        system = f"Today's date is {today}. You are a travel assistant." \
                f"Your are a friendly travel assistant. " \
                f"Keep your responses short, with a maximum of three sentences." \
                f"You will be given information in <data> tags about travel destinations and activities." \
                f"With that information, answer the user's question, embedded in <question> tags."

        if conversation is None:
            conversation = []

        # Retrieve data based on the system prompt and user question
        click.echo("Retrieving relevant travel info from the vector database...")
        data = retrieve_from_vector_db(f"{system}\n{user_input}")

        click.echo(f"Retrieved travel info:\n{data}\n")

        augmented_prompt = (f"<data>"
                            f"{data}"
                            f"</data>"
                            f"<question>"
                            f"{user_input}"
                            f"</question>")

        conversation.append({
            "role": "user",
            "content": [{"text": augmented_prompt}],
        })

        response = client.converse(
            modelId=model_id,
            system=[{"text": system}],
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
