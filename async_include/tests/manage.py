#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Ensure project root and tests directories are in sys.path
    tests_dir = Path(__file__).resolve().parent
    project_root = tests_dir.parent.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(tests_dir) not in sys.path:
        sys.path.insert(0, str(tests_dir))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
