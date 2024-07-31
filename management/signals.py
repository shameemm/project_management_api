from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Milestone,Notification
from .tasks import SendEmail

@receiver(post_save, sender=Task)
@receiver(post_save, sender=Milestone)
def create_notification(sender, instance, created, **kwargs):
    if created:
        if sender == Task:
            SendEmail.delay(instance.id, True)
            Notification.objects.create(message=f"Task {instance.title} created", user=instance.assigned_to)
        if sender == Milestone:
            SendEmail.delay(instance.id, False)
            Notification.objects.create(message=f"Milestone {instance.title} created", user=instance.project.owner)
        