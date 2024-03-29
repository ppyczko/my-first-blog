# Generated by Django 5.0.3 on 2024-03-22 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_main', to='blog.post')),
                ('related_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts_related', to='blog.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='related_posts',
            field=models.ManyToManyField(blank=True, through='blog.RelatedPost', to='blog.post'),
        ),
    ]
