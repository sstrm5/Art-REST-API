from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.guide.models import Card


@receiver(post_save, sender=Card)
def update_search_vector(sender, instance, **kwargs):
    Card.objects.filter(id=instance.id).update(
        search_vector=SearchVector("text", "title", "subject")
    )
