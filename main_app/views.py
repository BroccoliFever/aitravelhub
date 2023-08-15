from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .api_functions.gpt import generate_text
from .api_functions.yelp import yelp_get_business_info
from django.core.paginator import Paginator
import ast

# Create your views here.

def index(request):
    if request.method == "POST":
        generated_text = generate_text(request.POST.get("prompt"))
        data_list = ast.literal_eval(generated_text)
        for business in data_list:
            temp_data = yelp_get_business_info(business["id"])
            business["image_url"] = temp_data["image_url"]
            business["url"] = temp_data["url"]
            business["rating"] = "/static/main_app/small/" + str(temp_data["rating"]).replace(".", "") + ".png"
            business["review_count"] = temp_data["review_count"]
            business["name"] = temp_data["name"]

        request.session["temp_data_list"] = data_list  # Store data in the session
        return HttpResponseRedirect(request.path)  # Redirect to the same page to clear POST data

    # Retrieve the stored data from the session
    data_list = request.session.get("temp_data_list", [])

    paginator = Paginator(data_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "main_app/index.html", {"data_list": page_obj})