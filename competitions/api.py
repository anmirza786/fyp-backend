from django.urls import path
from .views import CompetitionListApiView, SingleCompetitionRetrieveApiView, PublishedCompetitionListApiView

urlpatterns = [
    path('', CompetitionListApiView.as_view()),
    path('published-competitions', PublishedCompetitionListApiView.as_view()),
    path('<pk>', SingleCompetitionRetrieveApiView.as_view())
]
