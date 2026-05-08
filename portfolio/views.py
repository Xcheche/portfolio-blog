from django.http import HttpResponse, FileResponse
from django.shortcuts import redirect, render, get_object_or_404
from types import SimpleNamespace
from django.contrib.auth import get_user_model

from django.urls import reverse

from contact.models import Contact
from portfolio.forms import EmailPortfolioForm
from portfolio.models import Portfolio, Category
from django.core.paginator import Paginator as Paginator  
from accounts.models import CustomUser
from testimonial.models import Testimonial
from django.contrib import messages
from Common.email import send_contact_notifications

from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from pathlib import Path
from django.core.mail import send_mail # For sending email notifications when sharing portfolio via email

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
    User = get_user_model()

    profile_user = (
        request.user if request.user.is_authenticated else
        User.objects.filter(is_superuser=True).order_by("id").first()
        or User.objects.order_by("id").first()
        or SimpleNamespace(
            display_name="Your Name",
            username="yourname",
            profile_image=None,
            default_image_url="/static/landing/images/person_1.jpg",
            bio="",
            whatsapp_link="",
        )
    )
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




# Share link generation view for non-email sharing of portfolio details
def generate_share_link(request, portfolio_id):
    """
    Generate shareable link for a portfolio post.
    
    Purpose:
    - Create absolute URL for sharing posts on social media
    - Allows easy sharing via email, social platforms, etc.
    
    Parameters:
    - portfolio_id: ID of the portfolio post to share
    
    Process:
    1. Get the portfolio post or return 404
    2. Build absolute URL (includes domain)
    3. Pass URL to template for display/copying
    
    Returns:
        Rendered template with shareable URL
    
    Usage:
    - Users can copy the link to share on social media
    - Link will work from any location (absolute URL)
    """
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    share_url = request.build_absolute_uri(reverse('detail', args=[portfolio.slug]))
    return render(
        request,
        'portfolio/share_link_output.html',
        {
            'share_url': share_url,
            'portfolio_id': portfolio.id,
            'portfolio_title': portfolio.title,
        },
    )




# Link to download resume (assuming resume is stored in static files or media)
def resume(request):
    resume_path = "cv/python.pdf"
    # Use storage APIs to support various static file backends and avoid
    # requiring a filesystem path (works with collectstatic storage backends).
    if staticfiles_storage.exists(resume_path):
        f = staticfiles_storage.open(resume_path, 'rb')
        return FileResponse(f, content_type='application/pdf', as_attachment=True, filename='python.pdf')

    # Fallback: check the project's `static/` folder on disk (useful in dev).
    fs_path = Path(settings.BASE_DIR) / "static" / resume_path
    if fs_path.exists():
        return FileResponse(open(fs_path, 'rb'), content_type='application/pdf', as_attachment=True, filename='python.pdf')

    return HttpResponse("Resume not found", status=404)



# Share portfolio by email
def share_portfolio(request, portfolio_id):
    # Retrieve portfolio by id
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    sent = False
    share_url = request.build_absolute_uri(reverse('detail', args=[portfolio.slug]))

    if request.method == "POST":
        # Form was submitted
        form = EmailPortfolioForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data

            subject = (
                f"{cd['name']} shared a portfolio project with you"
            )
            comments = cd['comments'].strip() if cd['comments'] else "No additional comments."
            message = (
                f"Project: {portfolio.title}\n"
                f"Link: {share_url}\n\n"
                f"From: {cd['name']} ({cd['email']})\n"
                f"Comment: {comments}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[cd["to"]],
                fail_silently=False,
            )
            sent = True

    else:
        form = EmailPortfolioForm()
        context = {
            "portfolio": portfolio,
            "form": form,
            "sent": sent,
            "share_url": share_url,
        }
    return render(
        request,
        "portfolio/share.html",
        context,
    )
    