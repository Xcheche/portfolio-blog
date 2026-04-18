
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


logger = logging.getLogger(__name__)



# Convert email input to a clean list of addresses.
def _to_email_list(value):
    if not value:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [item for item in value if item]



# Build the admin/owner recipient list from project settings.
def _admin_recipients(setting_name=None):
    recipients = []

    if setting_name:
        recipients.extend(_to_email_list(getattr(settings, setting_name, [])))

    recipients.extend(_to_email_list(getattr(settings, "ADMIN_NOTIFICATION_EMAILS", [])))

    for admin in getattr(settings, "ADMINS", []):
        if isinstance(admin, (list, tuple)) and len(admin) >= 2 and admin[1]:
            recipients.append(admin[1])

    default_from = getattr(settings, "DEFAULT_FROM_EMAIL", "")
    if default_from:
        recipients.append(default_from)

    # Keep order and remove duplicates.
    return list(dict.fromkeys(recipients))



# Send an email with optional HTML template and text fallback.
def send_email(subject, email_to, html_template=None, context=None, text_body="", fail_silently=True):
    recipients = _to_email_list(email_to)
    if not recipients:
        return False

    html_content = None
    if html_template:
        try:
            html_content = render_to_string(html_template, context or {})
        except Exception:
            logger.exception("Failed rendering template '%s'", html_template)

    body = text_body or strip_tags(html_content or "") or subject

    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        to=recipients,
    )
    if html_content:
        message.attach_alternative(html_content, "text/html")

    try:
        message.send(fail_silently=fail_silently)
        return True
    except Exception:
        logger.exception("Failed sending email '%s'", subject)
        return False



# Notify user and admins when a new testimonial is submitted.
def send_testimonial_submitted_notifications(testimonial):
    context = {"testimonial": testimonial}

    user_subject = "Thanks for your testimonial"
    send_email(
        user_subject,
        [testimonial.email],
        html_template="emails/testimonial_submitted_user.html",
        context=context,
    )
# Notify owner/admin about new testimonial submission.
    admin_subject = "New testimonial submitted"
    send_email(
        admin_subject,
        _admin_recipients("TESTIMONIAL_NOTIFICATION_EMAILS"),
        html_template="emails/testimonial_submitted_admin.html",
        context=context,
    )



# Notify user when their testimonial is approved.
def send_testimonial_approved_email(testimonial):
    subject = "Your testimonial was approved"
    send_email(
        subject,
        [testimonial.email],
        html_template="emails/testimonial_approved_user.html",
        context={"testimonial": testimonial},
    )



# Read a contact field from dict input or object attributes.
def _contact_value(contact, key, default=""):
    if isinstance(contact, dict):
        return contact.get(key, default)
    return getattr(contact, key, default)



# Send contact confirmation to sender and notification to admins.
def send_contact_notifications(contact):
    name = _contact_value(contact, "name", "there")
    email = _contact_value(contact, "email", "")
    subject_value = _contact_value(contact, "subject", "")
    message = _contact_value(contact, "message", "")
    context = {
        "name": name,
        "email": email,
        "subject": subject_value,
        "message": message,
    }

    if email:
        send_email(
            subject="Thanks for reaching out",
            email_to=[email],
            html_template="emails/contact_thank_you_user.html",
            context=context,
        )
# Notify owner/admin about new contact form submission.
    send_email(
        subject="New contact form submission",
        email_to=_admin_recipients("CONTACT_NOTIFICATION_EMAILS"),
        html_template="emails/contact_submitted_admin.html",
        context=context,
    )