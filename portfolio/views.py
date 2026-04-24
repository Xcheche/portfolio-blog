from django.shortcuts import redirect, render, get_object_or_404

from contact.models import Contact
from portfolio.models import Portfolio, Category
from django.core.paginator import Paginator as Paginator  
from accounts.models import CustomUser
from testimonial.models import Testimonial
from django.contrib import messages
from Common.email import send_contact_notifications

# Create your views here.

# helpers.py
from django.core.exceptions import ValidationError

def validate_contact_form(data):
    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    subject = (data.get('subject') or '').strip()
    message = (data.get('message') or '').strip()

    errors = [] # Append every validation error to this list and raise them together at the end for better user experience.
    bad_words = ['fuck you', 'scammer', 'poor','not good','slow','expensive','monkey'] #example bad words 
    if any(bad_word in message.lower() for bad_word in bad_words):
        errors.append("Message contains inappropriate language.")
    if not name:
        errors.append("Name is required.")
    if not email:
        errors.append("Email is required.")
    elif '@' not in email:
        errors.append("Enter a valid email address.")
    if not subject:
        errors.append("Subject is required.")
    if not message:
        errors.append("Message cannot be empty.")

    if errors:
        raise ValidationError(errors)
    
    
    return {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    }

# --------------------------Home view-----------------------------
def home(request):
    # Pagination and filtering for portfolio listing on home page
    
    portfolios = Portfolio.objects.filter(is_deleted=False, status="published").order_by("-created_at")
    paginator = Paginator(portfolios, 3)  # Show 3 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Use logged-in user profile in session; for public visitors use the owner profile.
    owner_profile = CustomUser.objects.filter(is_superuser=True).order_by("id").first()
    if owner_profile is None:
        owner_profile = CustomUser.objects.order_by("id").first()
    profile_user = request.user if request.user.is_authenticated else owner_profile
    testimonials = Testimonial.objects.filter(is_approved=True).order_by("-created_at")


    # Process contact form only on submit.
    if request.method == "POST":
        try:
            cleaned_data = validate_contact_form(request.POST)
            # Save to DB.
            Contact.objects.create(**cleaned_data)
            messages.success(request, "Your message has been sent successfully.")
            # Send email from contact form to site owner/admins.
            send_contact_notifications(cleaned_data)
            return redirect('home')
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)

    context = {
        "portfolios": portfolios,
        "page_obj": page_obj,
        "profile_user": profile_user,
        "testimonials": testimonials,
    }
    return render(request, "portfolio/index.html", context)


# Detail page using django slug for better seo and user-friendly urls
def detail(request,slug):
    
    portfolio =get_object_or_404(Portfolio,slug=slug, is_deleted=False, status="published")
    context = {
        "portfolio": portfolio,
    }
    return render(request, "portfolio/detail.html", context)



# Category view with slug for portfolio category filtering
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug, is_deleted=False)
    
    portfolios = Portfolio.objects.filter(
        category=category,
        is_deleted=False,
        status="published",
    ).order_by("-created_at")
    context = {
        "category": category,
        "portfolios": portfolios,
 
    }
    return render(request, "portfolio/category.html", context)


