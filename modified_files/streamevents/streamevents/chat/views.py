from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import ChatMessageForm
from .models import ChatMessage
from events.models import Event # Asegúrate de que esta importación sea correcta


@login_required
@require_POST
def chat_send_message(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)

    if event.status != 'live':
        return JsonResponse({'success': False, 'errors': {'__all__': 'El chat solo está disponible durante eventos en directo.'}}, status=400)

    form = ChatMessageForm(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.user = request.user
        message.event = event
        message.save()

        return JsonResponse({
            'success': True,
            'message': {
                'id': str(message.id), # Convertir ObjectId a string
                'user': message.user.username,
                'display_name': message.get_user_display_name(),
                'message': message.message,
                'created_at': message.get_time_since(),
                'can_delete': message.can_delete(request.user),
                'is_highlighted': message.is_highlighted,
            }
        })
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def chat_load_messages(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    messages = ChatMessage.objects.filter(event=event, is_deleted=False).order_by('created_at')[:50]

    messages_data = []
    for message in messages:
        messages_data.append({
            'id': str(message.id),
            'user': message.user.username,
            'display_name': message.get_user_display_name(),
            'message': message.message,
            'created_at': message.get_time_since(),
            'can_delete': message.can_delete(request.user),
            'is_highlighted': message.is_highlighted,
        })
    return JsonResponse({'messages': messages_data})

@login_required
@require_POST
def chat_delete_message(request, message_pk):
    message = get_object_or_404(ChatMessage, pk=message_pk)

    if not message.can_delete(request.user):
        return JsonResponse({'success': False, 'error': 'No tienes permiso para eliminar este mensaje.'}, status=403)

    message.is_deleted = True
    message.save()
    return JsonResponse({'success': True})

@login_required
@require_POST
def chat_highlight_message(request, message_pk):
    message = get_object_or_404(ChatMessage, pk=message_pk)

    # Verificar que el usuario es el creador del evento
    if not (hasattr(message.event, 'creator') and message.event.creator == request.user):
        return JsonResponse({'success': False, 'error': 'Solo el creador del evento puede destacar mensajes.'}, status=403)

    message.is_highlighted = not message.is_highlighted # Toggle
    message.save()
    return JsonResponse({'success': True, 'is_highlighted': message.is_highlighted})
