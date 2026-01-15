from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea un usuario de prueba para desarrollo'

    def handle(self, *args, **kwargs):
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpass123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario "{username}" ya existe.')
            )
            return
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name='Test',
            last_name='User',
            phone='+1234567890'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Usuario de prueba creado exitosamente!')
        )
        self.stdout.write(f'   Username: {username}')
        self.stdout.write(f'   Email: {email}')
        self.stdout.write(f'   Password: {password}')
        self.stdout.write('')
        self.stdout.write('Puedes usar estas credenciales para probar la API.')
