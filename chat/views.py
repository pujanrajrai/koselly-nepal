from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from accounts.models import MyUser
from chat.models import Chat
from decorator import is_admin_or_user, is_user, is_admin


@is_admin()
def all_chat(request):
    chat = Chat.objects.filter(Q(send_from=request.user) | Q(send_to=request.user)).order_by('send_date_time')
    chat_send_from = set(chat.values_list('send_from__username'))
    chat_send_to = set(chat.values_list('send_to__username'))
    chat_union = chat_send_to.union(chat_send_from)
    context = {'chats': chat_union}
    return render(request, 'chat/all_chat.html', context)


@is_admin_or_user()
def view_chat(request, username):
    context = {'username': username,
               }
    if request.method == 'POST':
        try:
            message = request.POST['message']
            Chat.objects.create(
                send_from=request.user,
                send_to=MyUser.objects.get(username=username),
                message=message,
            )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        except:
            print('something went wrong')

    return render(request, 'chat/my_chat.html', context)


@is_admin_or_user()
def new_chat(request, username):
    chat = Chat.objects.filter(
        (Q(send_from=request.user) & Q(send_to__username=username)) | Q(send_from__username=username) & Q(
            send_to=request.user)).order_by('-send_date_time')
    return JsonResponse(
        {'message': list(chat.values('send_from__username', 'send_to__username', 'send_date_time', 'message'))})
