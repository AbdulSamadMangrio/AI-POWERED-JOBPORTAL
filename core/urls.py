from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sim.urls')),
    # path('api/', include('sim.urls')),  # API routes
]
