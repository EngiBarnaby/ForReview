import os

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class EquipmentCategory(models.Model):
    """
    Категория оборудования.
    """
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']


class EquipmentCategoryProperty(models.Model):
    category = models.ForeignKey('searching.EquipmentCategory', on_delete=models.CASCADE,
                                 related_name='properties')
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']


class EquipmentCategoryPropertyValue(models.Model):
    property = models.ForeignKey('searching.EquipmentCategoryProperty', on_delete=models.CASCADE,
                                 related_name='values')
    value = models.CharField(max_length=250)

    class Meta:
        ordering = ['property']


class OurEquipmentProperty(models.Model):
    equipment = models.ForeignKey('searching.OurEquipment', related_name="properties", on_delete=models.CASCADE)
    property = models.ForeignKey('searching.EquipmentCategoryProperty', on_delete=models.CASCADE,
                                 related_name='our_equipment_properties')
    value = models.ForeignKey('searching.EquipmentCategoryPropertyValue', on_delete=models.SET_NULL, null=True,
                              default=None, related_name='our_equipment_values')

    class Meta:
        unique_together = ['equipment', 'property', 'value']
        ordering = ['equipment']


class CompetitorsEquipmentProperty(models.Model):
    equipment = models.ForeignKey('searching.CompetitorsEquipment', related_name="properties", on_delete=models.CASCADE)
    property = models.ForeignKey('searching.EquipmentCategoryProperty', on_delete=models.CASCADE,
                                 related_name='comp_equipment_properties')
    value = models.ForeignKey('searching.EquipmentCategoryPropertyValue', on_delete=models.SET_NULL, null=True,
                              default=None,
                              related_name='comp_equipment_values')

    class Meta:
        unique_together = ['equipment', 'property', 'value']
        ordering = ['property']


class EquipmentModel(models.Model):
    """
    Линейка оборудования.
    """
    category = models.ForeignKey('searching.EquipmentCategory', on_delete=models.CASCADE,
                                 related_name='equipment_models')
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']


class EquipmentUnit(models.Model):
    name = models.CharField(max_length=30)


class OurEquipment(models.Model):
    """
    Оборудование ITK/IEK.
    """
    category = models.ForeignKey('searching.EquipmentCategory', on_delete=models.SET_NULL, related_name='our_equipment',
                                 blank=True, null=True, default=None)
    model = models.ForeignKey('searching.EquipmentModel', on_delete=models.SET_NULL, related_name='equipment',
                              blank=True, null=True, default=None)
    unit = models.ForeignKey('searching.EquipmentUnit', on_delete=models.SET_NULL, null=True, default=None)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, unique=True, db_index=True)
    cost = models.DecimalField(decimal_places=2, max_digits=9, blank=True, default=0)
    count = models.IntegerField(default=0, blank=True)
    comment = models.TextField(default='', null=True)
    is_promotion = models.BooleanField(default=False)
    is_not_actual = models.BooleanField(default=False)
    promotion_description = models.TextField(default='', null=True, blank=True)

    class Meta:
        ordering = ['name']


class OurEquipmentImage(models.Model):
    """
    Фотография оборудования ITK/IEK
    """

    def img_upload(self, filename):
        return os.path.join('our_equipment', str(self.equipment.code), filename)

    img = models.ImageField(upload_to=img_upload, null=True, default=None)
    equipment = models.ForeignKey('searching.OurEquipment', related_name="images", on_delete=models.CASCADE)


class Competitor(models.Model):
    """
    Конкурент
    """
    name = models.CharField(max_length=250)

    class Meta:
        ordering = ['name']


class CompetitorsEquipment(models.Model):
    """
    Оборудование конкурента
    """
    competitor = models.ForeignKey('searching.Competitor', on_delete=models.SET_NULL, related_name='equipment',
                                   blank=True, null=True, default=None)
    category = models.ForeignKey('searching.EquipmentCategory', on_delete=models.SET_NULL,
                                 related_name='comp_equipment', blank=True, null=True, default=None)
    unit = models.ForeignKey('searching.EquipmentUnit', on_delete=models.SET_NULL, null=True, default=None, blank=True)
    name = models.CharField(max_length=250, blank=True)
    code = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ['name']
        unique_together = ['competitor', 'code']


class KeyWord(models.Model):
    """
    Поисковой ключ
    """
    keyword = models.TextField()
    our_equipment = models.ForeignKey('searching.OurEquipment', related_name="keywords", on_delete=models.SET_NULL,
                                      null=True, default=None)
    comp_equipment = models.ForeignKey('searching.CompetitorsEquipment', related_name="keywords",
                                       on_delete=models.SET_NULL, null=True, default=None)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['keyword']


class SearchProcess(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(default=None, null=True)
    psp = models.IntegerField(default=80)  # Properties Similarity Percentage
    is_active = models.BooleanField(default=True)
    is_success = models.BooleanField(default=False)
    is_error = models.BooleanField(default=False)
    is_interrupted = models.BooleanField(default=False)
    rows_count = models.IntegerField(default=0)
    match_rows_count = models.IntegerField(default=0)
    unmatch_rows_count = models.IntegerField(default=0)
    skip_rows_count = models.IntegerField(default=0)
    error_detail = models.TextField(blank=True)

    def success(self):
        self.end = timezone.localtime(timezone.now())
        self.is_active = False
        self.is_success = True
        self.save()

    def error(self, detail: str = ''):
        self.end = timezone.localtime(timezone.now())
        self.is_active = False
        self.is_error = True
        self.error_detail = detail
        self.save()

    def interrupt(self):
        self.end = timezone.localtime(timezone.now())
        self.is_active = False
        self.is_interrupted = True
        self.save()

    def remtime(self):
        """
        Возвращает прогнозируемое оставшееся время до окончания пересчета в секундах
        """
        return int(self.rows_count - self.match_rows_count - self.skip_rows_count - self.unmatch_rows_count * 0.1)

    class Meta:
        ordering = ['-start']


class SearchProcessResult(models.Model):
    process = models.ForeignKey('searching.SearchProcess', on_delete=models.CASCADE, related_name='results')
    input_code = models.TextField(blank=True)
    input_name = models.TextField(blank=True)
    output_code = models.TextField(blank=True)
    output_name = models.TextField(blank=True)
    is_match = models.BooleanField(default=False)
    is_unmatch = models.BooleanField(default=False)
    is_skip = models.BooleanField(default=False)
    match_in_own_codes = models.BooleanField(default=False)
    match_in_own_names = models.BooleanField(default=False)
    match_in_comp_codes = models.BooleanField(default=False)
    match_in_comp_names = models.BooleanField(default=False)
    match_in_keys = models.BooleanField(default=False)
    match_by_properties = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
