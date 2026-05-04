import pickle
import os
import requests
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from .models import PhishingAttempt

PHISHING_MODEL_PATH = os.path.join(settings.BASE_DIR, 'phishing_model.pkl')
PHISHING_VEC_PATH   = os.path.join(settings.BASE_DIR, 'phishing_vectorizer.pkl')

with open(PHISHING_MODEL_PATH, 'rb') as f:
    phishing_model = pickle.load(f)

with open(PHISHING_VEC_PATH, 'rb') as f:
    phishing_vectorizer = pickle.load(f)

TIMEZONE_COORDS = {
    'Asia/Tashkent':      (41.2995,  69.2401, 'Uzbekistan',   'Tashkent'),
    'Asia/Samarkand':     (39.6542,  66.9597, 'Uzbekistan',   'Samarkand'),
    'Asia/Almaty':        (43.2220,  76.8512, 'Kazakhstan',   'Almaty'),
    'Asia/Bishkek':       (42.8746,  74.5698, 'Kyrgyzstan',   'Bishkek'),
    'Asia/Dushanbe':      (38.5598,  68.7733, 'Tajikistan',   'Dushanbe'),
    'Asia/Ashgabat':      (37.9601,  58.3261, 'Turkmenistan', 'Ashgabat'),
    'Asia/Kabul':         (34.5553,  69.2075, 'Afghanistan',  'Kabul'),
    'Europe/Moscow':      (55.7558,  37.6173, 'Russia',       'Moscow'),
    'Asia/Yekaterinburg': (56.8389,  60.6057, 'Russia',       'Yekaterinburg'),
    'Asia/Novosibirsk':   (54.9885,  82.9207, 'Russia',       'Novosibirsk'),
    'Europe/London':      (51.5074,  -0.1278, 'UK',           'London'),
    'Europe/Berlin':      (52.5200,  13.4050, 'Germany',      'Berlin'),
    'Europe/Paris':       (48.8566,   2.3522, 'France',       'Paris'),
    'Europe/Rome':        (41.9028,  12.4964, 'Italy',        'Rome'),
    'Europe/Madrid':      (40.4168,  -3.7038, 'Spain',        'Madrid'),
    'Europe/Warsaw':      (52.2297,  21.0122, 'Poland',       'Warsaw'),
    'Europe/Kiev':        (50.4501,  30.5234, 'Ukraine',      'Kyiv'),
    'Europe/Istanbul':    (41.0082,  28.9784, 'Turkey',       'Istanbul'),
    'Asia/Dubai':         (25.2048,  55.2708, 'UAE',          'Dubai'),
    'Asia/Riyadh':        (24.7136,  46.6753, 'Saudi Arabia', 'Riyadh'),
    'Asia/Tehran':        (35.6892,  51.3890, 'Iran',         'Tehran'),
    'Asia/Karachi':       (24.8607,  67.0011, 'Pakistan',     'Karachi'),
    'Asia/Kolkata':       (22.5726,  88.3639, 'India',        'Kolkata'),
    'Asia/Dhaka':         (23.8103,  90.4125, 'Bangladesh',   'Dhaka'),
    'Asia/Bangkok':       (13.7563, 100.5018, 'Thailand',     'Bangkok'),
    'Asia/Singapore':     ( 1.3521, 103.8198, 'Singapore',    'Singapore'),
    'Asia/Seoul':         (37.5665, 126.9780, 'South Korea',  'Seoul'),
    'Asia/Tokyo':         (35.6762, 139.6503, 'Japan',        'Tokyo'),
    'Asia/Shanghai':      (31.2304, 121.4737, 'China',        'Shanghai'),
    'America/New_York':   (40.7128, -74.0060, 'USA',          'New York'),
    'America/Chicago':    (41.8781, -87.6298, 'USA',          'Chicago'),
    'America/Los_Angeles':(34.0522,-118.2437, 'USA',          'Los Angeles'),
    'America/Sao_Paulo':  (-23.5505,-46.6333, 'Brazil',       'Sao Paulo'),
    'America/Mexico_City':(19.4326, -99.1332, 'Mexico',       'Mexico City'),
    'Africa/Cairo':       (30.0444,  31.2357, 'Egypt',        'Cairo'),
    'Africa/Lagos':       ( 6.5244,   3.3792, 'Nigeria',      'Lagos'),
    'Africa/Johannesburg':(-26.2041, 28.0473, 'South Africa', 'Johannesburg'),
    'Australia/Sydney':   (-33.8688, 151.2093,'Australia',    'Sydney'),
}


def get_geo(ip):
    try:
        if ip in ('127.0.0.1', 'localhost', '::1'):
            return {}
        res = requests.get(f'http://ip-api.com/json/{ip}', timeout=2)
        data = res.json()
        if data.get('status') == 'success':
            return {
                'country': data.get('country', ''),
                'city':    data.get('city', ''),
                'lat':     data.get('lat'),
                'lon':     data.get('lon'),
            }
    except Exception:
        pass
    return {}


class HomePageView(TemplateView):
    template_name = 'home.html'


def phishing_demo(request):
    if request.method == 'POST':
        email       = request.POST.get('email', '')
        password    = request.POST.get('password', '')
        ip          = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        ip          = ip.split(',')[0].strip()
        user_agent  = request.META.get('HTTP_USER_AGENT', '')
        timezone    = request.POST.get('timezone', '')
        language    = request.POST.get('language', '')
        screen_size = request.POST.get('screen_size', '')
        platform    = request.POST.get('platform', '')
        geo_lat     = request.POST.get('geo_lat', '')
        geo_lon     = request.POST.get('geo_lon', '')

        if geo_lat and geo_lon:
            try:
                lat = float(geo_lat)
                lon = float(geo_lon)
                geo = {'lat': lat, 'lon': lon, 'country': '', 'city': ''}
            except ValueError:
                geo = {}
        else:
            geo = {}

        if not geo:
            geo = get_geo(ip)

        if not geo and timezone in TIMEZONE_COORDS:
            lat, lon, country, city = TIMEZONE_COORDS[timezone]
            geo = {'country': country, 'city': city, 'lat': lat, 'lon': lon}

        PhishingAttempt.objects.create(
            email=email,
            password=password,
            ip_address=ip,
            user_agent=user_agent,
            country=geo.get('country', ''),
            city=geo.get('city', ''),
            latitude=geo.get('lat'),
            longitude=geo.get('lon'),
            timezone=timezone,
            language=language,
            screen_size=screen_size,
            platform=platform,
        )
        return redirect('phishing_warning')
    return render(request, 'phishing_demo.html')


def phishing_warning(request):
    jami = PhishingAttempt.objects.count()
    return render(request, 'phishing_warning.html', {'jami': jami})


def phishing_check(request):
    natija = None
    if request.method == 'POST':
        email_text = request.POST.get('email_text', '')
        vec  = phishing_vectorizer.transform([email_text])
        prob = phishing_model.predict_proba(vec)[0]

        if prob[1] >= 0.5:
            natija = {'xavf': 'PHISHING', 'foiz': round(prob[1] * 100, 1), 'rang': 'danger'}
        else:
            natija = {'xavf': 'NORMAL',   'foiz': round(prob[0] * 100, 1), 'rang': 'success'}

    return render(request, 'phishing_check.html', {'natija': natija})


def attack_map(request):
    barchasi = list(PhishingAttempt.objects.exclude(latitude=None).values(
        'email', 'ip_address', 'country', 'city',
        'latitude', 'longitude', 'user_agent',
        'timezone', 'language', 'screen_size', 'platform'
    ))
    oxirgi = barchasi[0:1] if barchasi else []
    return render(request, 'attack_map.html', {
        'urinishlar': barchasi,
        'xarita': oxirgi,
    })


def attack_map_api(request):
    data = list(PhishingAttempt.objects.exclude(latitude=None).values(
        'email', 'ip_address', 'country', 'city',
        'latitude', 'longitude', 'user_agent',
        'timezone', 'language', 'screen_size', 'platform'
    ))
    return JsonResponse(data, safe=False)