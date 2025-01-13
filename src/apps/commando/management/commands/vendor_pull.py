from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

STATIC_VENDOR_DIR = getattr(settings, "STATIC_VENDOR_DIR")

VENDOR_STATICFILES = {
    "htmx.min.js": "https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js",
    "alpine-core.min.js": "https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js",
}


class Command(BaseCommand):
    help = "Download vendor files."

    def handle(self, *args, **options):
        self.stdout.write("Downloading vendor static files")
        completed_urls = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATIC_VENDOR_DIR / name
            dl_success = self.download_to_local(url, out_path)
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

    def download_to_local(self, url: str, out_path: Path, parent_mkdir: bool = True):
        if parent_mkdir:
            out_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            res = requests.get(url)
            res.raise_for_status()
            # Write using binary mode to prevent \n conversions
            out_path.write_bytes(res.content)

            return True
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")

            return False
