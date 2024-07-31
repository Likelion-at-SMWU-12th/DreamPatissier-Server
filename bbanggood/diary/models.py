from django.db import models

class BreadDiary(models.Model):
    img_src = models.ImageField(max_length=255, null=True, blank=True)
    date = models.DateField()
    bread_name = models.CharField(max_length=255)
    bakery_name = models.CharField(max_length=255)
    tags = models.JSONField(default=list)
    review = models.TextField()

    def __str__(self):
        return f"{self.bread_name} from {self.bakery_name} on {self.date}"
