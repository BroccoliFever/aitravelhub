import openai
from django.conf import settings
import json
from .yelp import *

def generate_text(prompt):
    openai.api_key = settings.GPT_API_KEY
    yelp_function = yelp_get_function()
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        functions=yelp_function,
        function_call="auto"
    )

    new_response = response["choices"][0]["message"]

    if (new_response.get("function_call")):
        # Get the function arguments
        function_args = json.loads(new_response["function_call"]["arguments"])
        # Call the function
        function_response = yelp_get_data(function_args["location"], function_args["term"])
        # Add the original response and the function response to the messages
        messages.append(new_response)
        for business in function_response["businesses"]:
            messages.append(
                {
                    "role": "function",
                    "name": "yelp_get_data",
                    "content": f"""
                                {business['id']}:
                                {business['name']} - {business['rating']}/5",
                                {business['review_count']} reviews",
                                
                                """
                }
            )
        # Instruct it on how to format response
        messages.append(
            {
                "role": "system",
                "content": "In the above, do not show the business ID to the user, and please add a new line between each business.",
            }
        )


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    print(response.choices[0].message.content)
    return response.choices[0].message.content