# Context processor for categories used in templates (e.g., portfolio filter menu)
from .models import Category



def categories(request):
    categories = Category.objects.order_by("name")
    return {
        "categories": categories,
    }