# Generated by Django 4.0.4 on 2022-05-04 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tibiahelper', '0003_alter_creature_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creature',
            name='experience',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
