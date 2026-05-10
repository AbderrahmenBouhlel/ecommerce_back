import re

from core.exceptions.excecptions import RequestValidationException


class GetCategoryCatalogRequestDTO:
    def __init__(self, category_slug: object):
        self.category_slug = self._validate_category_slug(category_slug)

    @classmethod
    def from_path(cls, category_slug: object):
        return cls(category_slug=category_slug)

    def _validate_category_slug(self, value: object) -> str:
        if not isinstance(value, str):
            raise RequestValidationException(message="Category slug is required.", cause=None)

        slug = value.strip()
        if not slug:
            raise RequestValidationException(message="Category slug is required.", cause=None)

        if len(slug) > 50:
            raise RequestValidationException(message="Category slug must not exceed 50 characters.", cause=None)

        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            raise RequestValidationException(message="Category slug format is invalid.", cause=None)

        return slug
