# urls.py

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home,predict,aboutus, tokenize_text, delete_prediction

urlpatterns = [
    path('', home, name='home'),
    path('home.html', home, name='home_html'),
    path('predict/', predict, name='predict'),
    path('predict.html', predict, name='predict_html'),
    path('aboutus/', aboutus, name='aboutus'),
    path('aboutus.html', aboutus, name='aboutus_html'),
    path('tokenize_text/', tokenize_text, name='tokenize_text'),
    path('delete_prediction/<int:prediction_id>/', delete_prediction, name='delete_prediction'),
]

# Add this for serving static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
