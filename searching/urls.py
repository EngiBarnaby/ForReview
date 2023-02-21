from rest_framework.routers import DefaultRouter

from .views.main_views import Recalculates
from .views.main_views import UploadData

from searching.views.admin_views import EquipmentCategoryAdminViewSet
from searching.views.admin_views import EquipmentCategoryPropertyAdminViewSet
from searching.views.admin_views import EquipmentCategoryPropertyValueAdminViewSet
from searching.views.admin_views import OurEquipmentPropertyAdminViewSet
from searching.views.admin_views import CompetitorsEquipmentPropertyAdminViewSet
from searching.views.admin_views import EquipmentModelAdminViewSet
from searching.views.admin_views import EquipmentUnitAdminViewSet
from searching.views.admin_views import OurEquipmentAdminViewSet
from searching.views.admin_views import OurEquipmentImageAdminViewSet
from searching.views.admin_views import CompetitorAdminViewSet
from searching.views.admin_views import CompetitorsEquipmentAdminViewSet
from searching.views.admin_views import KeyWordAdminViewSet
from searching.views.admin_views import SearchProcessAdminViewSet
from searching.views.admin_views import SearchProcessResultAdminViewSet

r = DefaultRouter()

# пользовательское приложение
r.register('recalculates', Recalculates)
r.register('upload_data', UploadData)

# админка
r.register('equipment_category', EquipmentCategoryAdminViewSet)
r.register('equipment_category_property', EquipmentCategoryPropertyAdminViewSet)
r.register('equipment_category_property_value', EquipmentCategoryPropertyValueAdminViewSet)
r.register('our_equipment_property', OurEquipmentPropertyAdminViewSet)
r.register('comp_equipment_property', CompetitorsEquipmentPropertyAdminViewSet)
r.register('equipment_model', EquipmentModelAdminViewSet)
r.register('equipment_unit', EquipmentUnitAdminViewSet)
r.register('our_equipment', OurEquipmentAdminViewSet)
r.register('our_equipment_img', OurEquipmentImageAdminViewSet)
r.register('competitor', CompetitorAdminViewSet)
r.register('competitor_equipment', CompetitorsEquipmentAdminViewSet)
r.register('keywords', KeyWordAdminViewSet)
r.register('search_processes', SearchProcessAdminViewSet)
r.register('search_process_results', SearchProcessResultAdminViewSet)

urlpatterns = r.urls
