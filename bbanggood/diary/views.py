from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from .models import BreadDiary
from .serializers import BreadDiarySerializer
from django.utils.dateparse import parse_date

class BreadDiaryViewSet(viewsets.ModelViewSet):
    queryset = BreadDiary.objects.all().order_by('-date')
    serializer_class = BreadDiarySerializer

    @action(detail=False, methods=['get'])
    def by_date(self, request, *args, **kwargs):
        date_param = request.query_params.get('date')
        if date_param:
            try:
                date = parse_date(date_param)
                if date is None:
                    raise NotFound("Invalid date format")
                queryset = self.queryset.filter(date=date)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                raise NotFound("Invalid date format")
        return Response({"detail": "Date parameter is required"}, status=400)

    @action(detail=True, methods=['get'])
    def detail(self, request, *args, **kwargs):
        diary = self.get_object()
        serializer = self.get_serializer(diary)
        return Response(serializer.data)
