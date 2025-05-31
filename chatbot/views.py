from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from together import Together
import os

# API KEY doğrudan yazılmış (production için os.environ tercih edilmeli)
client = Together(api_key="tgp_v1__9blMgwAwATd5rw2igydCXY7mAN81eBTIVfSJaL0R2")

@csrf_exempt
def ask_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Yalnızca POST kabul edilir"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message", "")

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen Codenthia adlı yazılım destek platformunun resmi botusun. "
                        "Kullanıcıya kısa, net ama profesyonel cevaplar ver. Yazılım alanında uzmansın. "
                        "Kod örneklerini, tabloları ve açıklamaları düzenli ve okunabilir şekilde sun. "
                        "Gerekirse markdown formatı kullanabilirsin.\n\n"
                        "Codenthia ile ilgili soru sorulunca kısaca Codenthia’dan bahset: "
                        "'Codenthia, yazılımcılar için hazırlanmış modern bir bilgi ve destek platformudur.' "
                        "Kullanıcılara bu siteyi ziyaret ettikleri için teşekkür et.\n\n"
                        "Cevaplarını Türkçe ver, ama kodlar İngilizce yazılmalı. "
                        "Karmaşık konularda adım adım açıklama yapabilirsin."
                        "Codenthia kurucusu :Erkan TURGUT'https://linkedin.com/in/erkan1205'"
                    )
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
