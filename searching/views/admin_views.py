import os

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from searching.models import EquipmentCategory
from searching.models import EquipmentCategoryProperty
from searching.models import EquipmentCategoryPropertyValue
from searching.models import OurEquipmentProperty
from searching.models import CompetitorsEquipmentProperty
from searching.models import EquipmentModel
from searching.models import EquipmentUnit
from searching.models import OurEquipment
from searching.models import OurEquipmentImage
from searching.models import Competitor
from searching.models import CompetitorsEquipment
from searching.models import KeyWord
from searching.models import SearchProcess
from searching.models import SearchProcessResult

from searching.serializers.admin_serializers import EquipmentCategoryAdminSerializer
from searching.serializers.admin_serializers import EquipmentCategoryPropertyAdminSerializer
from searching.serializers.admin_serializers import EquipmentCategoryPropertyValueAdminSerializer
from searching.serializers.admin_serializers import OurEquipmentPropertyAdminSerializer
from searching.serializers.admin_serializers import CompetitorsEquipmentPropertyAdminSerializer
from searching.serializers.admin_serializers import EquipmentModelAdminSerializer
from searching.serializers.admin_serializers import EquipmentUnitAdminSerializer
from searching.serializers.admin_serializers import OurEquipmentAdminSerializer
from searching.serializers.admin_serializers import OurEquipmentImageAdminSerializer
from searching.serializers.admin_serializers import CompetitorAdminSerializer
from searching.serializers.admin_serializers import CompetitorsEquipmentAdminSerializer
from searching.serializers.admin_serializers import KeyWordAdminSerializer
from searching.serializers.admin_serializers import SearchProcessAdminSerializer
from searching.serializers.admin_serializers import SearchProcessResultAdminSerializer

from searching.services import UploadDatafileService
from searching.services import DownloadDatafileService


class EquipmentCategoryAdminViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategory.objects.all()
    serializer_class = EquipmentCategoryAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)

    @action(methods=('get',), detail=False)
    def download(self, request):
        path = DownloadDatafileService.create_category_datafile(self.filter_queryset(self.get_queryset()))
        response = DownloadDatafileService.get_file_response(path, path.split(os.sep)[-1], 30)
        return response

    @action(methods=('post',), detail=False)
    def upload(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = UploadDatafileService.upload_equipment_categories(datafile)
        return Response({'detail': 'Данные о категориях оборудования успешно обновлены', 'invalid': invalid}, 200)


class EquipmentCategoryPropertyAdminViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategoryProperty.objects.all()
    serializer_class = EquipmentCategoryPropertyAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('name', 'category',)
    search_fields = ('name',)
    ordering_fields = ('name', 'category__name',)


class EquipmentCategoryPropertyValueAdminViewSet(viewsets.ModelViewSet):
    queryset = EquipmentCategoryPropertyValue.objects.all()
    serializer_class = EquipmentCategoryPropertyValueAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('value', 'property',)
    search_fields = ('value',)
    ordering_fields = ('value', 'property__name',)


class OurEquipmentPropertyAdminViewSet(viewsets.ModelViewSet):
    queryset = OurEquipmentProperty.objects.all()
    serializer_class = OurEquipmentPropertyAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('equipment', 'property', 'value',)
    search_fields = ('equipment__name', 'equipment__code', 'property__name', 'value__value',)
    ordering_fields = ('equipment__name', 'property__name', 'value__value',)


class CompetitorsEquipmentPropertyAdminViewSet(viewsets.ModelViewSet):
    queryset = CompetitorsEquipmentProperty.objects.all()
    serializer_class = CompetitorsEquipmentPropertyAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('equipment', 'property', 'value',)
    search_fields = ('equipment__name', 'equipment__code', 'property__name', 'value__value',)
    ordering_fields = ('equipment__name', 'property__name', 'value__value',)


class EquipmentModelAdminViewSet(viewsets.ModelViewSet):
    queryset = EquipmentModel.objects.all()
    serializer_class = EquipmentModelAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('name', 'category',)
    search_fields = ('name',)
    ordering_fields = ('category__name', 'name',)


class EquipmentUnitAdminViewSet(viewsets.ModelViewSet):
    queryset = EquipmentUnit.objects.all()
    serializer_class = EquipmentUnitAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)


class OurEquipmentAdminViewSet(viewsets.ModelViewSet):
    queryset = OurEquipment.objects.all()
    serializer_class = OurEquipmentAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('category', 'model', 'name', 'cost', 'count', 'is_promotion', 'is_not_actual', 'unit',)
    search_fields = ('category__name', 'model__name', 'name', 'code', 'comment', 'promotion_description', 'unit__name',)
    ordering_fields = (
        'category__name', 'model__name', 'name', 'code', 'cost', 'count', 'comment', 'is_promotion', 'is_not_actual',
        'promotion_description', 'unit__name',
    )

    @action(methods=('get',), detail=False)
    def download(self, request):
        path = DownloadDatafileService.create_our_equipment_datafile(self.filter_queryset(self.get_queryset()))
        response = DownloadDatafileService.get_file_response(path, path.split(os.sep)[-1], 30)
        return response

    @action(methods=('post',), detail=False)
    def upload(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = UploadDatafileService.upload_our_equipment(datafile)
        return Response(
            {'detail': f'Загружено {valid} позиций. Данные об оборудовании успешно обновлены', 'invalid': invalid}, 200)


class OurEquipmentImageAdminViewSet(viewsets.ModelViewSet):
    queryset = OurEquipmentImage.objects.all()
    serializer_class = OurEquipmentImageAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('equipment',)
    search_fields = ('equipment__name', 'equipment__code',)
    ordering_fields = ('equipment__name',)


class CompetitorAdminViewSet(viewsets.ModelViewSet):
    queryset = Competitor.objects.all()
    serializer_class = CompetitorAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('name',)
    search_fields = ('name',)
    ordering_fields = ('name',)


class CompetitorsEquipmentAdminViewSet(viewsets.ModelViewSet):
    queryset = CompetitorsEquipment.objects.all()
    serializer_class = CompetitorsEquipmentAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('competitor', 'category', 'unit', 'name', 'code',)
    search_fields = ('competitor__name', 'category__name', 'unit__name', 'name', 'code',)
    ordering_fields = ('competitor__name', 'category__name', 'unit__name', 'name', 'code',)

    @action(methods=('get',), detail=False)
    def download(self, request):
        path = DownloadDatafileService.create_comp_equipment_datafile(self.filter_queryset(self.get_queryset()))
        response = DownloadDatafileService.get_file_response(path, path.split(os.sep)[-1], 30)
        return response

    @action(methods=('post',), detail=False)
    def upload(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = UploadDatafileService.upload_comp_equipment(datafile)
        return Response({'detail': f'Загружено {valid} позиций. Данные об оборудовании конкурентов успешно обновлены',
                         'invalid': invalid}, 200)


class KeyWordAdminViewSet(viewsets.ModelViewSet):
    queryset = KeyWord.objects.all()
    serializer_class = KeyWordAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('keyword', 'out_equipment', 'comp_equipment', 'is_approved',)
    search_fields = (
        'keyword', 'our_equipment__name', 'our_equipment__code', 'comp_equipment__name', 'comp_equipment__code',
    )
    ordering_fields = ('keyword', 'our_equipment__name', 'comp_equipment__name', 'is_approved',)

    @action(methods=('get',), detail=False)
    def download(self, request):
        path = DownloadDatafileService.create_kwds_datafile(self.filter_queryset(self.get_queryset()))
        response = DownloadDatafileService.get_file_response(path, path.split(os.sep)[-1], 30)
        return response

    @action(methods=('post',), detail=False)
    def upload(self, request):
        datafile = request.FILES.get('file')
        invalid, valid = UploadDatafileService.upload_keywords(datafile)
        return Response({'detail': 'Данные об аналогах успешно обновлены', 'invalid': invalid}, 200)


class SearchProcessAdminViewSet(viewsets.ModelViewSet):
    queryset = SearchProcess.objects.all()
    serializer_class = SearchProcessAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = ('user', 'psp', 'is_active', 'is_success', 'is_error', 'is_interrupted',)
    search_fields = ('user__name', 'user__email', 'error_detail',)
    ordering_fields = (
        'user__name', 'user__email', 'start', 'end', 'psp', 'is_active', 'is_success', 'is_error', 'is_interrupted',
        'rows_count', 'match_rows_count', 'unmatch_rows_count', 'skip_rows_count', 'error_detail',
    )


class SearchProcessResultAdminViewSet(viewsets.ModelViewSet):
    queryset = SearchProcessResult.objects.all()
    serializer_class = SearchProcessResultAdminSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    permission_classes = (IsAdminUser,)
    filterset_fields = (
        'process', 'input_code', 'input_name', 'output_code', 'output_name', 'is_match', 'is_unmatch', 'is_skip',
        'match_in_own_codes', 'match_in_own_names', 'match_in_comp_codes', 'match_in_comp_names', 'match_in_keys',
        'match_by_properties'
    )
    search_fields = ('input_code', 'input_name', 'output_code', 'output_name',)
    ordering_fields = (
        'process', 'input_code', 'input_name', 'output_code', 'output_name', 'is_match', 'is_unmatch', 'is_skip',
        'match_in_own_codes', 'match_in_own_names', 'match_in_comp_codes', 'match_in_comp_names', 'match_in_keys',
        'match_by_properties',
    )
