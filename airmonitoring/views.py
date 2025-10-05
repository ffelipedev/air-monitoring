# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests
import os
from django.conf import settings

def index(request):
    """Página principal simple"""
    return render(request, 'airmonitoring/index.html', {
        'nasa_username': settings.NASA_USERNAME
    })

def nasa_test(request):
    """Prueba simple de conexión NASA"""
    try:
        # Prueba básica de conexión
        session = requests.Session()
        session.auth = (settings.NASA_USERNAME, settings.NASA_PASSWORD)
        
        # test_url = "https://cmr.earthdata.nasa.gov/search/collections.json?pretty=true"
        test_url = "https://urs.earthdata.nasa.gov/profile"
        response = session.get(test_url)
        
        if response.status_code == 200:
            return JsonResponse({
                'status': 'success',
                'message': '✅ Conexión NASA exitosa',
                'user': settings.NASA_USERNAME
            })
        else:
            return JsonResponse({
                'status': 'error', 
                'message': f'❌ Error: {response.status_code}'
            }, status=400)
            
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'❌ Exception: {str(e)}'
        }, status=500)