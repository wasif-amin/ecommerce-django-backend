from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path('', RedirectView.as_view(url='http://localhost:5173/', permanent=False)) 
]
#