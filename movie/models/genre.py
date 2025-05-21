from django.db import models


class Genre(models.Model):
    class Meta:
        db_table = "genre"

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
