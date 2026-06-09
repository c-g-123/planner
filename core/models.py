from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Tag(models.Model):

    class Colour(models.TextChoices):

        RED = "RED", "Red"
        GREEN = "GREEN", "Green"
        BLUE = "BLUE", "Blue"

    MAX_NAME_LENGTH = 20

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    colour = models.CharField(choices=Colour.choices, default=Colour.RED)

    def __str__(self):
        return self.name

class Item(models.Model):

    MAX_NAME_LENGTH = 20
    MAX_DESCRIPTION_LENGTH = 200

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    description = models.TextField(max_length=MAX_DESCRIPTION_LENGTH, blank=True)
    is_complete = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        Tag,
        related_name="items",
        blank=True,
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.end_datetime < self.start_datetime:
            raise ValidationError("The end datetime cannot be less than the start datetime.")

    def __str__(self):
        return self.name
