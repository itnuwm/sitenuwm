from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import os
from pages.utils import Utils


class Slider(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, default='')
    image = models.ImageField(upload_to='sliders/', max_length=500)
    button_1 = models.CharField(max_length=255, blank=True, default='')
    url_1 = models.URLField(blank=True, default='')
    button_2 = models.CharField(max_length=255, blank=True, default='')
    url_2 = models.URLField(blank=True, default='')
    button_3 = models.CharField(max_length=255, blank=True, default='')
    url_3 = models.URLField(blank=True, default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'Банер'
        verbose_name_plural = 'Банери'
        default_permissions = ()




def get_wallpaper_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'pages/{instance}/wallpaper{ext}'

class Webpage(models.Model):
    BASIC_DETAIL = 'basic_detail'
    BASIC_WITH_TABS = 'basic_with_tabs'
    # separator
    BASIC_LIST = 'basic_list'
    BLOG_LIST = 'blog_list'
    BLOG_DETAIL = 'blog_detail'
    CARD_LIST = 'card_list'
    COUNCIL = 'council'
    CUSTOM_DETAIL = 'custom_detail'
    CUSTOM_LIST = 'custom_list'
    PERSON_DETAIL = 'person_detail'
    FULL_WIDTH_DETAIL = 'full_width_detail'

    DESIGN_CHOICES = (
        (BASIC_DETAIL, 'Basic Detail'),
        (BASIC_WITH_TABS, 'Basic With Tabs'),
        # separator
        (BASIC_LIST, 'Basic List'),
        (BLOG_LIST, 'Blog List'),
        (BLOG_DETAIL, 'Blog Detail'),
        (CARD_LIST, 'Card List'),
        (COUNCIL, 'Вчена рада'),
        (CUSTOM_DETAIL, 'Custom Detail'),
        (CUSTOM_LIST, 'Custom List'),
        (PERSON_DETAIL, 'Person Detail'),
        (FULL_WIDTH_DETAIL, 'Full Width Detail'),
    )
    # For IT department
    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='pages', null=True, blank=True)
    slug = models.CharField(max_length=255, blank=True)
    design = models.CharField(max_length=255, choices=DESIGN_CHOICES, default=BASIC_DETAIL)
    temp_pk = models.IntegerField(null=True, blank=True)
    sidebar_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    # For general users
    title = models.CharField(max_length=255)
    wallpaper = models.ImageField(upload_to=get_wallpaper_path, null=True, blank=True, max_length=500)
    phone = models.CharField(max_length=255, blank=True, default='')
    email = models.CharField(max_length=255, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    content = HTMLField(blank=True, default='')
    content_2 = HTMLField(blank=True, default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'Web-сторінка'
        verbose_name_plural = 'Web-сторінки'
        unique_together = ('parent', 'slug')
        default_permissions = ()
        permissions = [
            ('view', 'Can view page'),
            ('edit', 'Can edit page'),
            ('add', 'Can add page'),
            ('delete', 'Can delete page'),
        ]
    def __str__(self):
        return f"{self.parent}/{self.slug}" if self.parent else f"{self.slug}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = Utils.slugify(self.title)
        super().save(*args, **kwargs)

    def get_edit_url(self):
        return reverse('page:edit_url', kwargs={'pk': self.id})

    def get_detail_url(self):
        return f'/{self}'

    def get_design(self):
        return dict(self.DESIGN_CHOICES).get(self.design)


class WebpageRows(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE, related_name='rows')
    col1 = models.CharField(max_length=255, blank=True, default='')
    col2 = models.CharField(max_length=255, blank=True, default='')
    col3 = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['id']
        verbose_name = 'Таблиця сторінки'
        verbose_name_plural = 'Таблиці сторінок'
        default_permissions = ()

class WebpageDocs(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE, related_name='docs')
    title = models.CharField(max_length=255)
    url = models.URLField()

    class Meta:
        ordering = ['id']
        verbose_name = 'Документ сторінки'
        verbose_name_plural = 'Документи сторінок'
        default_permissions = ()