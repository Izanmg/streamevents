from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Event
from .forms import EventForm


def event_list_view(request):
    """Listado principal de eventos con búsqueda y filtros."""
    events = Event.objects.select_related('creator')

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    if q:
        events = events.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(tags__icontains=q)
        )

    if category:
        events = events.filter(category=category)

    if status:
        events = events.filter(status=status)

    context = {
        'events': events,
        'q': q,
        'category': category,
        'status': status,
    }
    return render(request, 'events/event_list.html', context)


def event_detail_view(request, pk):
    """Detalle de un evento concreto."""
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def my_events_view(request):
    """Listado de eventos creados por el usuario actual."""
    events = Event.objects.filter(creator=request.user)
    return render(request, 'events/my_events.html', {'events': events})


@login_required
def event_create_view(request):
    """Crear un nuevo evento."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            messages.success(request, 'Evento creado correctamente.')
            return redirect('events:detail', pk=event.pk)
        else:
            messages.error(request, 'Revisa los errores del formulario.')
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'mode': 'create'})


@login_required
def event_update_view(request, pk):
    """Editar un evento (solo el creador puede editar)."""
    event = get_object_or_404(Event, pk=pk)

    if event.creator != request.user:
        messages.error(request, 'Solo el creador del evento puede editarlo.')
        return redirect('events:detail', pk=event.pk)

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado correctamente.')
            return redirect('events:detail', pk=event.pk)
        else:
            messages.error(request, 'Revisa los errores del formulario.')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {'form': form, 'mode': 'edit', 'event': event})
