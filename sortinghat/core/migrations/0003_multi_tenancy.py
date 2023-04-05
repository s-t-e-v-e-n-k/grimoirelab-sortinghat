# Generated by Django 3.2.18 on 2023-04-04 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import grimoirelab_toolkit.datetime
import sortinghat.core.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_importidentitiestask'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='tenant',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', sortinghat.core.models.CreationDateTimeField(default=grimoirelab_toolkit.datetime.datetime_utcnow, editable=False)),
                ('last_modified', sortinghat.core.models.LastModificationDateTimeField(default=grimoirelab_toolkit.datetime.datetime_utcnow, editable=False)),
                ('host', models.CharField(max_length=128)),
                ('database', models.CharField(max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tenants',
                'unique_together': {('user', 'host')},
            },
        ),
    ]
