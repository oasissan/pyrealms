from pathlib import Path

import markdown
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


def render_md(text: str) -> str:
    """Render Markdown (fenced code + tables) to HTML. Shared by the page
    routers and available as the ``md`` Jinja filter for inline content like
    quiz prompts and explanations."""
    return markdown.markdown(text or "", extensions=["fenced_code", "tables"])


templates.env.filters["md"] = render_md
