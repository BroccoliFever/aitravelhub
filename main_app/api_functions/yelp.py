import requests
from django.conf import settings

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {settings.YELP_API_KEY}",
}

def yelp_get_data(location, term):
    url = "https://api.yelp.com/v3/businesses/search?"
    location_url = f"location={location}"
    term_url = f"term={term}"

    response = requests.get(url + location_url + "&" + term_url, headers=headers)
    return response.json()


def yelp_get_function():
    '''Returns the function parameters for the Yelp API so that GPT can format the request correctly.'''
    return [
        {
            "name": "yelp_get_data",
            "description": "Get data from the Yelp API",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to search for"
                    },
                    "term": {
                        "type": "string",
                        "description": "The term to search for"
                    },
                },
                "required": ["location", "term"],
            },
        }
    ]

def yelp_get_business_info(id):
    url = f"https://api.yelp.com/v3/businesses/{id}"
    return requests.get(url, headers=headers).json()

