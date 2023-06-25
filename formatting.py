def to_html(input: str):
    # replace newlines with paragraph breaks (html)
    html = input.replace("\n", "<br/>").replace("\t", "&emsp;")
    return html


def bold_face(input: str):
    return f"<b>{input}</b>"


def italics(input: str):
    return f"<i>{input}</i>"
