from rest_framework import serializers

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


class EquipmentCategoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCategory
        fields = '__all__'


class EquipmentCategoryPropertyAdminSerializer(serializers.ModelSerializer):
    _category = serializers.SlugRelatedField(read_only=True, slug_field='name', source='category')

    class Meta:
        model = EquipmentCategoryProperty
        fields = '__all__'


class EquipmentCategoryPropertyValueAdminSerializer(serializers.ModelSerializer):
    _property = serializers.SlugRelatedField(read_only=True, slug_field='name', source='property')

    class Meta:
        model = EquipmentCategoryPropertyValue
        fields = '__all__'


class OurEquipmentPropertyAdminSerializer(serializers.ModelSerializer):
    _property = serializers.SlugRelatedField(read_only=True, slug_field='name', source='property')
    _value = serializers.SlugRelatedField(read_only=True, slug_field='value', source='value')
    _equipment = serializers.SlugRelatedField(read_only=True, slug_field='name', source='equipment')

    class Meta:
        model = OurEquipmentProperty
        fields = '__all__'


class CompetitorsEquipmentPropertyAdminSerializer(serializers.ModelSerializer):
    _property = serializers.SlugRelatedField(read_only=True, slug_field='name', source='property')
    _value = serializers.SlugRelatedField(read_only=True, slug_field='value', source='value')
    _equipment = serializers.SlugRelatedField(read_only=True, slug_field='name', source='equipment')

    class Meta:
        model = CompetitorsEquipmentProperty
        fields = '__all__'


class EquipmentModelAdminSerializer(serializers.ModelSerializer):
    _category = serializers.SlugRelatedField(read_only=True, slug_field='name', source='category')

    class Meta:
        model = EquipmentModel
        fields = '__all__'


class EquipmentUnitAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentUnit
        fields = '__all__'


class OurEquipmentAdminSerializer(serializers.ModelSerializer):
    _category = serializers.SlugRelatedField(read_only=True, slug_field='name', source='category')
    _model = serializers.SlugRelatedField(read_only=True, slug_field='name', source='model')
    _unit = serializers.SlugRelatedField(read_only=True, slug_field='name', source='unit')

    class Meta:
        model = OurEquipment
        fields = '__all__'


class OurEquipmentImageAdminSerializer(serializers.ModelSerializer):
    _equipment = serializers.SlugRelatedField(read_only=True, slug_field='name', source='equipment')

    class Meta:
        model = OurEquipmentImage
        fields = '__all__'


class CompetitorAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competitor
        fields = '__all__'


class CompetitorsEquipmentAdminSerializer(serializers.ModelSerializer):
    _category = serializers.SlugRelatedField(read_only=True, slug_field='name', source='category')
    _unit = serializers.SlugRelatedField(read_only=True, slug_field='name', source='unit')

    class Meta:
        model = CompetitorsEquipment
        fields = '__all__'


class KeyWordAdminSerializer(serializers.ModelSerializer):
    _our_equipment = serializers.SlugRelatedField(read_only=True, slug_field='name', source='our_equipment')
    _comp_equipment = serializers.SlugRelatedField(read_only=True, slug_field='name', source='comp_equipment')

    class Meta:
        model = KeyWord
        fields = '__all__'


class SearchProcessAdminSerializer(serializers.ModelSerializer):
    _user = serializers.SlugRelatedField(read_only=True, slug_field='name', source='user')

    class Meta:
        model = SearchProcess
        fields = '__all__'


class SearchProcessResultAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchProcessResult
        fields = '__all__'
