import boto3
import click

from datetime import date

from .scenario_10_tools import call_weather_api, get_weather_api_spec


# Scenario 10: Tool use (also known as function calling)
def process_response(follow_up_response, client, depth=0, max_depth=3, **params):
    """
    Recursively processes model responses that may contain tool use requests
    Handles the back-and-forth between the model and tools
    """
    # Prevent infinite recursion
    if depth >= max_depth:
        print(f"Maximum recursion depth ({max_depth}) reached")
        return

    # Get the current conversation state
    conversation = params["messages"]
    conversation.append(follow_up_response["output"]["message"])

    tool_results = []

    # Process each content block in the response
    content_blocks = follow_up_response["output"]["message"]["content"]
    for content_block in content_blocks:
        # Handle plain text responses
        if "text" in content_block and len(content_blocks) == 1:
            return content_block["text"]
        elif "text" in content_block:
            click.echo(content_block["text"])

        # Handle tool use requests
        elif "toolUse" in content_block:
            tool_use_request = content_block["toolUse"]
            if tool_use_request["name"] == "get_weather":
                # Execute the weather tool
                tool_use_id = tool_use_request["toolUseId"]
                city = tool_use_request["input"]["city"]
                weather_info = call_weather_api(city)

                tool_results.append({
                    "toolResult": {
                        "toolUseId": tool_use_id,
                        "content": [{"json": weather_info}],
                    }
                })

                # Update the conversation in the request parameters
                params["messages"] = conversation

    if len(tool_results) > 0:
        # Add the tool's response(s) to conversation
        conversation.append({
            "role": "user",
            "content": tool_results
        })

        # Send the tool results to the model
        follow_up_response = client.converse(**params)

        return process_response(follow_up_response, client, depth + 1, max_depth, **params)

def tool_use(user_input, conversation=None):
    try:
        # Initialize the Bedrock Runtime client
        client = boto3.client("bedrock-runtime", region_name="us-east-1")

        # Specify the foundation model to use
        model_id = "amazon.nova-lite-v1:0"

        # Get today's date for context, e.g. "Tuesday 03 December 2024"
        today = date.today().strftime("%A %d %B %Y")

        # Define a system prompt with strict rules about tool usage
        system = [{
            "text": f"Today's date is {today}. You are a travel assistant."
                    f"Your are a friendly travel assistant. "
                    f"Keep your responses short, with a maximum of three sentences."
                    f"You have access to the tool 'get_weather'."
                    f"You MUST follow the rules below:"
                    f"- ALWAYS use the get_weather to get weather information."
                    f"- NEVER rely on anything else for weather information."
                    f"- NEVER make up weather information."
                    f"- If the tool doesn't return the weather, say that you don't know the answer."
                    f"- If the question is not related to travel, say that you don't know the answer."
        }]

        # Initialize conversation history if None
        if conversation is None:
            conversation = []

        # Add the new user message to the conversation
        conversation.append(
            {"role": "user", "content": [{"text": user_input}]}
        )

        # Configure the list of available tools
        tool_config = {"tools": [get_weather_api_spec()]}

        # Prepare the parameters for the API call
        params = {
            "modelId": model_id,
            "toolConfig": tool_config,
            "system": system,
            "messages": conversation
        }

        # Make the initial API call
        response = client.converse(**params)

        # Process the response (may involve multiple tool interactions)
        return {
            "response_text": process_response(response, client, **params),
            "conversation": conversation
        }

    except Exception as e:
        return {"error": e}
