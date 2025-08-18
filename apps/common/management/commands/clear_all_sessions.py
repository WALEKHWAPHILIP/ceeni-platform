from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = 'Logs out all users by clearing all sessions.'

    def handle(self, *args, **kwargs):
        # Get all sessions
        sessions = Session.objects.all()

        # Check if there are any sessions
        if sessions.exists():
            self.stdout.write("Sessions found before deletion:")
            # Print each session key for tracking/debugging
            for s in sessions:
                self.stdout.write(f" - {s.session_key}")
        else:
            self.stdout.write("No sessions found.")

        # Delete all sessions (logs out all users)
        deleted_count, _ = sessions.delete()
        self.stdout.write(f"✅ All sessions cleared. ({deleted_count} deleted)")
