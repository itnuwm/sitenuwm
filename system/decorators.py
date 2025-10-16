from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def perms_required(perm):
	def inner(request, *args, **kwargs):
		perms = (perm,) if isinstance(perm, str) else perm
		if not request.is_anonymous:
			if request.is_authenticated:
				if request.has_perms(perms):
					return True
				else:
					raise PermissionDenied
		return False
	return user_passes_test(inner, login_url=None)