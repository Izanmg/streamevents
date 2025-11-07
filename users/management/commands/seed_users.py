from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from faker import Faker
from django.db import transaction

class Command(BaseCommand):
    help = "Genera usuaris falsos per al projecte StreamEvents"

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Nombre d’usuaris falsos a crear (per defecte: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina tots els usuaris abans de crear-ne de nous'
        )
        parser.add_argument(
            '--with-follows',
            action='store_true',
            help='(Opcional) Genera relacions de seguiment (followers)'
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        fake = Faker('es_ES')
        User = get_user_model()
        num_users = options['users']
        clear = options['clear']
        with_follows = options['with_follows']

        if clear:
            self.stdout.write(self.style.WARNING("🧹 Esborrant usuaris existents..."))

            for user in User.objects.all():
                if not user.is_superuser:
                    user.delete()


        groups = list(Group.objects.all())
        if not groups:
            self.stdout.write(self.style.ERROR("❌ No hi ha grups disponibles. Executa primer els fixtures."))
            return

        self.stdout.write(self.style.SUCCESS(f"🌱 Creant {num_users} usuaris nous..."))

        for _ in range(num_users):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@streamevents.com"
            password = "password123"
            group = fake.random_element(groups)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(f"✅ {num_users} usuaris creats correctament!"))

        if with_follows:
            self.stdout.write(self.style.NOTICE("👥 Generant relacions de seguiment (no implementat en aquest exemple)."))
