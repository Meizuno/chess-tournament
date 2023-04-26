from django.db import models


class Player(models.Model):
    username = models.CharField("Username", max_length=20, default="", null=False, blank=False)
    password = models.CharField("Password", max_length=128, default="", null=False, blank=False)

    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last name", max_length=50)
    email = models.EmailField("Email", max_length=50, default="", null=False, blank=False)

    date_of_birth = models.DateField("Date of birth")
    gender = models.CharField("Gender", max_length=6, choices=(('male', 'male'), ('female', 'female')))
    country = models.CharField("Country", max_length=20)
    rating = models.IntegerField("Rating", default=1000)

