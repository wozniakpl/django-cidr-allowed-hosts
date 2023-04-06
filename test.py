import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def run_tests():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    django.setup()
    failures = get_runner(settings)().run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()
