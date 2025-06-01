from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from together import Together
import os
from dotenv import load_dotenv

# API KEY doğrudan yazılmış (production için os.environ tercih edilmeli)
load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

@csrf_exempt
def ask_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Yalnızca POST kabul edilir"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()

        # Temel sistem mesajı
        system_message = (
            "Codenthia adlı yazılım destek platformunun resmi botusun. "
            "Kullanıcıya kısa, net ama profesyonel cevaplar ver. Yazılım alanında uzmansın. "
            "Kod örneklerini, tabloları ve açıklamaları düzenli ve okunabilir şekilde sun. "
            "Gerekirse markdown formatı kullanabilirsin.\n\n"
            "Cevaplarını Türkçe ver, ama kodlar İngilizce yazılmalı. "
            "Karmaşık konularda adım adım açıklama yapabilirsin."
        )

        # Codenthia ile ilgili belirli sorular için tanıtım bilgisi ekle
        intro_triggers = ["codenthia nedir", "codenthia hakkında", "kurucu kim", "kim kurdu", "codenthia kim"]
        should_add_intro = any(trigger in user_message for trigger in intro_triggers)

        if should_add_intro:
            system_message += (
                "\n\nCodenthia ile ilgili sorulara şu bilgileri ekleyerek cevap ver: "
                "'Codenthia, yazılımcılar için hazırlanmış modern bir bilgi ve destek platformudur. "
                "Kurucusu Erkan TURGUT'tur (LinkedIn: https://linkedin.com/in/erkan1205). "
                "Resmi site: https://codenthia.com. Bizi tercih ettiğiniz için teşekkür ederiz!'"
            )

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {"role": "user", "content": user_message}
            ]
        )

        answer = response.choices[0].message.content
        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def chatbot_page(request):
    return render(request, "chatbot/chat.html")