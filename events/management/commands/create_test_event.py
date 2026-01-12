from django.core.management.base import BaseCommand
from events.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un evento de prueba si no existe.'

    def handle(self, *args, **options):
        admin_user = User.objects.filter(username='admin').first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('El usuario admin no existe. Por favor, crea un superusuario primero.'))
            return

        if not Event.objects.filter(name='Evento de Prueba').exists():
            Event.objects.create(name='Evento de Prueba', status='live', creator=admin_user)
            self.stdout.write(self.style.SUCCESS('Evento de Prueba creado con éxito.'))
        else:
            self.stdout.write(self.style.WARNING('El Evento de Prueba ya existe.'))
