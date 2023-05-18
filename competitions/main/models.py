from django.contrib.auth.models import AbstractUser
from django.db import models


class Player(AbstractUser):
    unique_id = models.CharField(max_length=8, unique=True)
    photo = models.ImageField(upload_to='static/images/foto/', blank=True, null=True, default='static/images/no_foto.jpg')

    username = models.CharField("Username", unique=True, max_length=30, default="", null=False, blank=False)
    password = models.CharField("Password", max_length=128, default="", null=False, blank=False)
    password2 = models.CharField("Password", max_length=128, default="", null=False, blank=False)

    first_name = models.CharField("First name", max_length=50)
    last_name = models.CharField("Last name", max_length=50)
    email = models.EmailField("Email", unique=True, max_length=50, default="", null=False, blank=False)

    date_of_birth = models.DateField("Date of birth", null=True)
    country = models.CharField("Country", max_length=3)
    rating = models.IntegerField("Rating", default=1000)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Tournament(models.Model):
    unique_id = models.CharField(max_length=8, unique=True, default='')
    name = models.CharField("Name", max_length=30, null=False)
    place = models.CharField("Place", max_length=30, null=False)
    description = models.TextField("Description", null=True, blank=True)
    capacity = models.IntegerField("Capacity", null=False)
    date_of_start = models.DateTimeField("Start")
    date_of_end = models.DateTimeField("End")
    opened = models.BooleanField("Registration", default=True)
    players = models.ManyToManyField(Player, blank=True)
    organizers = models.ManyToManyField(Player, related_name='organized_tournaments')

    def __str__(self):
        return self.name


class Game(models.Model):
    players = models.ManyToManyField(Player)
    time = models.CharField("Time control", max_length=10)
    result = models.CharField("Result", max_length=10)
    date = models.DateTimeField("Start game")


class Result(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    point = models.FloatField("Points", default=0.0)
    tie_break1 = models.FloatField("Tie Break 1", default=0.0)
    tie_break2 = models.FloatField("Tie Break 1", default=0.0)
    tie_break3 = models.FloatField("Tie Break 1", default=0.0)
