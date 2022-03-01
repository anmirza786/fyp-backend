from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions

from competitions.models import Competition, MoveSectionEnum
from competitions.serializers import CompetitionSerializers
# Create your views here.


class CompetitionListApiView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CompetitionSerializers

    def get_queryset(self):
        return Competition.objects.filter(
            move_section=MoveSectionEnum.ONLINEINCOMPETITION).order_by('-id')


class SingleCompetitionRetrieveApiView(RetrieveAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CompetitionSerializers

    def get_queryset(self):
        return Competition.objects.all()
