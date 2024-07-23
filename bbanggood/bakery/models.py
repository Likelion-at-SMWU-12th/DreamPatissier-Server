from django.db import models

class Bread(models.Model):
    CATEGORY_CHOICES = [
        ('bread', '식빵'),
        ('baguette', '바게트'),
        ('bagel', '베이글'),
        ('cake', '케이크'),
        ('donut', '도넛'),
        ('cream', '크림빵'),
        ('root_vegetable', '구황작물빵'),
        ('special', '기획전'),
    ]
    img_src = models.ImageField(max_length=255, null=True, blank=True)
    tags = models.JSONField(null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
