from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, FileExtensionValidator, MaxValueValidator


def validate_file_size(file):
    max_size_kb = 2000

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_kb}kb')



percentage_validator = [MinValueValidator(0), MaxValueValidator(100)]
