# Generated by Django 4.0.6 on 2022-08-01 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0002_feedback_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='flowers.customer', verbose_name='Автор'),
            preserve_default=False,
        ),
    ]