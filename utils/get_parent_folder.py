# Derive a short slug for the project parent folder from the first URL in the story, or default to 'project
import re

def get_parent_folder(high_level_story):
    """Derive and return a short slug for the project parent folder from the first URL in the story, or default to 'project'"""
    m = re.search(r'https?://([^/\s\)\"]+)', high_level_story)

    if m:
        raw = m.group(1)
        slug = re.sub(r'[^0-9a-zA-Z]+', '', raw).strip('_')
    else:
        slug = 'project'

    parent_folder = f"autogen/{slug}"
    return parent_folder