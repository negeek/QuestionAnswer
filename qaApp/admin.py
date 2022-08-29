from django.contrib import admin
from .models import IndivdualQuestion, IndividualTopic, StudentTopic, StudentQuestion

# Register your models here.
admin.site.register(IndividualTopic)
admin.site.register(IndivdualQuestion)
admin.site.register(StudentTopic)
admin.site.register(StudentQuestion)
