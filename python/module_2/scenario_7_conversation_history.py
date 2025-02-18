import boto3
from datetime import date


# Scenario 7: Retain the conversation history across multiple calls
def conversation_history(user_input, conversation=None):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "amazon.nova-lite-v1:0"

        # Get today's date for context, e.g. "Tuesday 03 December 2024"
        today = date.today().strftime("%A %d %B %Y")

        # Define the system prompt
        system = [{
            "text": f"Today's date is {today}. "
                    f"Your are a friendly travel assistant. "
                    f"Keep your responses short, with a maximum of three sentences."
        }]

        # If this is the first message, initialize the conversation history
        if conversation is None:
            conversation = []

        # Add the new user message to the conversation
        conversation.append(
            {"role": "user", "content": [{"text": user_input}]}
        )

        # Make the API call with the full conversation history
        response = client.converse(
            modelId=model_id,
            system=system,
            messages=conversation, # Pass the entire conversation history
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        # Extract the model's response
        model_response = response["output"]["message"]
        response_text = model_response["content"][0]["text"]

        # Add the model's response to the conversation history
        conversation.append(model_response)

        # Return both the response and updated conversation history
        return {
            "response_text": response_text,
            "conversation": conversation
        }

    except Exception as e:
        return {"error": e}
