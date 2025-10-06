from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
from django.conf import settings

def index(request):
    """
    Vista principal de Airmonitoring
    """
    ciudades_predeterminadas = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Londres', 'Paris']
    
    context = {
        'ciudades_predeterminadas': ciudades_predeterminadas,
        'titulo': 'Airmonitoring - Calidad del Aire'
    }
    
    return render(request, 'airmonitoring/index.html', context)

def obtener_calidad_aire(request):
    """
    API endpoint para obtener calidad del aire
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ciudad = data.get('ciudad', '').strip()
            
            if not ciudad:
                return JsonResponse({
                    'success': False, 
                    'error': 'Por favor ingresa una ciudad'
                })
            
            # Usar API key de settings
            api_key = "3fe59fad829b30186993c68f4456506b"
            
            if not api_key:
                return JsonResponse({
                    'success': False, 
                    'error': 'API key no configurada en el servidor'
                })
            
            print(f"🔍 Buscando: {ciudad}")
            
            # 1. Obtener coordenadas
            url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={ciudad}&limit=1&appid={api_key}"
            respuesta_geo = requests.get(url_geo, timeout=10)
            
            if respuesta_geo.status_code != 200:
                return JsonResponse({
                    'success': False, 
                    'error': f'Error del servicio: {respuesta_geo.status_code}'
                })
                
            datos_geo = respuesta_geo.json()
            
            if not datos_geo:
                return JsonResponse({
                    'success': False, 
                    'error': f'Ciudad no encontrada: "{ciudad}"'
                })
            
            lat = datos_geo[0]['lat']
            lon = datos_geo[0]['lon']
            nombre_ciudad = datos_geo[0]['name']
            pais = datos_geo[0].get('country', '')
            
            print(f"📍 Coordenadas: {lat}, {lon}")
            
            # 2. Obtener calidad del aire
            url_aire = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
            respuesta_aire = requests.get(url_aire, timeout=10)
            
            if respuesta_aire.status_code != 200:
                return JsonResponse({
                    'success': False, 
                    'error': f'Error al obtener datos de calidad del aire: {respuesta_aire.status_code}'
                })
            
            datos_aire = respuesta_aire.json()
            
            # Procesar respuesta
            componentes = datos_aire['list'][0]['components']
            aqi = datos_aire['list'][0]['main']['aqi']
            
            calidad_texto = {
                1: "BUENA",
                2: "MODERADA", 
                3: "REGULAR",
                4: "MALA",
                5: "MUY MALA"
            }
            
            resultado = {
                'ciudad': nombre_ciudad,
                'pais': pais,
                'coordenadas': {
                    'lat': lat,
                    'lon': lon
                },
                'componentes': {
                    'o3': round(componentes['o3'], 2),
                    'pm2_5': round(componentes['pm2_5'], 2),
                    'pm10': round(componentes['pm10'], 2),
                    'no2': round(componentes['no2'], 2),
                    'so2': round(componentes['so2'], 2),
                    'co': round(componentes['co'], 2)
                },
                'indice_calidad': {
                    'valor': aqi,
                    'texto': calidad_texto.get(aqi, 'DESCONOCIDO')
                },
                'timestamp': datos_aire['list'][0]['dt']
            }
            
            print(f"✅ Datos obtenidos para: {nombre_ciudad}")
            return JsonResponse({'success': True, 'data': resultado})
            
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False, 
                'error': 'Tiempo de espera agotado. Intenta nuevamente.'
            })
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'success': False, 
                'error': 'Error de conexión. Verifica tu internet.'
            })
        except Exception as e:
            print(f"❌ Error: {e}")
            return JsonResponse({
                'success': False, 
                'error': f'Error inesperado: {str(e)}'
            })
    
    return JsonResponse({
        'success': False, 
        'error': 'Método no permitido. Usa POST.'
    })