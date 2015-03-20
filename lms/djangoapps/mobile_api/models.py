"""
A models.py is required to make this an app (until we move to Django 1.7)
"""
# pylint: disable=no-member

from django.db.models.fields import TextField

from config_models.models import ConfigurationModel


class MobileApiConfig(ConfigurationModel):
    """Configuration for the video upload feature."""
    video_profiles = TextField(
        blank=True,
        help_text="A comma-separated list of names of profiles to include in video encoding downloads."
    )

    @classmethod
    def get_video_profiles(cls):
        """Get the list of profiles to include in the encoding download"""
        return [profile for profile in cls.current().video_profiles.split(",") if profile]
