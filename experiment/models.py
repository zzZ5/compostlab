from django.db.models.fields.related import OneToOneField
from equipment.models import Equipment

from django.contrib.auth.models import User
from django.db import models


class Experiment(models.Model):

    name = models.CharField(max_length=128, unique=True)
    site = models.CharField(max_length=128)
    descript = models.CharField(max_length=256, null=True)
    equipment = models.ManyToManyField(Equipment, related_name='%(class)s')
    begin_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    user = models.ManyToManyField(
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

    created_time = models.DateTimeField(auto_now_add=True)

    def equipment_display(self):
        return "\n".join([equipment.name for equipment in self.equipment.all()])

    def user_display(self):
        return "\n".join([user.username for user in self.user.all()])

    def __str__(self):
        return self.name

    class Meta:
        db_table = "experiment"
        ordering = ["-created_time"]
        verbose_name = "Experiment"
        verbose_name_plural = "Experiments"


class Review(models.Model):
    experiment = OneToOneField(
        Experiment, null=False, on_delete=models.CASCADE)
    is_passed = models.BooleanField(null=True)
    reply = models.CharField(max_length=128)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='%(class)s')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.experiment.name

    class Meta:
        db_table = "experiment_review"
        ordering = ["-created_time"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
