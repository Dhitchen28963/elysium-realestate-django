import re
import bleach
from html import unescape

def replace_font_with_span(html):
    # Replace <font color="#...">...</font> with <span style="color:...;">...</span>
    font_open_tag_pattern = re.compile(r'<font\s+color="([^"]+)">')
    font_close_tag_pattern = re.compile(r'</font>')
    
    # Replace opening font tags
    html = font_open_tag_pattern.sub(r'<span style="color:\1;">', html)
    # Replace closing font tags
    html = font_close_tag_pattern.sub('</span>', html)
    
    return html

def clean_html_content(html):
    
    # Unescape HTML entities
    html = unescape(html)

    allowed_tags = [
        'p', 'b', 'i', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'span', 'ul', 'ol', 'li', 'strong', 'br', 'em', 'blockquote', 'a'
    ]
    allowed_attrs = {
        'span': ['style'],
        'a': ['href', 'title', 'style'],
        '*': ['style']
    }

    allowed_styles = ['color']

    # Replace <font> tags with <span> tags
    html = replace_font_with_span(html)

    # Sanitize the HTML
    cleaned_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, styles=allowed_styles, strip=False)

    # Remove empty style attributes and trailing spaces
    cleaned_html = re.sub(r'style="\s*"', '', cleaned_html)
    cleaned_html = re.sub(r'\s+>', '>', cleaned_html)

    return cleaned_html
