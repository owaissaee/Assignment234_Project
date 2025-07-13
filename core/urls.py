from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

web_patterns = [
    path('admin/', admin.site.urls),  # ✅ Admin panel
    path('web/', include('resume_builder.web.urls')),
    path('web/', include('accounts.web.urls')),
    path('accounts/', include('allauth.urls')),
    path('jobs/', include('jobs.urls')),
    path('applications/', include(('applications.urls', 'applications'), namespace='applications')),
    path('', include('dashboard.urls')),  # Main homepage or dashboard
]

apis_patterns = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('resume_builder.api.urls')),
    path('api/v1/', include('accounts.api.urls')),
]

urlpatterns = web_patterns + apis_patterns

# ✅ Only serve media and static files in DEBUG mode (not catch-all!)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
