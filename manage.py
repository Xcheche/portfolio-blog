#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def main():
    """Run administrative tasks."""
    if os.getenv("DEBUG", "True") == "True":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
#TODO:Testing portfolio,contact and testimonial apps. Add more tests for accounts app. Add pagination to portfolio app. Add search functionality to portfolio app. Add categories/tags to portfolio app. Add user profiles with profile pictures and bios. Add social media links to user profiles. Add a blog section to share updates and news. Implement a more robust contact form with CAPTCHA and file attachments. Add an admin dashboard for managing testimonials and contact messages.
#TODO:Implement reacptcha for contact and testimonial,share by email,share by id functionality for portfolio items,add categories/tags to portfolio items,add user profiles with profile pictures and bios,add social media links to user profiles,add a blog section to share updates and news,implement a more robust contact form with CAPTCHA and file attachments,add an admin dashboard for managing testimonials and contact messages.
#TODO:Implement nginx for static and media file serving,add caching for improved performance,add logging and monitoring for better error tracking,add unit tests and integration tests for better code quality,add CI/CD pipeline for automated testing and deployment,add Docker support for easier development and deployment,add support for multiple languages/localization,add accessibility features for better usability,add a dark mode option for better user experience.
#TODO:Docker,deployment,amazon ses,brevo domain name ,storage s3 bucket,cloudinary,imagekit,database for production neon db


## Blog implementation
### News letter