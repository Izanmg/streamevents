from django import forms
from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Escribe tu mensaje aquí...",
                    "maxlength": 500,
                }
            )
        }

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if not message or not message.strip():
            raise forms.ValidationError("El mensaje no puede estar vacío.")

        # Lista de palabras ofensivas (ejemplo, se puede ampliar)
        prohibited_words = ["tonto", "estúpido", "idiota", "mierda", "joder"]
        for word in prohibited_words:
            if word in message.lower():
                raise forms.ValidationError("El mensaje contiene palabras ofensivas.")

        if len(message) > 500:
            raise forms.ValidationError("El mensaje no puede exceder los 500 caracteres.")

        return message
