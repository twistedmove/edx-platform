from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from openedx.core.djangoapps.user_api.accounts import NAME_MIN_LENGTH
from openedx.core.djangoapps.user_api.serializers import ReadOnlyFieldsSerializerMixin

from student.models import UserProfile, LanguageProficiency
from .helpers import get_profile_image_url_for_user, PROFILE_IMAGE_SIZES_MAP

PROFILE_IMAGE_KEY_PREFIX = 'image_url'


class LanguageProficiencySerializer(serializers.ModelSerializer):
    """
    Class that serializes the LanguageProficiency model for account
    information.
    """
    class Meta:
        model = LanguageProficiency
        fields = ("code",)

    def get_identity(self, data):
        """
        This is used in bulk updates to determine the identity of an object.
        The default is to use the id of an object, but we want to override that
        and consider the language code to be the canonical identity of a
        LanguageProficiency model.
        """
        try:
            return data.get('code', None)
        except AttributeError:
            return None


class AccountUserSerializer(serializers.HyperlinkedModelSerializer, ReadOnlyFieldsSerializerMixin):
    """
    Class that serializes the portion of User model needed for account information.
    """
    class Meta:
        model = User
        fields = ("username", "email", "date_joined", "is_active")
        read_only_fields = ("username", "email", "date_joined", "is_active")
        explicit_read_only_fields = ()


class AccountLegacyProfileSerializer(serializers.HyperlinkedModelSerializer, ReadOnlyFieldsSerializerMixin):
    """
    Class that serializes the portion of UserProfile model needed for account information.
    """
    profile_image = serializers.SerializerMethodField("get_profile_image")
    language_proficiencies = LanguageProficiencySerializer(many=True, allow_add_remove=True, required=False)

    class Meta:
        model = UserProfile
        fields = (
            "name", "gender", "goals", "year_of_birth", "level_of_education", "country",
            "mailing_address", "bio", "profile_image", "language_proficiencies"
        )
        # Currently no read-only field, but keep this so view code doesn't need to know.
        read_only_fields = ()
        explicit_read_only_fields = ("profile_image",)

    def validate_name(self, attrs, source):
        """ Enforce minimum length for name. """
        if source in attrs:
            new_name = attrs[source].strip()
            if len(new_name) < NAME_MIN_LENGTH:
                raise serializers.ValidationError(
                    "The name field must be at least {} characters long.".format(NAME_MIN_LENGTH)
                )
            attrs[source] = new_name

        return attrs

    def validate_language_proficiencies(self, attrs, source):
        """ Enforce all languages are unique. """
        language_proficiencies = [language for language in attrs.get(source, [])]
        unique_language_proficiencies = set(language.code for language in language_proficiencies)
        if len(language_proficiencies) != len(unique_language_proficiencies):
            raise serializers.ValidationError("The language_proficiencies field must consist of unique languages")
        return attrs

    def transform_gender(self, obj, value):
        """ Converts empty string to None, to indicate not set. Replaced by to_representation in version 3. """
        return AccountLegacyProfileSerializer.convert_empty_to_None(value)

    def transform_country(self, obj, value):
        """ Converts empty string to None, to indicate not set. Replaced by to_representation in version 3. """
        return AccountLegacyProfileSerializer.convert_empty_to_None(value)

    def transform_level_of_education(self, obj, value):
        """ Converts empty string to None, to indicate not set. Replaced by to_representation in version 3. """
        return AccountLegacyProfileSerializer.convert_empty_to_None(value)

    @staticmethod
    def convert_empty_to_None(value):
        """ Helper method to convert empty string to None (other values pass through). """
        return None if value == "" else value

    def get_profile_image(self, obj):
        """ Returns metadata about a user's profile image. """
        data = {'has_image': obj.has_profile_image}
        data.update({
            '{image_key_prefix}_{size}'.format(image_key_prefix=PROFILE_IMAGE_KEY_PREFIX, size=size_display_name):
            get_profile_image_url_for_user(obj.user, size_value)
            for size_display_name, size_value in PROFILE_IMAGE_SIZES_MAP.items()
        })
        return data
