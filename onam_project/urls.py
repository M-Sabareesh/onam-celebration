"""
URL configuration for onam_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from apps.core.admin import admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', admin_site.urls),  # Custom admin with enhanced features
    path('', include('apps.core.urls')),
    # path('accounts/', include('apps.accounts.urls')),  # Temporarily disabled
    # path('game/', include('apps.games.urls')),         # Temporarily disabled
    # path('api/', include('apps.api.urls')),            # Temporarily disabled
    
    # Redirect common missing URLs
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('accounts/login/', RedirectView.as_view(url='/', permanent=False)),
    path('accounts/register/', RedirectView.as_view(url='/', permanent=False)),
    path('game/', RedirectView.as_view(url='/', permanent=False)),
]

# Serve media files in development and production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, ensure media files are served
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    
    # Debug toolbar - temporarily disabled
    # import debug_toolbar
    # urlpatterns += [
    #     path('__debug__/', include(debug_toolbar.urls)),
    # ]
