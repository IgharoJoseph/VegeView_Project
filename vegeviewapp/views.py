from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Vegetable, PestDisease


def index(request):
    featured_diseases = PestDisease.objects.prefetch_related('affected_vegetables')[:3]
    vegetable_count = Vegetable.objects.count()
    disease_count = PestDisease.objects.count()
    return render(request, 'vegeviewapp/index.html', {
        'featured_diseases': featured_diseases,
        'vegetable_count': vegetable_count,
        'disease_count': disease_count,
    })


def directory(request):
    query = request.GET.get('q', '').strip()
    problem_type = request.GET.get('type', '').strip()
    severity = request.GET.get('severity', '').strip()
    vegetable_id = request.GET.get('crop', '').strip()

    items = PestDisease.objects.prefetch_related('affected_vegetables').all()

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(causal_agent__icontains=query) |
            Q(symptoms__icontains=query) |
            Q(affected_vegetables__name__icontains=query)
        ).distinct()

    if problem_type:
        items = items.filter(problem_type=problem_type)

    if severity:
        items = items.filter(severity=severity)

    if vegetable_id:
        items = items.filter(affected_vegetables__id=vegetable_id)

    vegetables = Vegetable.objects.all()

    return render(request, 'vegeviewapp/directory.html', {
        'items': items,
        'vegetables': vegetables,
        'selected_q': query,
        'selected_type': problem_type,
        'selected_severity': severity,
        'selected_crop': vegetable_id,
        'total_count': items.count(),
    })


def disease_detail(request, pk):
    item = get_object_or_404(PestDisease.objects.prefetch_related('affected_vegetables'), pk=pk)
    related_issues = PestDisease.objects.filter(
        affected_vegetables__in=item.affected_vegetables.all()
    ).exclude(pk=item.pk).distinct()[:3]
    return render(request, 'vegeviewapp/disease_detail.html', {
        'item': item,
        'related_issues': related_issues,
    })


def signup(request):
    return render(request, 'vegeviewapp/signup.html')


def login(request):
    return render(request, 'vegeviewapp/login.html')


def forgotpassword(request):
    return render(request, 'vegeviewapp/forgotpassword.html')
