from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from .models import Task, Milestone
from accounts.models import User

@shared_task
def SendEmail(id, is_task):
    if is_task:
        task = Task.objects.get(id=id)
        subject = 'Task created'
        message = f"A new task assigned to you in {task.title} by {task.project.owner}"
        recipient_list = [task.assigned_to.email, ]
    else:
        milestone = Milestone.objects.get(id=id)
        subject = 'Milestone created'
        message = f"A new milestone created by {milestone.project.owner} in {milestone.title}"
        tasks = Task.objects.filter(project=milestone.project)      
        recipient_list = [task.assigned_to.email for task in tasks] 
        recipient_list.append(milestone.project.owner.email)
    print(recipient_list)
    email_from = settings.EMAIL_HOST_USER
    send_mail( subject, message, email_from, recipient_list )