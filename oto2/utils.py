def remove_newlines(text):
    return ''.join(text.splitlines())

def filter_html(text):
    new_text = remove_newlines(text)
    new_text = new_text.replace('&nbsp;', '')
    new_text = new_text.replace('&apos;', "'")

    return new_text
