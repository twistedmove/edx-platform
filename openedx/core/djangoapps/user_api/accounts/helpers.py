"""
Helper functions for the accounts API.
"""
import hashlib

from django.conf import settings
from django.core.files.storage import FileSystemStorage, get_storage_class

PROFILE_IMAGE_SIZES_MAP = {
    'full': 500,
    'large': 120,
    'medium': 50,
    'small': 30
}
_PROFILE_IMAGE_SIZES = PROFILE_IMAGE_SIZES_MAP.values()


def get_profile_image_storage():
    """
    Configures and returns a django Storage instance that can be used
    to physically locate, read and write profile images.
    """
    storage_class = get_storage_class(settings.PROFILE_IMAGE_BACKEND)
    return storage_class(base_url=(settings.PROFILE_IMAGE_DOMAIN + settings.PROFILE_IMAGE_URL_PATH))


def get_profile_image_name(username):
    """
    Returns the prefix part of the filename used for all profile images.
    """
    return hashlib.md5(settings.PROFILE_IMAGE_SECRET_KEY + username).hexdigest()


def get_profile_image_filename(name, size):
    """
    Returns the full filename for a profile image, given the name prefix and
    size.
    """
    return '{name}_{size}.jpg'.format(name=name, size=size)


def get_profile_image_names(username):
    """
    Return a dict {size:filename} for each profile image for a given username.
    """
    name = get_profile_image_name(username)
    return {size: get_profile_image_filename(name, size) for size in _PROFILE_IMAGE_SIZES}


def get_profile_image_urls(user):
    """
    Return a dict {size:url} for each profile image for a given image name.
    Note that based on the value of django.conf.settings.PROFILE_IMAGE_DOMAIN,
    the URL may be relative, and in that case the caller is responsible for
    constructing the full URL if needed.

    Arguments:
        name (str): the base name for the requested profile image.

    Returns:
        dictionary of {size_display_name: url} for each image.

    Raises:
        ValueError: The caller asked for an unsupported image size.

    """
    if user.profile.has_profile_image:
        name = get_profile_image_name(user.username)
    else:
        name = settings.PROFILE_IMAGE_DEFAULT_FILENAME
    storage = get_profile_image_storage()

    return {
        size_display_name: storage.url(get_profile_image_filename(name, size))
        for size_display_name, size in PROFILE_IMAGE_SIZES_MAP.items()
    }
