from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
class Make(models.Model):
    name = models.CharField(
        max_length=100,
        help_text = 'Enter a make (e.g. Dodge)',
        validators=[MinLengthValidator(2,"Make must be greater than 1 character")]
    )
    def __str__(self):
        return self.name

class Auto(models.Model):
    nickname = models.CharField(
        max_length=50, validators=[MinLengthValidator(2,"Nickname must be greater than 1 character")]
    )
    mileage = models.PositiveIntegerField()
    comments = models.CharField(max_length=300)
    make = models.ForeignKey('Make', on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname