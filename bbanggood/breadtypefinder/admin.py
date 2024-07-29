from django.contrib import admin
from .models import Result, ResultType, BreadRecommendation

# Register your models here.
admin.site.register(Result)
admin.site.register(ResultType)
admin.site.register(BreadRecommendation)