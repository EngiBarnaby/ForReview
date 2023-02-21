from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from searching.services import SearchService
from searching.services import UploadDatafileService
from searching.serializers.main_serializers import SearchRequestSerializer

from searching.models import SearchProcess


class Recalculates(viewsets.GenericViewSet):
    queryset = SearchProcess.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SearchRequestSerializer
    service = SearchService

    @action(methods=('post',), detail=False)
    def prepare(self, request):
        try:
            return Response(self.service.get_prepare_data(request.FILES['file']))
        except KeyError:
            return Response({'detail': 'Выберите файл сметы'}, 400)
        except (ValueError, AttributeError,):
            return Response(
                {'detail': 'Загруженный файл не является валидным файлом сметы. Попробуйте скачать новый шаблон'}, 400)

    @action(methods=('post',), detail=False)
    def search(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        prc = self.queryset.create(user=request.user, psp=data.get('psp'))
        return Response(self.service.do_recalculate(data.get('rows'), prc, data.get('ex_mdls')))

    @action(methods=('get',), detail=False)
    def download(self, request):
        response = self.service.get_file_response(self.service.get_file(request.data), request.user.email, 30)
        return Response(response)

    @action(methods=('post',), detail=True)
    def interrupt(self, request, pk=None):
        self.get_object().interrupt()
        return Response({'detail': 'Процесс поиска остановлен'})


class UploadData(viewsets.ViewSet):
    service = UploadDatafileService
    permission_classes = (IsAdminUser,)

    @action(methods=('post',), detail=False)
    def upload_our_equipment(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = self.service.upload_our_equipment(datafile)
        return Response(
            {'detail': f'Загружено {valid} позиций. Данные об оборудовании успешно обновлены', 'invalid': invalid}, 200)

    @action(methods=('post',), detail=False)
    def upload_comp_equipment(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = self.service.upload_comp_equipment(datafile)
        return Response({'detail': f'Загружено {valid} позиций. Данные об оборудовании конкурентов успешно обновлены',
                         'invalid': invalid}, 200)

    @action(methods=('post',), detail=False)
    def upload_keywords(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = self.service.upload_keywords(datafile)
        return Response({'detail': 'Данные об аналогах успешно обновлены', 'invalid': invalid}, 200)

    @action(methods=('post',), detail=False)
    def upload_equipment_categories(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = self.service.upload_equipment_categories(datafile)
        return Response({'detail': 'Данные о категориях оборудования успешно обновлены', 'invalid': invalid}, 200)
