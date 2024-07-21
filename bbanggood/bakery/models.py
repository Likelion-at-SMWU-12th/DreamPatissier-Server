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
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image_url = models.URLField()

    def __str__(self):
        return self.name
