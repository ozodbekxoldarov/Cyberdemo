from django.urls import path
from .views import HomePageView, phishing_demo, phishing_warning, phishing_check, attack_map, attack_map_api

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('phishing-demo/', phishing_demo, name='phishing_demo'),
    path('phishing-warning/', phishing_warning, name='phishing_warning'),
    path('phishing-check/', phishing_check, name='phishing_check'),
    path('attack-map/', attack_map, name='attack_map'),
    path('attack-map/api/', attack_map_api, name='attack_map_api'),
]