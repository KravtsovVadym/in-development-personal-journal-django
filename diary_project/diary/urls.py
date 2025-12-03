from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, EntryViewSet

router = DefaultRouter()

router.register(r"entry", EntryViewSet, basename="entry")
router.register(r"tag", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls))
]
