from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vegeviewapp', '0002_pestdisease_affected_part'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g. North Plot - Roma Tomatoes', max_length=150)),
                ('area_hectares', models.DecimalField(decimal_places=2, default=1.5, help_text='Field area in hectares', max_digits=6)),
                ('latitude', models.FloatField(default=9.082)),
                ('longitude', models.FloatField(default=8.6753)),
                ('current_ndvi', models.FloatField(default=0.75, help_text='Vegetation Index from -1.0 to 1.0 (Healthy crop 0.6 - 0.85)')),
                ('health_status', models.CharField(choices=[('vigorous', 'Vigorous Growth (NDVI >= 0.70)'), ('moderate', 'Moderate Health (NDVI 0.45 - 0.69)'), ('stressed', 'Stressed / Water Deficit (NDVI 0.25 - 0.44)'), ('critical', 'Critical / Degraded (NDVI < 0.25)')], default='vigorous', max_length=20)),
                ('irrigation_system', models.CharField(blank=True, default='Drip Irrigation', max_length=80)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('crop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fields', to='vegeviewapp.vegetable')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),
    ]
