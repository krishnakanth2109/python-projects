# users/views.py
import csv
import subprocess
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from user_management_api.settings import EMAIL_HOST_USER

@api_view(['POST'])
def upload_data(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    file = request.FILES['file']
    if not file.name.endswith('.csv'):
        return JsonResponse({'error': 'Invalid file format. Please upload a CSV file.'}, status=400)

    try:
        with transaction.atomic():
            reader = csv.reader(file.read().decode('utf-8', errors='replace').splitlines())
            next(reader)  # Skip header row

            for row in reader:
                name, email, username, address, role = row
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={'name': name, 'username': username, 'address': address, 'role': role}
                )

                if created:
                    send_mail(
                        'Welcome to the Platform',
                        f'Hello {name},\nYour data has been successfully stored.',
                        EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )

            return JsonResponse({'message': 'Data uploaded and emails sent successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def view_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def backup_database(request):
    try:
        backup_file = 'backup.sql'
        with open(backup_file, 'w') as f:
            subprocess.run(['mysqldump', '-u', 'your_username', '-p', 'user_management_db'], stdout=f)
        return JsonResponse({'message': 'Backup completed successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def restore_database(request):
    try:
        backup_file = 'backup.sql'
        with open(backup_file, 'r') as f:
            subprocess.run(['mysql', '-u', 'your_username', '-p', 'user_management_db'], stdin=f)
        return JsonResponse({'message': 'Database restored successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
