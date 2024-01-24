from django.conf import settings
from django.db import models


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performance")
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE, related_name="performance")
    show_time = models.DateTimeField()
    actor = models.ManyToManyField("Actor", related_name="performance")
    genre = models.ManyToManyField("Genre", related_name="performance")

    def __str__(self):
        return f"{self.play.title} {self.show_time}"

    class Meta:
        ordering = ['-show_time']


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return (f"{str(self.performance)} "
                f"(row: {self.row}, seat: {self.seat})")

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")

    def __str__(self):
        return self.created_at