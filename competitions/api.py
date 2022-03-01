from django.urls import path
from .views import CompetitionListApiView, SingleCompetitionRetrieveApiView


urlpatterns = [
    path('', CompetitionListApiView.as_view()),
    path('<pk>', SingleCompetitionRetrieveApiView.as_view())
]
