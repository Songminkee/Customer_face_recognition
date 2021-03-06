# Generated by Django 3.1.7 on 2021-03-04 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingLog',
            fields=[
                ('tid', models.AutoField(primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('video_path', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BorrowerTrackingLog',
            fields=[
                ('btid', models.AutoField(primary_key=True, serialize=False)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.borrower')),
                ('tid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.trackinglog')),
            ],
        ),
    ]
