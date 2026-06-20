"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Base_app.views import r2_presign, serve_sw, serve_offline

from django.views.generic import TemplateView

urlpatterns = [
    # SEO
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml")),
    path('sw.js', TemplateView.as_view(template_name="sw.js", content_type="application/javascript")),

    # Admin
    path('admin/', admin.site.urls),

    # PWA files served from root so SW scope covers /
    path('sw.js', serve_sw, name='sw'),
    path('offline/', serve_offline, name='offline'),

    # Base app (includes: home, about, help, terms, privacy, safety, contact)
    path('', include('Base_app.urls')),

    # Authentication
    path('auth/', include('Auth_app.urls')),

    # Main apps
    path('dashboard/', include('dash_app.urls')),
    path('listings/', include('Listings_app.urls')),
    path('profile/', include('Profile_app.urls')),
    path('chat/', include('chat_app.urls')),
    path('search/', include('search_app.urls')),
    path("accounts/", include("allauth.urls")),
    path('api/r2-presign/', r2_presign, name='r2_presign'),

]
# Media & Static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)