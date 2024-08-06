from typing import Any
from django.core.management import BaseCommand, call_command
from django.contrib.auth import get_user_model
from django.conf import settings



class Command(BaseCommand):

    """ Custom command to run all apps makemigrations(database query base) and 
    migrate (apply this database queries to database) command with this single 
    command also one account created as superuser"""

    def __init__(self, *args, **kwargs):
        self.user_class = get_user_model()
        super().__init__()
    
    def handle(self, *args: Any, **options: Any) -> str | None:

        """ run makemigrations and migrate command for each app"""
        
        apps = settings.INSTALLED_APPS
        for app in apps :
            call_command("makemigrations", app.split(".")[-1])
        call_command("migrate")
        self.create_super_user()

    def create_super_user(self):

        """create super user"""

        admin_user = self.user_class.objects.filter(email="admin@mail.com")
        if admin_user.exists():
            self.stdout.write(f"Admin account '{admin_user.last().email}' already exists")
            return False
        admin_user = self.user_class.objects.create(
            username="admin",
            email="admin@mail.com"
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password("admin")
        admin_user.save()
        self.stdout.write(f"Admin Account '{admin_user.email}' Created.")