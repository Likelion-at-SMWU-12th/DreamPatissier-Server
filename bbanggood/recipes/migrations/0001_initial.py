# Generated by Django 5.0.7 on 2024-07-31 20:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('tags', models.CharField(max_length=255)),
                ('cookingTime', models.CharField(max_length=255)),
                ('equipment', models.CharField(max_length=100)),
                ('ingredients', models.JSONField(blank=True, default=list, null=True)),
                ('step1_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step1_description', models.TextField(blank=True, null=True)),
                ('step2_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step2_description', models.TextField(blank=True, null=True)),
                ('step3_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step3_description', models.TextField(blank=True, null=True)),
                ('step4_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step4_description', models.TextField(blank=True, null=True)),
                ('step5_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step5_description', models.TextField(blank=True, null=True)),
                ('step6_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step6_description', models.TextField(blank=True, null=True)),
                ('step7_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step7_description', models.TextField(blank=True, null=True)),
                ('step8_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step8_description', models.TextField(blank=True, null=True)),
                ('step9_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step9_description', models.TextField(blank=True, null=True)),
                ('step10_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('step10_description', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='recipes.recipe')),
            ],
            options={
                'unique_together': {('user', 'recipe')},
            },
        ),
    ]
