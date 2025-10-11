import os
from typing import Optional
from langchain.tools import StructuredTool

def write_file(path: str, content: str) -> str:
    """Writes or creates a file in the local system."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"✅ File written successfully to {path}"

def get_writer_tool():
    writer_tool = StructuredTool.from_function(
        func=write_file,
        name="write_create_file",
        description=(
            "Writes or creates a file in the local system. "
            "Args: path (str): file path to save to; "
            "content (str): content to write to the file."
        ),
    )
    return writer_tool
