from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField

class Post(models.Model):
	DRAFT = 'draft'
	PUBLISHED = 'published'
	
	STATUS_CHOICES = [
		(DRAFT, 'Чернетка'),
		(PUBLISHED, 'Опубліковано'),
	]
	
	title = models.CharField(max_length=255, verbose_name='Заголовок')
	slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
	content = HTMLField(blank=True, default='', verbose_name='Зміст')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
	published_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата публікації')
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено')
	updated_at = models.DateTimeField(auto_now=True, verbose_name='Оновлено')
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT, verbose_name='Статус')
	
	class Meta:
		ordering = ['-published_date', '-created_at']
		verbose_name = 'Пост'
		verbose_name_plural = 'Пости'
	
	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'slug': self.slug})
	
	def save(self, *args, **kwargs):
		if self.status == self.PUBLISHED and not self.published_date:
			self.published_date = timezone.now()
		super().save(*args, **kwargs)
