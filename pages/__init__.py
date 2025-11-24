# pages/__init__.py

from . import _1_Login
from . import _2_Identity
from . import _3_Menu
from . import _4_Interview
from . import _5_Result
from . import _6_Dashboard

# Central registry of pages
PAGES = {
    "login": _1_Login,
    "identity": _2_Identity,
    "menu": _3_Menu,
    "interview": _4_Interview,
    "result": _5_Result,
    "dashboard": _6_Dashboard
}

def render_page(page_name: str):
    """Call the render() of the page module by name."""
    page_module = PAGES.get(page_name)
    if page_module and hasattr(page_module, "render"):
        page_module.render()
    else:
        raise ValueError(f"Page '{page_name}' not found or has no render()")
