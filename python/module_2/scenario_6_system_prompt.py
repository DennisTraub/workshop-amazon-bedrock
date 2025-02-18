import boto3
from datetime import date


# Scenario 6: Providing additional context with system prompts
def system_prompt(user_input):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model ID
        model_id = "amazon.nova-lite-v1:0"

        # Get today's date for context, e.g. "Tuesday 03 December 2024"
        today = date.today().strftime("%A %d %B %Y")

        # Define the system prompt
        # This sets up the assistant's persona and behavioral guidelines
        system = [{
            "text": f"Today's date is {today}. "
                    f"Your are a friendly travel assistant. "
                    f"Keep your responses short, with a maximum of three sentences."
        }]

        # Format the conversation using the messages structure
        conversation = [
            {"role": "user", "content": [{"text": user_input}]}
        ]

        # Make the API call with both system prompt and user message
        response = client.converse(
            modelId=model_id,
            system=system,
            messages=conversation,
            inferenceConfig={"maxTokens": 500, "temperature": 0.5}
        )

        # Extract and return the response text from the structured output
        response_text = response["output"]["message"]["content"][0]["text"]
        return {"response_text": response_text}

    except Exception as e:
        return {"error": e}
