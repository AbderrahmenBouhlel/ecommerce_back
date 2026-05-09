from uuid import uuid4
from django.utils.text import slugify





def build_unique_slug( name: str) -> str:
    base_slug = slugify(name) or "filter"
    # Append a 4-character random hex string
    # Results in: "my-filter-a1b2"
    suffix = uuid4().hex[:4]
    return f"{base_slug}-{suffix}"