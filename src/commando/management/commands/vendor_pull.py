from django.conf import settings
from django.core.management.base import BaseCommand

import utils

STATIC_VENDOR_DIR = getattr(settings, "STATIC_VENDOR_DIR")

VENDOR_STATICFILES = {
    "htmx.min.js": "https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js",
    "alpine.min.js": "https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Downloading vendor static files")
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATIC_VENDOR_DIR / name
            dl_success = utils.download_to_local(url, out_path)
            if dl_success:
                completed_urls.append(url)
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download {url}"))
        if set(completed_urls) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(
                self.style.SUCCESS("Successfully updated all vendor static files.")
            )
        else:
            self.stdout.write(self.style.WARNING("Some files were not updated."))
