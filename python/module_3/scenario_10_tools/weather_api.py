def get_weather_api_spec():
    """
    Defines the tool specification using the API Schema format
    This tells the model what parameters the tool expects and how to use it
    """
    return {
        "toolSpec": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city to get weather for",
                        }
                    },
                    "required": ["city"],
                }
            }
        }
    }

def call_weather_api(city):
    """
    Simulates a weather API with hardcoded responses
    In a real application, this would call an actual weather service API
    """
    weather_data = {
        "barcelona": {"temperature": "12°C/54°F", "condition": "Partly cloudy"},
        "new_york": {"temperature": "-2°C/28°F", "condition": "Clear skies"},
    }
    return weather_data.get(city.lower().replace(" ", "_"))
