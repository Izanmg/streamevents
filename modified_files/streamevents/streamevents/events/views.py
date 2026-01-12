from django.shortcuts import render, get_object_or_404
from .models import Event
from chat.forms import ChatMessageForm

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    chat_form = ChatMessageForm()
    return render(request, 'events/event_detail.html', {'event': event, 'chat_form': chat_form})
