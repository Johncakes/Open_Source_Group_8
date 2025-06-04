import random

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from movie.models import Movie


class Review(models.Model):
    class Meta:
        db_table = "review"
        constraints = [
            models.UniqueConstraint(fields=["movie", "user"], name="unique_user_review_per_movie")
        ]

    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    username = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.rating}점"

    def clean(self):
        if not self.content.strip():
            raise ValidationError("리뷰 내용을 입력해주세요.")

        if not (0 <= self.rating <= 5):
            raise ValidationError("별점은 0점 이상 5점 이하여야 합니다.")

        if (self.rating * 2) % 1 != 0:
            raise ValidationError("별점은 0.5 단위로 입력해주세요.")

    @classmethod
    def generate_anonymous_review(
        cls,
        movie: Movie,
        user: User | None,
        content: str,
        rating: float,
    ) -> "Review":
        return cls(
            movie=movie,
            user=user,
            username=cls.generate_random_username(),
            content=content,
            rating=rating,
        )

    @staticmethod
    def generate_random_username() -> str:
        random_suffix = random.randint(1000, 9999)

        return f"익명{random_suffix}"
