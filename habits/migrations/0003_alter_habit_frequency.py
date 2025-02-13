# Generated by Django 4.2.14 on 2024-07-11 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0002_alter_habit_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="frequency",
            field=models.CharField(
                blank=True,
                choices=[("daily", "ежедневно"), ("once_a_week", "раз в неделю")],
                db_comment="периодичность выполнения привычки для напоминания в днях",
                default="daily",
                null=True,
                verbose_name="Периодичность",
            ),
        ),
    ]
