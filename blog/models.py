from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField
from django_resized import ResizedImageField
from pages.utils import Utils


class Post(models.Model):
	NEWS = 'news'
	ANNOUNCEMENT = 'announcement'
	
	KIND_CHOICES = [
		(NEWS, 'Новина'),
		(ANNOUNCEMENT, 'Оголошення'),
	]

	title = models.CharField(max_length=64, verbose_name='Заголовок')
	slug = models.SlugField(max_length=255, unique=True, verbose_name='URL', blank=True)
	kind = models.CharField(max_length=64, choices=KIND_CHOICES, default=NEWS, verbose_name='Новина чи оголошення?')
	wallpaper = ResizedImageField(size=[1024, 768], crop=['middle', 'center'], upload_to='news/', verbose_name='Обкладинка')
	content = HTMLField(blank=True, default='', verbose_name='Зміст')
	author = models.CharField(max_length=255, verbose_name='Автор')

	date_created = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
	date_published = models.DateTimeField(verbose_name='Дата публікації')
	date_updated = models.DateTimeField(auto_now=True, verbose_name='Оновлено')

	is_published = models.BooleanField(default=False, verbose_name='Опубліковано')
	
	class Meta:
		ordering = ['-date_published']
		verbose_name = 'Пост'
		verbose_name_plural = 'Пости'
	
	def __str__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = Utils.slugify(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'slug': self.slug})
	
	def get_kind(self):
		return dict(self.KIND_CHOICES).get(self.kind)