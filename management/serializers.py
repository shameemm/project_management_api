from rest_framework import serializers
from .models import Project,Task, Milestone,Notification

class ProjectSerializer(serializers.ModelSerializer):
    read_only_fields = ['id']
    class Meta:
        model = Project
        fields = ['id','name','description','start_date','end_date','status','owner']
        
    def validate_owner(self, value):
        if value and value.role != 'manager':
            raise serializers.ValidationError("Only users with the 'manager' role can be assigned as the owner.")
        return value
        
        
class TaskSerializer(serializers.ModelSerializer):
    read_only_fields = ['id']
    class Meta:
        model = Task
        fields = ['id','title','description','project','assigned_to','status','due_date']
        
    def validate_assigned_to(self, value):
        if value and value.role != 'member':
            raise serializers.ValidationError("Only users with the 'member' role can be assigned as the assigned_to.")
        return value
        
class MilestoneSerializer(serializers.ModelSerializer):
    read_only_fields = ['id']
    class Meta:
        model = Milestone
        fields = ['id','title','description','project','due_date','achieved_on']
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['message','user']
        
