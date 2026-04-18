from django import forms
from django.forms import ModelForm  

from testimonial.models import Testimonial


class TestimonialForm(ModelForm):
    class Meta:
        model = Testimonial
        fields = ['full_name', 'email', 'role', 'message', 'project_name', 'permission_to_publish', 'testimonial_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = "form-control"
        for field_name in ['full_name', 'email', 'role', 'message', 'project_name', 'permission_to_publish']:
            self.fields[field_name].widget.attrs.update({'class': base_class})
        self.fields['testimonial_image'].widget.attrs.update({'class': base_class})

        #Clean data email field
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "@" not in email or not email.endswith(".com"):
            raise forms.ValidationError("Please enter a valid email address ending with '.com'.")
        return email
    
    # filter bad words in message field
    def clean_message(self):
        message = self.cleaned_data.get('message')
        bad_words = ['fuck you', 'scammer','monkey', 'poor','not good','slow','expensive']  # Replace with actual bad words
        for bad_word in bad_words:
            if bad_word in message.lower():
                raise forms.ValidationError("Please remove inappropriate language from your message.")
        return message