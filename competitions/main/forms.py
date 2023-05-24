import re
from datetime import datetime, timedelta
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from main.models import Player, Tournament


class PlayerLoginForm(AuthenticationForm):

    error_messages = {
        "invalid_login": "Invalid username or password.",
        "inactive": "This account is inactive."
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = "background-color: #EEEEEE;"

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and Player.objects.filter(username=username).exists():
            if not Player.objects.get(username=username).check_password(password):
                self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
                self.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
                self.add_error('__all__', self.error_messages['invalid_login'])
        else:
            self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['password'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('__all__', self.error_messages['invalid_login'])
        return cleaned_data


class PlayerSignUpForm(forms.ModelForm):
    password1 = forms.CharField(strip=False, widget=forms.PasswordInput())
    password2 = forms.CharField(strip=False, widget=forms.PasswordInput())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = "background-color: #EEEEEE;"

    class Meta:
        model = Player
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth', 'country')

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username and Player.objects.filter(username=username).exists():
            self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('username', 'Username is already exists.')
        else:
            self.fields['username'].widget.attrs.update({'class': 'form-control is-valid'})
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if any(char.isdigit() for char in first_name):
            self.fields['first_name'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('first_name', 'First name should not contain digits.')
        else:
            self.fields['first_name'].widget.attrs.update({'class': 'form-control is-valid'})
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if any(char.isdigit() for char in last_name):
            self.fields['last_name'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('last_name', 'Last name should not contain digits.')
        else:
            self.fields['last_name'].widget.attrs.update({'class': 'form-control is-valid'})
        return last_name

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and Player.objects.filter(email=email).exists():
            self.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('email', 'This email is already taken')
        elif email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})
        else:
            self.fields['email'].widget.attrs.update({'class': 'form-control is-valid'})
        return email

    def clean_password1(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        if password1 and (len(password1) < 8 or password1.isdigit()):
            self.fields['password1'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('password1', 'Password must be at least 8 characters long')
            self.add_error('password1', 'The password cannot be entirely numeric.')
        return password1

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.fields['password1'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['password2'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('password2', 'The two password fields didn’t match.')
        return password2

    def clean_date_of_birth(self):
        date = self.cleaned_data.get('date_of_birth')
        age = datetime.now().date() - date
        if age < timedelta(days=1460):
            self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('date_of_birth', 'Invalid date of birth')
        else:
            self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control is-valid'})
        return date

    def clean_country(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        if country and not re.match(r'^[A-Z]{2,3}$', country):
            self.fields['country'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('country', 'Country should consist of 3 uppercase letters, e.g. \'USA\'')
        else:
            self.fields['country'].widget.attrs.update({'class': 'form-control is-valid'})
        return country


class PlayerEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = "background-color: #EEEEEE;"

    def clean_username(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        if username and Player.objects.filter(username=username).exclude(username=self.instance.username).exists():
            self.fields['username'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('username', 'Username is already exists.')
        else:
            self.fields['username'].widget.attrs.update({'class': 'form-control is-valid'})
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if any(char.isdigit() for char in first_name):
            self.fields['first_name'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('first_name', 'First name should not contain digits.')
        else:
            self.fields['first_name'].widget.attrs.update({'class': 'form-control is-valid'})
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if any(char.isdigit() for char in last_name):
            self.fields['last_name'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('last_name', 'Last name should not contain digits.')
        else:
            self.fields['last_name'].widget.attrs.update({'class': 'form-control is-valid'})
        return last_name

    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email and Player.objects.filter(email=email).exclude(email=self.instance.email).exists():
            self.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('email', 'This email is already taken')
        elif email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.fields['email'].widget.attrs.update({'class': 'form-control is-invalid'})
        else:
            self.fields['email'].widget.attrs.update({'class': 'form-control is-valid'})
        return email

    def clean_date_of_birth(self):
        date = self.cleaned_data.get('date_of_birth')
        age = datetime.now().date() - date
        if age < timedelta(days=1460):
            self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('date_of_birth', 'Invalid date of birth')
        else:
            self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control is-valid'})
        return date

    def clean_country(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        if country and not re.match(r'^[A-Z]{3}$', country):
            self.fields['country'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('country', 'Country should consist of 3 uppercase letters, e.g. \'USA\'')
        else:
            self.fields['country'].widget.attrs.update({'class': 'form-control is-valid'})
        return country

    class Meta:
        model = Player
        fields = ['username', 'first_name', 'last_name', 'email', 'date_of_birth', 'country', 'photo']
        widgets = {
            'rating': forms.TextInput(attrs={'readonly': True}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class TournamentNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = "background-color: #EEEEEE;"

    def clean(self):

        cleaned_data = super().clean()

        if self.cleaned_data.get('name'):
            self.fields['name'].widget.attrs.update({'class': 'form-control is-valid'})
        else:
            self.fields['name'].widget.attrs.update({'class': 'form-control is-invalid'})

        if self.cleaned_data.get('place'):
            self.fields['place'].widget.attrs.update({'class': 'form-control is-valid'})
        else:
            self.fields['place'].widget.attrs.update({'class': 'form-control is-invalid'})

        self.fields['description'].widget.attrs.update({'class': 'form-control is-valid'})

        date_of_start = cleaned_data.get('date_of_start')
        date_of_end = cleaned_data.get('date_of_end')
        if date_of_start and date_of_end and date_of_start >= date_of_end:
            self.fields['date_of_start'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['date_of_end'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('date_of_start', 'Invalid date for competition.')
        else:
            self.fields['date_of_start'].widget.attrs.update({'class': 'form-control is-valid'})
            self.fields['date_of_end'].widget.attrs.update({'class': 'form-control is-valid'})

        return cleaned_data

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if capacity < 1:
            self.fields['capacity'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('capacity', ' Invalid capacity.')
        else:
            self.fields['capacity'].widget.attrs.update({'class': 'form-control is-valid'})
        return capacity

    class Meta:
        model = Tournament
        fields = ['name', 'place', 'description', 'capacity', 'date_of_start', 'date_of_end', 'system']
        widgets = {
            'capacity': forms.TextInput(attrs={'type': 'number'}),
            'date_of_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_of_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 5})
        }


class TournamentEditForm(forms.ModelForm):
    new_organizer = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter organizer\'s username'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = "background-color: #EEEEEE;"

    def clean(self):

        cleaned_data = super().clean()

        if self.cleaned_data.get('name'):
            self.fields['name'].widget.attrs.update({'class': 'form-control is-valid'})
        else:
            self.fields['name'].widget.attrs.update({'class': 'form-control is-invalid'})

        if self.cleaned_data.get('place'):
            self.fields['place'].widget.attrs.update({'class': 'form-control is-valid'})
        else:
            self.fields['place'].widget.attrs.update({'class': 'form-control is-invalid'})

        self.fields['description'].widget.attrs.update({'class': 'form-control is-valid'})

        date_of_start = cleaned_data.get('date_of_start')
        date_of_end = cleaned_data.get('date_of_end')
        if date_of_start and date_of_end and date_of_start >= date_of_end:
            self.fields['date_of_start'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.fields['date_of_end'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('date_of_start', 'Invalid date for competition.')
        else:
            self.fields['date_of_start'].widget.attrs.update({'class': 'form-control is-valid'})
            self.fields['date_of_end'].widget.attrs.update({'class': 'form-control is-valid'})

        return cleaned_data

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if capacity < 1:
            self.fields['capacity'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('capacity', ' Invalid capacity.')
        else:
            self.fields['capacity'].widget.attrs.update({'class': 'form-control is-valid'})
        return capacity

    def clean_new_organizer(self):
        new_organizer = self.cleaned_data['new_organizer']
        if not new_organizer or Player.objects.filter(username=new_organizer).exists():
            self.fields['new_organizer'].widget.attrs.update({'class': 'form-control is-valid'})
        else:
            self.fields['new_organizer'].widget.attrs.update({'class': 'form-control is-invalid'})
            self.add_error('new_organizer', 'This username does not exists.')

        return new_organizer

    class Meta:
        model = Tournament
        fields = ['name', 'place', 'description', 'capacity', 'date_of_start', 'date_of_end', 'new_organizer', 'system']
        widgets = {
            'capacity': forms.TextInput(attrs={'type': 'number'}),
            'date_of_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_of_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 5})
        }
