# Generated by Django 5.1.3 on 2024-11-27 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='created_at',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
