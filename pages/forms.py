from django import forms
from django.contrib.auth.models import User
from .models import Webpage, WebpageRows, WebpageDocs, Slider
from tinymce.widgets import TinyMCE
from .utils import Utils

class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'description', 'image', 'button_1', 'url_1', 'button_2', 'url_2', 'button_3', 'url_3']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3, 'placeholder': 'Текст'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'button_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва'}),
            'url_1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Посилання'}),
            'button_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва'}),
            'url_2': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Посилання'}),
            'button_3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва'}),
            'url_3': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Посилання'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate button_1 and url_1
        button_1 = cleaned_data.get('button_1', '').strip()
        url_1 = cleaned_data.get('url_1', '').strip()
        
        if (button_1 and not url_1) or (not button_1 and url_1):
            raise forms.ValidationError('Якщо вказано назву кнопки 1, то посилання також обов\'язкове, і навпаки.')
        
        # Validate button_2 and url_2
        button_2 = cleaned_data.get('button_2', '').strip()
        url_2 = cleaned_data.get('url_2', '').strip()
        
        if (button_2 and not url_2) or (not button_2 and url_2):
            raise forms.ValidationError('Якщо вказано назву кнопки 2, то посилання також обов\'язкове, і навпаки.')
        
        # Validate button_3 and url_3
        button_3 = cleaned_data.get('button_3', '').strip()
        url_3 = cleaned_data.get('url_3', '').strip()
        
        if (button_3 and not url_3) or (not button_3 and url_3):
            raise forms.ValidationError('Якщо вказано назву кнопки 3, то посилання також обов\'язкове, і навпаки.')
        
        return cleaned_data


class WebpageAdminForm(forms.ModelForm):
    slug = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    admin = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.exclude(is_superuser=True),
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'})
    )
    
    class Meta:
        model = Webpage
        fields = ['parent', 'title', 'slug', 'design', 'admin']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'design': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'parent': forms.HiddenInput(),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = Utils.slugify(self.cleaned_data.get('title'))
            if Webpage.objects.filter(parent=self.cleaned_data.get('parent'), slug=slug).exists():
                raise forms.ValidationError('Цей slug вже зайнятий')
        return slug
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class WebpageForm(forms.ModelForm):
    class Meta:
        model = Webpage
        fields = ['parent', 'title', 'phone', 'email', 'address', 'wallpaper', 'content']
        widgets = {
            'parent': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'address': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'wallpaper': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'content': TinyMCE(attrs={'class': 'form-control form-control-sm', 'cols': 80, 'rows': 10}),
        }
        labels = {
            'parent': '',
            'title': 'Заголовок сторінки',
            'phone': 'Телефон',
            'email': 'Email',
            'address': 'Адреса',
            'wallpaper': 'Основне зображення',
            'content': 'Вміст',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove contact fields if design is not basic_with_tabs
        if self.instance and self.instance.design != 'basic_with_tabs':
            self.fields.pop('phone', None)
            self.fields.pop('email', None)
            self.fields.pop('address', None)

class WebpageRowsForm(forms.ModelForm):
    class Meta:
        model = WebpageRows
        fields = ['webpage', 'col1', 'col2', 'col3']
        widgets = {
            'webpage': forms.HiddenInput(),
            'col1': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'col2': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'col3': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
        labels = {
            'col1': 'Колонка 1',
            'col2': 'Колонка 2',
            'col3': 'Колонка 3',
        }

WebpageRowsFormset = forms.modelformset_factory(
    WebpageRows,
    form=WebpageRowsForm,
    can_delete=True,
    extra=1
)

class WebpageDocsForm(forms.ModelForm):
    class Meta:
        model = WebpageDocs
        fields = ['webpage', 'title', 'url']
        widgets = {
            'webpage': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'url': forms.URLInput(attrs={'class': 'form-control form-control-sm'}),
        }
        labels = {
            'title': 'Заголовок',
            'url': 'Посилання',
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith(('https://drive.google.com', 'https://docs.google.com')):
            raise forms.ValidationError('URL має починатися з https://drive.google.com/ або https://docs.google.com/')
        return url


WebpageDocsFormset = forms.modelformset_factory(
    WebpageDocs,
    form=WebpageDocsForm,
    can_delete=True,
    extra=1
)