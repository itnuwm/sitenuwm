from django import forms
from django.utils import timezone
from .models import Post
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['is_published', 'kind', 'title', 'author', 'wallpaper', 'date_published', 'content']
        labels = {
            'is_published': 'Позначка про опублікування. Якщо ввімкнено, публікація буде видима на сайті.',
            'kind': 'Тип публікації',
            'title': 'Заголовок',
            'author': 'Автор',
            'wallpaper': 'Обкладинка',
            'date_published': 'Дата публікації',
            'content': 'Вміст',
        }
        widgets = {
            'is_published': forms.CheckboxInput(attrs={'class': 'custom-control-input'}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'wallpaper': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'date_published': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'content': TinyMCE(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['date_published'].initial = timezone.now()
            self.fields['is_published'].initial = False