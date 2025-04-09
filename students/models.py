from django.db import models


class Student(models.Model):
    # auto-incremented primary key
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
