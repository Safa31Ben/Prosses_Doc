from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Administrative_staff/", include("Administrative_staff.urls")),
    path("Enseignant_candidat/", include("Enseignant_candidat.urls")),
    path("Gestion/", include(("Gestion.urls", "Gestion"), namespace="Gestion")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
