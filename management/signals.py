from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task, Milestone, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tasks import SendEmail

@receiver(post_save, sender=Task)
@receiver(post_save, sender=Milestone)
def create_notification(sender, instance, created, **kwargs):
    if created:
        if sender == Task:
            SendEmail.delay(instance.id, True)
            notification = Notification.objects.create(
                message=f"Task {instance.title} created", 
                user=instance.assigned_to
            )
        elif sender == Milestone:
            SendEmail.delay(instance.id, False)
            notification = Notification.objects.create(
                message=f"Milestone {instance.title} created", 
                user=instance.project.owner
            )        
        # Send notification to WebSocket group
        channel_layer = get_channel_layer()
        group_name = f"user_{notification.user.id}"
        print(group_name)
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                "message":notification.message,
                'user': notification.user.username if notification.user else None
            }
        )
