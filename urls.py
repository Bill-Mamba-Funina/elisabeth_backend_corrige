from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def frontend(request):
    return redirect("http://localhost:3000/")


urlpatterns = [
    # ========================================================
    # FRONTEND NEXT.JS
    # ========================================================

    path(
        "",
        frontend,
        name="frontend",
    ),

    # ========================================================
    # ADMINISTRATION DJANGO
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),

    # ========================================================
    # AUTHENTIFICATION JWT
    # ========================================================

    path(
        "api/auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # ========================================================
    # API ELISABETH
    # ========================================================

    path(
        "api/",
        include("application_elisabeth.urls"),
    ),
]


# ============================================================
# FICHIERS MÉDIA EN DÉVELOPPEMENT
# ============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

