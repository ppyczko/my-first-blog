# Generated by Django 5.0.3 on 2024-03-21 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20240320_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('stories', 'Stories'), ('films', 'Films'), ('books', 'Books'), ('sports', 'Sports'), ('fashion', 'Fashion'), ('politics', 'Politics')], default='stories', max_length=15),
        ),
    ]
