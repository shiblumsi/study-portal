from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'notes'
        verbose_name_plural = 'notes'

class Homework(models.Model):
    uesr = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    due = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title