# Generated by Django 5.0.3 on 2024-03-25 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_post_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category_new',
            new_name='category',
        ),
    ]