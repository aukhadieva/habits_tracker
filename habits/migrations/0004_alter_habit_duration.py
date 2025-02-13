# Generated by Django 4.2.14 on 2024-07-11 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0003_alter_habit_frequency"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="duration",
            field=models.TimeField(
                blank=True,
                db_comment="время, которое предположительно потратит пользователь на выполнение привычки",
                null=True,
                verbose_name="Время на выполнение",
            ),
        ),
    ]
