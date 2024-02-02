def create_button(ref, url):
    if not ref:
        ref = "No ref"
    return f'<a href="{url}" style="color: #0066cc; text-decoration: none; font-weight: bold;">{ref}</a>'

