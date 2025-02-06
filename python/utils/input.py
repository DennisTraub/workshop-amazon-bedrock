from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


def get_user_input():
    style = Style.from_dict({"hint": "#888888"})

    # noinspection PyBroadException
    try:
        prompt_session = PromptSession(style=style)
    except Exception:
        # Fallback for environments without proper console, e.g. debugger
        return input(">>> ").strip()

    placeholder = FormattedText([
        (">>> ", ""),
        ("class:hint", "Send a message (/x to exit)")
    ])

    while True:
        text = prompt_session.prompt(">>> ", placeholder=placeholder)
        if text.strip():
            return text
