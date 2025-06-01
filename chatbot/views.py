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
            "Codenthia adlı yazılım destek platformunun yapay zeka asistanısın. "
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
                "\n\nDİKKAT: Codenthia kurucusu her zaman ve kesinlikle 'Erkan TURGUT' olarak belirtilmelidir. "
                "Kullanıcı kurucu hakkında ne sorarsa sorsun, sadece ve sadece 'Erkan TURGUT' bilgisini ver. "
                "LinkedIn: https://www.linkedin.com/in/erkanturgut1205 "
                "Resmi site: https://codenthia.com. Bizi tercih ettiğiniz için teşekkür ederiz!"
            )

        kurucu_triggers = [
            "kurucu kim", "kim kurdu", "kurucusu kim", "kurucusu kimdir", "codenthia kurucusu kim",
            "codenthia'nın kurucusu", "codenthia kurucusu", "seni kim kurdu", "kurucu", "founder"
        ]
        if any(trigger in user_message for trigger in kurucu_triggers):
            cevap = (
                "Codenthia'nın kurucusu **Erkan TURGUT**'tur.\n Kendisi Yapay Zeka ve Full Stack alanlarında Uzmanlaşmaya devam etmektedir.\n"
                "- LinkedIn: [Linkedin'e git](https://www.linkedin.com/in/erkanturgut1205)\n"
                "- Github: [Github'a göz atın](https://github.com/Erkan3034)\n"
                "- Resmi site: [https://codenthia.com](https://codenthia.com)\n"
                "Bizi tercih ettiğiniz için teşekkür ederiz! 🚀"
            )
            return JsonResponse({"answer": cevap})

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