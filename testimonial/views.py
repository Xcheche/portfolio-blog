from django.shortcuts import redirect, render
from django.urls import reverse

from Common.email import send_testimonial_submitted_notifications
from testimonial.forms import TestimonialForm
from testimonial.models import Testimonial

# Create your views here.



def create_testimonial(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.is_approved = False  # Set to False initially
            #bad words  functionality is already implemented in the form's clean_message method, so we don't need to handle it here.
            testimonial.save()
            # Send notifications to user and admins about new testimonial submission.
            send_testimonial_submitted_notifications(testimonial)
            

            return redirect(f"{reverse('home')}#testimonial-section")
    else:
        form = TestimonialForm()
        
    return render(request, "testimonial/create_testimonial.html", {"form": form})    