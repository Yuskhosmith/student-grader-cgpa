from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_lecturer = models.BooleanField('lecturer_status', default=False)
    is_student = models.BooleanField('student_status', default=False)
    pass

class Course(models.Model):
    COURSE_TYPE_CHOICE = (
        ('Compulsory', 'Compulsory'),
        ('Required', 'Required'),
        ('Elective', 'Elective')
    )
    course_code = models.CharField(max_length=8, null=True)
    course_title = models.CharField(max_length=1000, null=True)
    unit = models.IntegerField(null=True)
    type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICE, null=True)

class Result(models.Model):
    student = models.ForeignKey(User, related_name='student_result', on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, related_name='course_result' ,on_delete=models.SET_NULL, null=True)
    test_score = models.IntegerField()
    exam_score = models.IntegerField()
    grade = models.IntegerField()
