from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.db import models
import os
from .models import Webpage


@receiver(pre_save, sender=Webpage)
def page_pre_save_signal(sender, instance, **kwargs):
	# HERE WE MAKE SURE THAT THE OLD WALLPAPER FILE IS DELETED IF IT IS CHANGED
	if instance.pk:
		webpage = Webpage.objects.get(pk=instance.pk)
		if webpage.wallpaper:
			if webpage.wallpaper != instance.wallpaper:
				if os.path.exists(webpage.wallpaper.path):
					os.remove(webpage.wallpaper.path)

	# HERE WE MAKE SURE THAT THE ADMIN IS SET FOR THE CHILDREN
	if instance.parent and not instance.admin:
		instance.admin = instance.parent.admin
		if instance.pk:
			page = Webpage.objects.get(id=instance.id)
			children = page.children.filter(models.Q(admin__isnull=True) | models.Q(admin=page.admin))
			children.update(admin=instance.admin)
		
	
	# HERE WE MAKE SURE THAT THE DESIGN AND SIDEBAR EDITED ARE SET FOR THE CHILDREN
	if instance.parent and not instance.pk:
		siblings = instance.parent.children.all()
		if siblings.count() > 1:
			bro = siblings.first()
		else:
			bro = instance.parent
		instance.design = bro.design
		instance.sidebar_edited = bro.sidebar_edited


# @receiver(post_save, sender=Webpage)
# def page_post_save_signal(sender, instance, created, **kwargs):
# 	if created:
# 		siblings = instance.parent.children.all()
# 		if siblings.count() > 1:
# 			bro = siblings.first()
# 		else:
# 			bro = instance.parent
# 		instance.design = bro.design
# 		instance.sidebar_edited = bro.sidebar_edited
# 		instance.save()

@receiver(post_delete, sender=Webpage)
def page_post_delete_signal(sender, instance, **kwargs):
	if instance.wallpaper:
		if os.path.isfile(instance.wallpaper.path):
			os.remove(instance.wallpaper.path)

