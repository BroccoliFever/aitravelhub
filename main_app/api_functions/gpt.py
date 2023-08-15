import openai
from django.conf import settings
import json
from .yelp import *

def generate_text(prompt):
    formate_string = """
        {
            "name": business name,
            "rating": business rating,
            "review_count": business review count,
            "url": business url,
            "image_url": business image url
        }
    """
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
        # System instructions
        messages.append(
            {
                "role": "system",
                "content":  "Please return your response as a list of dictionaries, where each dictionary has only the keys: id, suggestion_reason."
                            "The format MUST BE FOLLOWED as it is being passed to the Yelp API."
                            "DO NOT PUT THE BUSINESS NAME AS THE ID, use the id that is returned from the Yelp API."
                            "For example: [{id: 123, suggestion_reason: 'This business is great!'}, {id: 456, suggestion_reason: 'This business is also great!'}]}]"
                            "Use what you know and what you get from the Yelp API to suggest ten businesses to the user." 
                            "Tell the user why you are suggesting these businesses."
                            "Don't include a sentence at the beginning of your reasons that says 'This place is has X stars and Y reviews.'"
                            "Please make your reason about 100 to 150 characters long."
            }
        )


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
    print(response.choices[0].message.content)
    return response.choices[0].message.content