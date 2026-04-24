# Context processor for categories used in templates (e.g., portfolio filter menu)
from django.db.models import Count, Q

from .models import Category



def categories(request):
    categories = Category.objects.annotate(
        count=Count(
            "portfolios",
            filter=Q(portfolios__is_deleted=False, portfolios__status="published"),
        )
    ).order_by("name")
    return {
        "categories": categories,
    }