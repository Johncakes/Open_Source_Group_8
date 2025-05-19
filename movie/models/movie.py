from django.db import models

from movie.models import Genre


class Movie(models.Model):
    class Meta:
        db_table = "movie"

    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, db_index=True)
    original_title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.PositiveIntegerField(null=True, blank=True)
    popularity = models.FloatField(default=0)
    origin_country = models.CharField(max_length=10, blank=True)
    production_company = models.CharField(max_length=100, blank=True)

    genres = models.ManyToManyField(Genre, related_name="movies")

    def __str__(self):
        return self.title


class MovieCast(models.Model):
    class Meta:
        db_table = "cast"

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="casts")
    name = models.CharField(max_length=100)
    character = models.CharField(max_length=100, blank=True)
    profile_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} as {self.character}"


class MovieCrew(models.Model):
    class Meta:
        db_table = "crew"

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="crews")
    name = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.job})"
