
def get_user_story(path):
    """Read and return the high-level user story from the markdown file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            high_level_story = f.read()
    except Exception:
        high_level_story = "<UNAVAILABLE docs/parabank_user_story.md>"
    return high_level_story