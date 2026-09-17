from django.core.management.base import BaseCommand
from vegeviewapp.models import Vegetable, PestDisease

CROPS_DATA = [
    {
        "name": "Tomato",
        "scientific_name": "Solanum lycopersicum",
        "category": "fruit",
        "growing_duration_days": 80,
        "ideal_temperature": "21°C - 29°C",
        "description": "High-value fruit vegetable grown across open fields and greenhouses."
    },
    {
        "name": "Hot Pepper / Habanero",
        "scientific_name": "Capsicum chinense",
        "category": "fruit",
        "growing_duration_days": 90,
        "ideal_temperature": "24°C - 32°C",
        "description": "Pungent pepper widely cultivated across tropical and subtropical regions."
    },
    {
        "name": "Cucumber",
        "scientific_name": "Cucumis sativus",
        "category": "fruit",
        "growing_duration_days": 55,
        "ideal_temperature": "22°C - 30°C",
        "description": "Fast-growing climbing vine crop requiring consistent moisture and trellising."
    },
    {
        "name": "Fluted Pumpkin (Ugwu)",
        "scientific_name": "Telfairia occidentalis",
        "category": "leafy",
        "growing_duration_days": 120,
        "ideal_temperature": "22°C - 34°C",
        "description": "Prized tropical leafy green with dense foliage and high iron content."
    },
    {
        "name": "Okra",
        "scientific_name": "Abelmoschus esculentus",
        "category": "fruit",
        "growing_duration_days": 60,
        "ideal_temperature": "25°C - 35°C",
        "description": "Hardy flowering plant yielding tender mucilaginous pods."
    },
    {
        "name": "Cabbage",
        "scientific_name": "Brassica oleracea",
        "category": "leafy",
        "growing_duration_days": 75,
        "ideal_temperature": "15°C - 24°C",
        "description": "Cool-season heading vegetable prone to caterpillars and black rot."
    }
]

DISEASES_DATA = [
    {
        "name": "Early Blight (Alternaria)",
        "problem_type": "disease",
        "affected_part": "leaves",
        "causal_agent": "Alternaria solani (Fungus)",
        "severity": "high",
        "crops": ["Tomato", "Hot Pepper / Habanero"],
        "symptoms": "Concentric rings (target board spots) starting on older lower leaves. Leaves turn yellow around spots and drop early. Stem cankers may form near soil line.",
        "organic_treatment": "Prune lower infected leaves; apply copper-based fungicide or baking soda spray (1 tbsp baking soda + 1 tsp horticultural oil per gallon of water); mulch heavily to prevent soil splash.",
        "chemical_treatment": "Mancozeb, Chlorothalonil, or Azoxystrobin applied every 7-10 days upon first sighting.",
        "prevention_tips": "Rotate crops 3 years away from Solanaceae; use drip irrigation instead of overhead watering; space plants for air circulation."
    },
    {
        "name": "Late Blight",
        "problem_type": "disease",
        "affected_part": "leaves",
        "causal_agent": "Phytophthora infestans (Oomycete)",
        "severity": "high",
        "crops": ["Tomato"],
        "symptoms": "Rapidly expanding water-soaked greasy brown lesions on leaves and stems. White fuzzy mold on leaf undersides in humid mornings. Fruit develops large, firm, greasy brown patches.",
        "organic_treatment": "Immediately destroy heavily infected plants; apply fixed copper spray proactively during prolonged wet/cool spells.",
        "chemical_treatment": "Metalaxyl + Mancozeb (e.g. Ridomil Gold) or Cymoxanil at first onset.",
        "prevention_tips": "Plant certified disease-free seedlings; avoid wet leaves overnight; maintain wide plant spacing."
    },
    {
        "name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "problem_type": "disease",
        "affected_part": "leaves",
        "causal_agent": "Geminivirus (transmitted by Silverleaf Whitefly)",
        "severity": "high",
        "crops": ["Tomato", "Hot Pepper / Habanero"],
        "symptoms": "Severe upward curling and cupping of leaflets, distinct yellow margins between veins, stunted plant growth, flower abortion, and bushy erect shoots.",
        "organic_treatment": "No cure once infected; immediately remove and burn infected plants. Control whitefly vectors using yellow sticky traps and neem oil spray.",
        "chemical_treatment": "Insecticides targeting whitefly nymphs: Acetamiprid, Imidacloprid, or Spiromesifen.",
        "prevention_tips": "Use TYLCV-resistant hybrids; install 50-mesh insect netting in nurseries; maintain weed-free borders."
    },
    {
        "name": "Bacterial Wilt",
        "problem_type": "disease",
        "affected_part": "whole",
        "causal_agent": "Ralstonia solanacearum (Bacterium)",
        "severity": "high",
        "crops": ["Tomato", "Hot Pepper / Habanero"],
        "symptoms": "Rapid daytime wilting of green leaves without preliminary yellowing. Plant fails to recover overnight. Stem pith browns; stem water test releases milky white bacterial streaming threads.",
        "organic_treatment": "Uproot and destroy wilted plants with surrounding root soil; drench soil with bio-control agents like Bacillus subtilis or Trichoderma.",
        "chemical_treatment": "No effective chemical curative once vascular system is invaded. Copper hydroxide can help reduce surface spread.",
        "prevention_tips": "Strict 4-year crop rotation with non-host crops (corn, sorghum); ensure raised beds with excellent drainage."
    },
    {
        "name": "Aphid Infestation",
        "problem_type": "pest",
        "affected_part": "leaves",
        "causal_agent": "Aphis gossypii / Myzus persicae",
        "severity": "medium",
        "crops": ["Tomato", "Hot Pepper / Habanero", "Cucumber", "Fluted Pumpkin (Ugwu)", "Okra", "Cabbage"],
        "symptoms": "Clusters of tiny green, yellow, or black soft-bodied insects under leaves. Curled, distorted shoot tips. Sticky honeydew on foliage attracting black sooty mold and ants.",
        "organic_treatment": "Strong jet of water to dislodge; insecticidal soap or neem oil spray (5ml/L water + gentle liquid soap) applied at dusk; release ladybird beetles.",
        "chemical_treatment": "Cypermethrin, Lambda-cyhalothrin, or Acetamiprid applied targeting leaf undersides.",
        "prevention_tips": "Inspect leaf undersides weekly; intercrop with pungent herbs (coriander, basil, garlic)."
    },
    {
        "name": "Blossom End Rot",
        "problem_type": "deficiency",
        "affected_part": "fruit",
        "causal_agent": "Calcium deficiency exacerbated by irregular watering",
        "severity": "medium",
        "crops": ["Tomato", "Hot Pepper / Habanero"],
        "symptoms": "Flat, water-soaked spot at the blossom end of the fruit (opposite the stem) turning into a sunken, leathery, dark brown or black scar.",
        "organic_treatment": "Maintain steady, uniform soil moisture; apply calcium nitrate foliar spray; add compost and agricultural lime or crushed eggshells to soil.",
        "chemical_treatment": "Foliar spray of chelated calcium (Calcium EDTA) applied weekly during heavy fruit set.",
        "prevention_tips": "Mulch beds to stabilize soil moisture; test soil pH (aim for 6.2 - 6.8); avoid excessive nitrogen fertilizer which drives rapid leaf growth over calcium uptake."
    },
    {
        "name": "Powdery Mildew",
        "problem_type": "disease",
        "affected_part": "leaves",
        "causal_agent": "Podosphaera xanthii (Fungus)",
        "severity": "medium",
        "crops": ["Cucumber", "Okra", "Tomato"],
        "symptoms": "White to grayish talcum powder-like spots on upper leaf surfaces and stems. Heavily colonized leaves yellow, brown, curl upward, and dry out crisp.",
        "organic_treatment": "Spray milk-water solution (40% milk, 60% water) under sunlight; potassium bicarbonate (3g/L) or wettable sulfur spray.",
        "chemical_treatment": "Triadimefon, Tebuconazole, or Azoxystrobin spray.",
        "prevention_tips": "Choose resistant cultivars; prune dense foliage to maximize airflow and sunlight penetration."
    },
    {
        "name": "Root-Knot Nematodes",
        "problem_type": "pest",
        "affected_part": "roots",
        "causal_agent": "Meloidogyne spp. (Microscopic roundworms)",
        "severity": "high",
        "crops": ["Tomato", "Hot Pepper / Habanero", "Cucumber", "Fluted Pumpkin (Ugwu)", "Okra"],
        "symptoms": "Above-ground stunting, pale yellowing, and persistent mid-day wilting despite moist soil. Digging roots reveals irregular galls, swellings, and clubbed root systems.",
        "organic_treatment": "Heavy application of neem cake and poultry manure into beds; grow and incorporate African Marigold (Tagetes erecta) cover crops.",
        "chemical_treatment": "Oxamyl or biological nematicides (Purpureocillium lilacinum).",
        "prevention_tips": "Solarize soil using clear plastic during the hottest months; rotate with resistant grasses or grain crops."
    }
]


class Command(BaseCommand):
    help = "Seed database with vegetables and vegetable diagnostic pests/diseases"

    def handle(self, *args, **options):
        self.stdout.write("Seeding vegetable and disease catalog...")

        crop_objects = {}
        for cdata in CROPS_DATA:
            crop, created = Vegetable.objects.get_or_create(
                name=cdata["name"],
                defaults={
                    "scientific_name": cdata["scientific_name"],
                    "category": cdata["category"],
                    "growing_duration_days": cdata["growing_duration_days"],
                    "ideal_temperature": cdata["ideal_temperature"],
                    "description": cdata["description"]
                }
            )
            crop_objects[crop.name] = crop
            if created:
                self.stdout.write(f"Created crop: {crop.name}")

        for ddata in DISEASES_DATA:
            disease, created = PestDisease.objects.get_or_create(
                name=ddata["name"],
                defaults={
                    "problem_type": ddata["problem_type"],
                    "affected_part": ddata.get("affected_part", "leaves"),
                    "causal_agent": ddata["causal_agent"],
                    "severity": ddata["severity"],
                    "symptoms": ddata["symptoms"],
                    "organic_treatment": ddata["organic_treatment"],
                    "chemical_treatment": ddata["chemical_treatment"],
                    "prevention_tips": ddata["prevention_tips"]
                }
            )
            # Link crops
            for cname in ddata.get("crops", []):
                if cname in crop_objects:
                    disease.affected_vegetables.add(crop_objects[cname])

            if created:
                self.stdout.write(f"Created diagnostic entry: {disease.name}")

        self.stdout.write(self.style.SUCCESS("Diagnostic seed data complete!"))
