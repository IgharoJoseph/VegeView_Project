# Generated manually for boundary_geojson
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('vegeviewapp', '0003_farmfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmfield',
            name='boundary_geojson',
            field=models.TextField(blank=True, default='', help_text='GeoJSON geometry for polygon plot'),
        ),
    ]
