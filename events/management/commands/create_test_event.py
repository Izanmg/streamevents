from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Event

User = get_user_model()


class Command(BaseCommand):
    help = "Crea un evento de prueba si no existe."

    def handle(self, *args, **options):
        admin_user = User.objects.filter(username="admin").first()
        if not admin_user:
            self.stdout.write(
                self.style.ERROR(
                    "El usuario admin no existe. Crea un superusuario primero."
                )
            )
            return

        title = "Evento de Prueba"
        if Event.objects.filter(title=title).exists():
            self.stdout.write(self.style.WARNING("El Evento de Prueba ya existe."))
            return

        Event.objects.create(
            title=title,
            description="Evento de prueba para validar el flujo de la app.",
            category=Event.CATEGORY_TALK,
            difficulty=Event.DIFFICULTY_BEGINNER,
            status=Event.STATUS_LIVE,
            scheduled_for=timezone.now(),
            creator=admin_user,
        )
        self.stdout.write(self.style.SUCCESS("Evento de Prueba creado con exito."))
