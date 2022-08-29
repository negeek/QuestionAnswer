from audioop import maxpp
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class IndividualTopic(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class IndivdualQuestion(models.Model):
    topic = models.ForeignKey(IndividualTopic, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.question[:20]


class StudentTopic(models.Model):
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=50)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.course_code


class StudentQuestion(models.Model):
    course_code = models.ForeignKey(
        StudentTopic, on_delete=models.CASCADE, related_name='code')
    question = models.TextField()
    answer = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.question[:20]
