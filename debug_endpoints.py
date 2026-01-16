
import os
import sys

# Setup Django environment first
sys.path.append(r'c:\Users\Usuario\Documents\GitHub\wisebet_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def debug_api():
    print("Debugging API Endpoints...")
    client = APIClient()
    
    # Authenticate
    user = User.objects.filter(username='test_user_schema').first()
    if not user:
        user = User.objects.create_user(username='test_user_schema', password='password123')
    
    client.force_authenticate(user=user)

    try:
        url = reverse('distribuidora-list')
        print(f"Testing URL: {url}")
        response = client.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.content.decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    debug_api()
