from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from Common.email import send_contact_notifications
from contact.models import Contact


# Validate and normalize contact form payload.
def validate_contact_form(data):
	name = (data.get("name") or "").strip()
	email = (data.get("email") or "").strip().lower()
	subject = (data.get("subject") or "").strip()
	message = (data.get("message") or "").strip()

	errors = []
	bad_words = ["fuck you", "scammer", "poor", "not good", "slow", "expensive", "monkey"]

	if any(bad_word in message.lower() for bad_word in bad_words):
		errors.append("Message contains inappropriate language.")
	if not name:
		errors.append("Name is required.")
	if not email:
		errors.append("Email is required.")
	elif "@" not in email:
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


# Receive contact form submit and return JSON response.
@require_POST
def submit_contact(request):
	try:
		cleaned_data = validate_contact_form(request.POST)
		Contact.objects.create(**cleaned_data)
		send_contact_notifications(cleaned_data)
		return JsonResponse({"ok": True, "message": "Message sent."})
	except ValidationError as exc:
		return JsonResponse({"ok": False, "errors": exc.messages}, status=400)
