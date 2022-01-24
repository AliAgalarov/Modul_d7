# Generated by Django 3.2.9 on 2021-12-13 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('newsportal', '0002_auto_20211208_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='postCategory',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='newsportal.category'),
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]