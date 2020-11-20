# Generated by Django 2.1.5 on 2020-11-19 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('Plumbing', 'Plumbing'), ('Deep Cleaning', 'Deep Cleaning'), ('Electrical', 'Electrical'), ('Painting', 'Painting')], max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('In Progress', 'In Progress'), ('Pending', 'Pending')], max_length=100)),
                ('remarks', models.TextField()),
                ('pincode', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_detail', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('primarynumber', models.IntegerField()),
                ('primarycode', models.CharField(max_length=10)),
                ('alt_number', models.IntegerField(blank=True, null=True)),
                ('alt_code', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'user_details',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to=settings.AUTH_USER_MODEL),
        ),
    ]
