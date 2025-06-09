from django.db import models
from django.db.models import Count


class GenreQuerySet(models.QuerySet):
    def top_reviewed_by_user(self, user, limit=5):
        return (
            self.filter(movies__reviews__user=user)
            .annotate(review_count=Count("movies__reviews"))
            .order_by("-review_count")[:limit]
        )


class Genre(models.Model):
    objects = GenreQuerySet.as_manager()

    class Meta:
        db_table = "genre"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
