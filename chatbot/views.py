from .chatbot import chatbot
from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # return render_template("chatbot/chatbot.html")
    return render(request, 'chatbot/chatbot.html')


def get_bot_response(request):
    userText = request.GET.get('msg')
    return HttpResponse(str(chatbot.get_response(userText)))
