import datetime

from django.db.models import Q
from django.db.models import Count
from django.db.models import Case
from django.db.models import When
from django.db.models import Value
from django.db.models import BooleanField
from django.conf import settings

from django.utils import timezone
from django.contrib.auth import get_user_model

from .exceptions import ActualSystemConfigNotFound
from .exceptions import InvalidImage

from .models import SystemConfig
from .models import Log

from searching.models import OurEquipment
from searching.models import KeyWord
from searching.models import CompetitorsEquipment


def date_range_list(start: datetime.date, end: datetime.date):
    """
    Принимает начало и конец периода и возвращает список дат,
    входящих в этот период, включая переданные даты
    """
    return [(start + datetime.timedelta(days=i)) for i in range((end - start).days + 1)]


class AnnotationService:
    @staticmethod
    def annotate_viewed_news(queryset, user):
        return queryset.annotate(
            user_in_saw_users_count=Count('saw_users', Q(saw_users__id=user.id)),
            viewed=Case(
                When(user_in_saw_users_count__gt=0, then=Value(True)), output_field=BooleanField(), default=Value(False)
            ))


class SystemConfigService:

    @staticmethod
    def get_actual(date: datetime.date = None):
        try:
            if date:
                config = SystemConfig.objects.filter(
                    start_date__day__gte=date.day,
                    start_date__month__gte=date.month,
                    start_date__year__gte=date.year
                ).order_by('start_date').first()
                if not config:
                    config = SystemConfig.objects.filter(
                        start_date__day__lte=date.day,
                        start_date__month__lte=date.month,
                        start_date__year__lte=date.year
                    ).order_by('-start_date').first()
                return config
            return SystemConfig.objects.get(is_actual=True)
        except SystemConfig.DoesNotExist:
            raise ActualSystemConfigNotFound

    @classmethod
    def get_version(cls):
        actual = cls.get_actual()
        return actual.version, actual.version_suffix


class ReviewService:
    @staticmethod
    def add_images(review, images):
        for img in images:
            size_mb = img.size / 1024 / 1024
            if size_mb > settings.MAX_REVIEW_IMG_SIZE_MB:
                raise InvalidImage('Размер загружаемых фотографий не должен превышать 5 Мб')
            ext = img.name.split('.')[-1]
            if ext not in ('png', 'jpg', 'jpeg',):
                raise InvalidImage('Загружаемые файлы должны иметь один из перечисленных форматов: .png, .jpg, .jpeg')
            review.reviewimg_set.create(img=img)


class LogService:
    @staticmethod
    def log(action: str = 'info', log: str = 'log', section: str = 'system', user=None, error: bool = False):
        try:
            config = SystemConfig.objects.get(is_actual=True)
            log = Log(
                action=action,
                log=log,
                section=section,
                user=user,
                static_user_id=str(user.id) if user else '',
                user_email=user.email if user else '',
                user_name=user.name if user else '',
                system_version=config.version,
                is_error=error
            )
            log.save()
        except SystemConfig.DoesNotExist:
            log = Log(
                action='write-log',
                log='Попытка записать лог активности. Актуальная версия конфигурации не определена!',
                section=section,
                user=user,
                static_user_id=str(user.id) if user else '',
                user_email=user.email if user else '',
                user_name=user.name if user else '',
                system_version='none',
                is_error=True
            )
            log.save()
        finally:
            log = Log(
                action='write-log',
                log='Попытка записать лог активности. Неизвестная ошибка!',
                section=section,
                user=user,
                static_user_id=str(user.id) if user else '',
                user_email=user.email if user else '',
                user_name=user.name if user else '',
                system_version='none',
                is_error=True
            )
            log.save()


class ApplicationStatisticService:

    @staticmethod
    def get_summary():
        user_model = get_user_model()
        config = SystemConfigService.get_actual()
        return {
            'actual_version': config.version,
            'active_users_count': user_model.objects.filter(is_active=True).count(),
            'all_users_count': user_model.objects.count(),
            'new_users_since_last_release': Log.objects.filter(system_version=config.version,
                                                               action='new-user-register').count(),
            'partners_count': user_model.objects.filter(is_active=True).exclude(email__endswith='iek.ru').exclude(
                email__endswith='tcr.ru').count(),
            'our_equipment_count': OurEquipment.objects.count(),
            'our_equipment_wo_analogs_count': OurEquipment.objects.annotate(
                keys_count=Count('keywords')).filter(keys_count=0).count(),
            'comp_equipment_count': CompetitorsEquipment.objects.count(),
            'comp_equipment_wo_analogs_count': CompetitorsEquipment.objects.annotate(
                keys_count=Count('keywords')).filter(keys_count=0).count(),
            'keywords_count': KeyWord.objects.count()
        }

    @staticmethod
    def get_success_recalculate_rows_chart(start: datetime.date, end: datetime.date):
        """
        Принимает дату начала и окончания промежутка, за который необходимо собрать данные
        и возвращает генератор объектов dict:
            ...
            {
                'date': '01.02.2003',       <-- дата на графике
                'count': 123,               <-- кол-во успешно подобранных строк
                'version': 1.2.3            <-- актуальная версия на момент даты
            },
            ...
        """

        for date in date_range_list(start, end):
            config = SystemConfigService.get_actual(date)
            yield {
                'date': date.strftime('%d.%m.%Y'),
                'count': Log.objects.filter(
                    action='success-recalculate-row',
                    system_version__contains=config.version if config else '',
                    created__day=date.day,
                    created__month=date.month,
                    created__year=date.year
                ).count(),
                'version': config.version if config else None
            }

    @staticmethod
    def get_recalculates_requests_chart(start: datetime.date, end: datetime.date):
        """
        Принимает дату начала и окончания промежутка, за который необходимо собрать данные
        и возвращает генератор объектов dict:
            ...
            {
                'date': '01.02.2003',       <-- дата на графике
                'count': 123,               <-- кол-во запросов на пересчет
                'version': 1.2.3            <-- актуальная версия на момент даты
            },
            ...
        """
        for date in date_range_list(start, end):
            config = SystemConfigService.get_actual(date)
            yield {
                'date': date.strftime('%d.%m.%Y'),
                'count': Log.objects.filter(
                    action='request-to-recalculate',
                    system_version__contains=config.version if config else '',
                    created__day=date.day,
                    created__month=date.month,
                    created__year=date.year
                ).count(),
                'version': config.version if config else None
            }

    @staticmethod
    def get_active_users_per_day_chart(start, end):
        """
        Принимает дату начала и окончания промежутка, за который необходимо собрать данные
        и возвращает генератор объектов dict:
            ...
            {
                'date': '01.02.2003',       <-- дата на графике
                'count': 123,               <-- кол-во пользователей, отправивших хоть один запрос на пересчет
                'version': 1.2.3            <-- актуальная версия на момент даты
            },
            ...
        """
        for date in date_range_list(start, end):
            config = SystemConfigService.get_actual(date)
            yield {
                'date': date.strftime('%d.%m.%Y'),
                'count': Log.objects.filter(
                    action='request-to-recalculate',
                    system_version__contains=config.version if config else '',
                    created__day=date.day,
                    created__month=date.month,
                    created__year=date.year
                ).distinct('static_user_id').count(),
                'version': config.version if config else None
            }
