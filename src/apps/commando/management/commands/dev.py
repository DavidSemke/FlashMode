from subprocess import Popen

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Start the development server with TailwindCSS watch process."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting TailwindCSS watch process...")
        tw_watch_process = Popen(["pnpm", "tw_watch"])

        self.stdout.write("Starting the Django development server...")
        call_command("runserver", *args, **kwargs)

        tw_watch_process.terminate()
