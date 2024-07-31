from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'list', ProjectListViewSet, basename='project')
router.register(r'cud', ProjectViewSet, basename='createproject')

router.register(r'task/list', TaskListViewSet, basename='task')
router.register(r'task/cud', TaskViewSet, basename='createtask')

router.register(r'milestone/list', MileStoneListViewSet, basename='milestone')
router.register(r'milestone/cud', MilestoneViewSet, basename='createmilestone') 

urlpatterns = router.urls