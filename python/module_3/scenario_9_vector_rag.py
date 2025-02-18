import boto3
import click

from datetime import date

from app.utils.vector_db import retrieve_from_vector_db


# Scenario 9: Vector RAG with dynamic retrieval
def vector_rag(user_input, conversation=None):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "amazon.nova-lite-v1:0"

        # Get today's date for context, e.g. "Tuesday 03 December 2024"
        today = date.today().strftime("%A %d %B %Y")

        # Define the system prompt with instructions for handling the embedded data
        system = (
            f"Today's date is {today}. You are a travel assistant."
            f"Your are a friendly travel assistant. "
            f"Keep your responses short, with a maximum of three sentences."
            f"You will be given information about travel destinations and activities embedded in <data> tags."
            f"Based on that information, answer the user's question, which is embedded in <question> tags."
        )

        # Retrieve relevant information from the vector database based on the system prompt and query
        click.echo("Retrieving relevant travel info from the vector database...")
        data = retrieve_from_vector_db(f"{system}\n{user_input}")
        click.echo(f"Retrieved travel info:\n{data}\n")

        # Create an augmented prompt combining retrieved data and user question
        augmented_prompt = (
            f"<data>"
            f"{data}"
            f"</data>"
            f"<question>"
            f"{user_input}"
            f"</question>"
        )

        # If this is the first message, initialize the conversation history
        if conversation is None:
            conversation = []

        # Add the augmented prompt to the conversation
        conversation.append(
            {"role": "user", "content": [{"text": augmented_prompt}]}
        )

        # Make the API call with the dynamically retrieved context
        response = client.converse(
            modelId=model_id,
            system=[{"text": system}],
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        # Extract the response and update the conversation history
        model_response = response["output"]["message"]
        response_text = model_response["content"][0]["text"]
        conversation.append(model_response)

        return {
            "response_text": response_text,
            "conversation": conversation
        }

    except Exception as e:
        return {"error": e}
