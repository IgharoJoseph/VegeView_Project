from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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


@login_required(login_url='Login')
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


@login_required(login_url='Login')
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
    if request.user.is_authenticated:
        return redirect('DiseaseDirectory')

    if request.method == 'POST':
        full_name = request.POST.get('full-name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm-password', '')

        if not email or not password:
            messages.error(request, 'Please provide an email and password.')
            return render(request, 'vegeviewapp/signup.html', {'full_name': full_name, 'email': email})

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'vegeviewapp/signup.html', {'full_name': full_name, 'email': email})

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'vegeviewapp/signup.html', {'full_name': full_name, 'email': email})

        # Use email or part before @ as username
        base_username = email.split('@')[0] if '@' in email else email
        username = base_username
        suffix = 1
        while User.objects.filter(username=username).exists():
            username = f'{base_username}{suffix}'
            suffix += 1

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists. Please log in.')
            return render(request, 'vegeviewapp/signup.html', {'full_name': full_name, 'email': email})

        user = User.objects.create_user(username=username, email=email, password=password)
        if email == 'josephigharo@gmail.com' or User.objects.count() == 1:
            user.is_staff = True
            user.is_superuser = True
        if full_name:
            user.first_name = full_name
            user.save()

        auth_login(request, user)
        messages.success(request, f'Welcome to VegeView, {user.first_name or user.username}!')
        return redirect('DiseaseDirectory')

    return render(request, 'vegeviewapp/signup.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('DiseaseDirectory')

    next_url = request.GET.get('next', 'DiseaseDirectory')

    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not identifier or not password:
            messages.error(request, 'Please provide both email/username and password.')
            return render(request, 'vegeviewapp/login.html', {'identifier': identifier})

        # Try to find user by email or username
        user_obj = User.objects.filter(Q(email__iexact=identifier) | Q(username__iexact=identifier)).first()
        username_to_auth = user_obj.username if user_obj else identifier

        user = authenticate(request, username=username_to_auth, password=password)
        if user is not None:
            auth_login(request, user)
            target = request.POST.get('next') or next_url
            return redirect(target if target and target != 'None' else 'DiseaseDirectory')
        else:
            messages.error(request, 'Invalid email/username or password.')
            return render(request, 'vegeviewapp/login.html', {'identifier': identifier, 'next': next_url})

    return render(request, 'vegeviewapp/login.html', {'next': next_url})


def logout_view(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('HomePage')


def forgotpassword(request):
    return render(request, 'vegeviewapp/forgotpassword.html')
