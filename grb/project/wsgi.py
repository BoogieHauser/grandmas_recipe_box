"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Get the absolute path of the wsgi.py file
wsgi_path = os.path.abspath(__file__)

# Get the 'project' directory (the directory containing wsgi.py)
project_path = os.path.dirname(wsgi_path)

# Get the 'grb' directory
grb_path = os.path.dirname(project_path)

# Get the parent directory of 'grb', which is '/workspace'
workspace_path = os.path.dirname(grb_path)

# Add the 'grb' directory and the workspace directory to sys.path
sys.path.insert(0, grb_path)
sys.path.insert(0, workspace_path)

# Debug: Print paths
print("WSGI Path:", wsgi_path)
print("Project Path:", project_path)
print("GRB Path:", grb_path)
print("Workspace Path:", workspace_path)
print("sys.path:", sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
