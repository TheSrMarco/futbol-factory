import os
import sys

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futbol_factory.settings')
    command = sys.argv if len(sys.argv) > 1 else [sys.argv[0], 'runserver']
    execute_from_command_line(command)
