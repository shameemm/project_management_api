from .models import Project, Task, Milestone, Notification
from .serializers import ProjectSerializer, TaskSerializer, MilestoneSerializer, NotificationSerializer
from accounts.permissions import IsAdminOrManager
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

# Create your views here.

class ProjectListViewSet(ReadOnlyModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Project.objects.all()
        else:
            return Project.objects.filter(owner=self.request.user)
    
class ProjectViewSet(ModelViewSet):
    http_method_names = ['put', 'post','patch','delete']
    permission_classes = [IsAdminOrManager]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
class TaskListViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = TaskSerializer
    filterset_fields = ['project']
    
    def get_queryset(self):
        if self.request.user.role =='admin':
            return Task.objects.all()
        elif self.request.user.role == 'manager':
            return Task.objects.filter(project__owner=self.request.user)
        else:
            return Task.objects.filter(assigned_to=self.request.user)
    
class TaskViewSet(ModelViewSet):
    http_method_names = ['put', 'post','patch','delete']
    permission_classes = [IsAdminOrManager]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
class MileStoneListViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project']
    
class MilestoneViewSet(ModelViewSet):
    http_method_names = ['put', 'post','patch','delete']
    permission_classes = [IsAdminOrManager]
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    
class NotificationViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)

    

    
    
        

    