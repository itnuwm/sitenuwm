from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'status', 'published_date', 'created_at')
	list_filter = ('status', 'published_date', 'created_at', 'author')
	search_fields = ('title', 'content')
	prepopulated_fields = {'slug': ('title',)}
	date_hierarchy = 'published_date'
	ordering = ('-published_date', '-created_at')
	
	fieldsets = (
		('Основна інформація', {
			'fields': ('title', 'slug', 'author', 'status')
		}),
		('Зміст', {
			'fields': ('content',)
		}),
		('Дата публікації', {
			'fields': ('published_date',)
		}),
	)
