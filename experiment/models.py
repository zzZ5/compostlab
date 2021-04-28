from django.db.models.fields.related import OneToOneField
from equipment.models import Equipment

from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):

    reply = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='%(class)s')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply

    class Meta:
        db_table = "experiment_review"
        ordering = ["-created_time"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class Experiment(models.Model):

    name = models.CharField(max_length=128, unique=True)
    site = models.CharField(max_length=128, unique=True)
    descript = models.CharField(max_length=256, null=True)
    equipments = models.ManyToManyField(Equipment, related_name='%(class)s')
    begin_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    users = models.ManyToManyField(
        User,  related_name='%(class)s_use')
    owner = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_own')

    FAILED = 0
    DOING = 1
    DONE = 2
    APPLYING = 3
    STATUS_CHOICE = (
        (FAILED, "Failed"),
        (DOING, "Doing"),
        (DONE, "Done"),
        (APPLYING, "Applying")
    )
    status = models.IntegerField(choices=STATUS_CHOICE, default=APPLYING)

    review = OneToOneField(
        Review, null=True, on_delete=models.CASCADE, related_name='%(class)s')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "experiment"
        ordering = ["-created_time"]
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"
