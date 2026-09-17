from django.db import models


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
