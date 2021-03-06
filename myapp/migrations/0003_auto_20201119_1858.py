# Generated by Django 2.1.5 on 2020-11-19 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20201119_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_order', to='myapp.State'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('Painting', 'Painting'), ('Deep Cleaning', 'Deep Cleaning'), ('Plumbing', 'Plumbing'), ('Electrical', 'Electrical')], max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('Pending', 'Pending'), ('Completed', 'Completed')], max_length=100),
        ),
    ]
