from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Download global.db and user.db from Cloudflare R2 if missing locally (run before migrations)'

    def handle(self, *args, **options):
        from pu_mp.r2_db_sync import sync_on_startup
        sync_on_startup()
        self.stdout.write(self.style.SUCCESS('R2 DB sync complete'))
