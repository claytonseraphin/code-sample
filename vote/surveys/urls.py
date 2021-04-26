from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('survey', views.SurveyViewSet, 'survey')

app_name = 'survey'

urlpatterns = [
    path('', include(router.urls))
]
