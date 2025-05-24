from django.urls import path
from .views import ask_api, chatbot_page


urlpatterns = [
    path('', chatbot_page, name='chatbot_page'),   # /chatbot/ sayfası
    path('ask/', ask_api, name='chatbot_ask'),     # /chatbot/ask/ API POST isteği
]
