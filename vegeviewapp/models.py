from django.db import models
from django.conf import settings


class Vegetable(models.Model):
    CATEGORY_CHOICES = [
        ('leafy', 'Leafy Green (e.g. Spinach, Ugwu)'),
        ('fruit', 'Fruiting Vegetable (e.g. Tomato, Pepper, Cucumber)'),
        ('root', 'Root & Tuber (e.g. Carrot, Sweet Potato)'),
        ('bulb', 'Bulb (e.g. Onion, Garlic)'),
        ('legume', 'Legume (e.g. Green Beans, Cowpea)'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fruit')
    description = models.TextField(blank=True)
    growing_duration_days = models.PositiveIntegerField(
        help_text="Average days from planting to harvest",
        default=60
    )
    ideal_temperature = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. 20°C - 30°C"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PestDisease(models.Model):
    TYPE_CHOICES = [
        ('disease', 'Disease (Fungal/Bacterial/Viral)'),
        ('pest', 'Pest / Insect Infestation'),
        ('deficiency', 'Nutrient Deficiency'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Moderate'),
        ('high', 'High / Severe'),
    ]

    PART_CHOICES = [
        ('leaves', 'Leaves & Foliage'),
        ('stem', 'Stem & Shoots'),
        ('fruit', 'Fruit / Pod'),
        ('roots', 'Roots & Soil Level'),
        ('whole', 'Whole Plant'),
    ]

    name = models.CharField(max_length=150)
    problem_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='disease')
    affected_part = models.CharField(
        max_length=20,
        choices=PART_CHOICES,
        default='leaves',
        help_text="Primary plant part where symptoms manifest"
    )
    causal_agent = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Alternaria solani, Bemisia tabaci"
    )
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium')
    affected_vegetables = models.ManyToManyField(
        Vegetable,
        related_name='pests_and_diseases'
    )
    symptoms = models.TextField(help_text="Key visible symptoms on leaves, stems, or fruits")
    organic_treatment = models.TextField(
        blank=True,
        help_text="Eco-friendly / cultural / organic control methods"
    )
    chemical_treatment = models.TextField(
        blank=True,
        help_text="Recommended chemical fungicides/pesticides if severe"
    )
    prevention_tips = models.TextField(
        blank=True,
        help_text="Crop rotation, spacing, resistant varieties"
    )
    image_url = models.URLField(blank=True, help_text="Optional reference image URL")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Pest & Disease"
        verbose_name_plural = "Pests & Diseases"

    def __str__(self):
        return f"{self.name} ({self.get_problem_type_display()})"


class FarmField(models.Model):
    HEALTH_CHOICES = [
        ('vigorous', 'Vigorous Growth (NDVI >= 0.70)'),
        ('moderate', 'Moderate Health (NDVI 0.45 - 0.69)'),
        ('stressed', 'Stressed / Water Deficit (NDVI 0.25 - 0.44)'),
        ('critical', 'Critical / Degraded (NDVI < 0.25)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fields'
    )
    name = models.CharField(max_length=150, help_text="e.g. North Plot - Roma Tomatoes")
    crop = models.ForeignKey(
        Vegetable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fields'
    )
    area_hectares = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1.5,
        help_text="Field area in hectares"
    )
    latitude = models.FloatField(default=9.0820)
    longitude = models.FloatField(default=8.6753)
    current_ndvi = models.FloatField(
        default=0.75,
        help_text="Vegetation Index from -1.0 to 1.0 (Healthy crop 0.6 - 0.85)"
    )
    health_status = models.CharField(
        max_length=20,
        choices=HEALTH_CHOICES,
        default='vigorous'
    )
    irrigation_system = models.CharField(
    boundary_geojson = models.TextField(blank=True, default="", help_text="GeoJSON geometry for polygon plot")
        max_length=80,
        blank=True,
        default='Drip Irrigation'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.current_ndvi:.2f} NDVI)"

    def update_health_status(self):
        if self.current_ndvi >= 0.70:
            self.health_status = 'vigorous'
        elif self.current_ndvi >= 0.45:
            self.health_status = 'moderate'
        elif self.current_ndvi >= 0.25:
            self.health_status = 'stressed'
        else:
            self.health_status = 'critical'
