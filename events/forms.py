from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Event


class EventForm(forms.ModelForm):
    scheduled_for = forms.DateTimeField(
        label=_('Fecha y hora'),
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'category',
            'difficulty',
            'scheduled_for',
            'status',
            'thumbnail',
            'max_viewers',
            'duration_minutes',
            'tags',
            'stream_url',
            'is_featured',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Título del evento')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'max_viewers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('python, django, directo')}),
            'stream_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': _('https://...')}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_scheduled_for(self):
        dt = self.cleaned_data['scheduled_for']
        if dt < timezone.now():
            raise forms.ValidationError(_('La fecha del evento debe ser futura.'))
        return dt

    def clean_tags(self):
        tags = (self.cleaned_data.get('tags') or '').strip()
        # Normalizar: quitar espacios extra y duplicados
        if not tags:
            return ''
        parts = [t.strip() for t in tags.split(',') if t.strip()]
        return ', '.join(sorted(set(parts)))
