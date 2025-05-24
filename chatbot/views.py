from django.shortcuts import render

# Create your views here.

import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

API_URL = "https://router.huggingface.co/together/v1/chat/completions"
HEADERS = {
    "Authorization": "Bearer hf_nTqWkgkzdMQTyhgroCyRhNOFhRHcqHzb"
}
@csrf_exempt  # Eğer frontend başka origin’den istek yapıyorsa
def ask_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Yalnızca POST kabul edilir"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")

        payload = {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        response_data = response.json()

        answer = response_data["choices"][0]["message"]["content"]
        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def chatbot_page(request):
    return render(request, "chatbot/chat.html") 
