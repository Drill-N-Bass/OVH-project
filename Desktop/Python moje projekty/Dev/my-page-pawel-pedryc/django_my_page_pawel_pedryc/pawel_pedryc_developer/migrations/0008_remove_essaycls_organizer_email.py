# Generated by Django 4.0.1 on 2022-09-09 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pawel_pedryc_developer', '0007_essaycls_date_essaycls_organizer_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='essaycls',
            name='organizer_email',
        ),
    ]