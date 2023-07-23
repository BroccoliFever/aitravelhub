from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .api_functions.gpt import generate_text

# Create your views here.
def index(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt")

        # Generate text using the GPT API
        generated_text = generate_text(prompt)

        return render(request, "main_app/index.html", {"generated_text": generated_text})

    return render(request, "main_app/index.html")
