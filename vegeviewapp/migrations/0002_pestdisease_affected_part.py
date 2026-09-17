from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vegeviewapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pestdisease',
            name='affected_part',
            field=models.CharField(
                choices=[
                    ('leaves', 'Leaves & Foliage'),
                    ('stem', 'Stem & Shoots'),
                    ('fruit', 'Fruit / Pod'),
                    ('roots', 'Roots & Soil Level'),
                    ('whole', 'Whole Plant')
                ],
                default='leaves',
                help_text='Primary plant part where symptoms manifest',
                max_length=20
            ),
        ),
    ]
