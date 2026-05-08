from django import forms


# Form for sharing portfolio via email
class EmailPortfolioForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


    # Add CSS classes to form fields for styling
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = "form-control"
        for field_name in ['name', 'email', 'to', 'comments']:
            self.fields[field_name].widget.attrs.update({'class': base_class})
        self.fields['email'].widget.attrs.update({'class': base_class})


    # Clean comments field to filter out bad words
    def clean_comments(self):
        comments = self.cleaned_data.get("comments", "")
        # List of bad words to check for in the comments.
        bad_words = ["fuck you", "monkey", "fool"]  # Replace with actual bad words.
        for bad_word in bad_words:
            if bad_word in comments.lower():
                raise forms.ValidationError("Your comments contain inappropriate language. Please remove any offensive words and try again.")
        return comments
    

    # Clean email field to ensure it's valid
    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        if not email:
            raise forms.ValidationError("Email is required.")
        if '@' not in email:
            raise forms.ValidationError("Enter a valid email address.")
        return email
