import unittest
from real_estate.utils import replace_font_with_span, clean_html_content
import re

class UtilsTestCase(unittest.TestCase):

    def normalize_style_whitespace(self, html):
        # Normalize the whitespace in style attributes
        return re.sub(r'style="\s*([^"]*?)\s*"', lambda m: f'style="{m.group(1).replace(" ", "")}"', html)

    def test_replace_font_with_span(self):
        html_input = '<font color="#ff0000">This is red text</font>'
        expected_output = '<span style="color:#ff0000;">This is red text</span>'
        self.assertEqual(replace_font_with_span(html_input), expected_output)

        html_input = '<p>Normal text <font color="#00ff00">green text</font></p>'
        expected_output = '<p>Normal text <span style="color:#00ff00;">green text</span></p>'
        self.assertEqual(replace_font_with_span(html_input), expected_output)

        html_input = 'Text without font tags'
        expected_output = 'Text without font tags'
        self.assertEqual(replace_font_with_span(html_input), expected_output)

    def test_clean_html_content(self):
        html_input = '<p>This is <font color="#ff0000">red text</font> and <b>bold text</b>.</p>'
        expected_output = '<p>This is <span style="color:#ff0000;">red text</span> and <b>bold text</b>.</p>'
        actual_output = clean_html_content(html_input)
        self.assertEqual(self.normalize_style_whitespace(actual_output), self.normalize_style_whitespace(expected_output))

        html_input = '<h1>Title</h1>'
        expected_output = '<h1>Title</h1>'
        self.assertEqual(clean_html_content(html_input), expected_output)

        html_input = '<a href="http://example.com" style="color:#ff0000;">link</a>'
        expected_output = '<a href="http://example.com" style="color:#ff0000;">link</a>'
        actual_output = clean_html_content(html_input)
        self.assertEqual(self.normalize_style_whitespace(actual_output), self.normalize_style_whitespace(expected_output))

        html_input = '<span style="font-size:20px;">Text with disallowed style</span>'
        expected_output = '<span>Text with disallowed style</span>'
        actual_output = clean_html_content(html_input)
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
