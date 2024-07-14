from django.contrib import admin
from django.urls import path, include
from .views import robots_txt

urlpatterns = [
    path("", include("explorer.urls")),
    path("admin/", admin.site.urls),
    path('robots.txt', robots_txt),
]
