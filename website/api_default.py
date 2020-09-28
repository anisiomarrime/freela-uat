from rest_framework import routers
from mozlancers import api_default_views

router = routers.DefaultRouter()

router.register(r'skills', api_default_views.SkillViewset)

router.register(r'cities', api_default_views.CityViewset)

router.register(r'packages', api_default_views.PackageViewset)

router.register(r'categories', api_default_views.CategoryViewset)

router.register(r'status', api_default_views.StatusViewset)