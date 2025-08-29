from .models import Message

def delete_admin_test_messages():
    Message.objects.filter(text__startswith='Message from admin in chat').delete()

delete_admin_test_messages()
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_list(request):
    chats = request.user.chats.all().order_by('-created_at')
    # Найти пользователей из общих проектов
    from django.db.models import Q
    user_projects = list(request.user.member_projects.all()) + list(request.user.owned_projects.all())
    users = User.objects.filter(
        (
            Q(member_projects__in=user_projects) |
            Q(owned_projects__in=user_projects)
        ) & ~Q(id=request.user.id)
    ).distinct().select_related('profile')
    return render(request, 'aurora_store/chat_list.html', {'chats': chats, 'users': users})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages = chat.messages.order_by('created_at')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(chat=chat, sender=request.user, text=text)
            return redirect('aurora_store:chat_detail', chat_id=chat.id)
    return render(request, 'aurora_store/chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('aurora_store:chat_list')
    chat = Chat.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chat:
        chat = Chat.objects.create()
        chat.participants.add(request.user, other_user)
    return redirect('aurora_store:chat_detail', chat_id=chat.id)
