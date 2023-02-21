import datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from application_info.models import Log
from application_info.services import ApplicationStatisticService


class ApplicationStatistic(viewsets.GenericViewSet):
    queryset = Log.objects.all()
    service_class = ApplicationStatisticService
    permission_classes = (IsAdminUser,)

    @action(methods=('get',), detail=False)
    def summary(self, request):
        return Response(self.service_class.get_summary())

    @action(methods=('get',), detail=False)
    def success_recalculate_rows_chart(self, request):
        start = datetime.datetime.strptime(request.query_params.get('start'), '%d.%m.%Y')
        end = datetime.datetime.strptime(request.query_params.get('end'), '%d.%m.%Y')
        return Response(self.service_class.get_success_recalculate_rows_chart(start, end))

    @action(methods=('get',), detail=False)
    def recalculates_requests_chart(self, request):
        start = datetime.datetime.strptime(request.query_params.get('start'), '%d.%m.%Y')
        end = datetime.datetime.strptime(request.query_params.get('end'), '%d.%m.%Y')
        return Response(self.service_class.get_recalculates_requests_chart(start, end))

    @action(methods=('get',), detail=False)
    def active_users_per_day_chart(self, request):
        start = datetime.datetime.strptime(request.query_params.get('start'), '%d.%m.%Y')
        end = datetime.datetime.strptime(request.query_params.get('end'), '%d.%m.%Y')
        return Response(self.service_class.get_active_users_per_day_chart(start, end))
