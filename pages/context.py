from pages.models import Webpage

def navbar(request):
    return {"navbar": Webpage.objects.filter(parent=None)}