from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from datetime import date
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class UserSignupForm(forms.ModelForm):
    # Fields for user details
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'John'}))
    middle_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Mike'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Doe'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'JohnDoe'}))
    
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer-not-to-say', 'Prefer not to say')],
                               required=True, widget=forms.Select(attrs={'placeholder': 'Select Gender'}))
    
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    MIN_AGE = 16
    MAX_AGE = 100
    
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={'placeholder': 'johndoe@example.com'}))
    
    country = CountryField().formfield()

    phone_number = PhoneNumberField().formfield()

    organization = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Your Organization'}))
    job_title = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Your Job Title'}))
    
    data_use = forms.ChoiceField(choices=[('research', 'Research'), ('business-analysis', 'Business Analysis'), ('education', 'Education'), ('personal-use', 'Personal Use'), ('other', 'Other')],
                                 required=True, widget=forms.Select(attrs={'placeholder': 'Select an option'}))
    
    additional_details = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={'placeholder': 'Provide more context if needed'}))
    
    # Password fields at the end
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': '********'}))
    confirm_password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': '********'}))

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'username', 'gender', 'date_of_birth', 'email', 'phone_number', 'country',
                  'organization', 'job_title', 'data_use', 'additional_details', 'password', 'confirm_password']

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        today = date.today()
        if date_of_birth:
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < self.MIN_AGE:
                raise forms.ValidationError(f"Age must be {self.MIN_AGE} years and above.")
            if age > self.MAX_AGE:
                raise forms.ValidationError(f"Age must be between {self.MIN_AGE} and {self.MAX_AGE} years.")
        return date_of_birth

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        # Check for duplicate username
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Username is already taken.')

        # Check for duplicate email
        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email is already in use.')

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Ensure password is hashed
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if not username_or_email or not password:
            raise forms.ValidationError('Both username/email and password are required.')

        user = None
        if User.objects.filter(email=username_or_email).exists():
            user = User.objects.get(email=username_or_email)
        elif User.objects.filter(username=username_or_email).exists():
            user = User.objects.get(username=username_or_email)

        if user is None or not user.check_password(password):
            raise forms.ValidationError('Login details incorrect')

        # Optionally, authenticate the user
        self.user = authenticate(username=user.username, password=password)

        if self.user is None:
            raise forms.ValidationError('Login failed')

        return cleaned_data
