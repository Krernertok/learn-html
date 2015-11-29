import unittest
from app.tagnames import tagnames

class TagNameTestCase(unittest.TestCase):
    def test_get_definition(self):
        self.assertEquals("Specifies a hyperlink", 
            tagnames.get_definition("a"))
        self.assertEquals(None, tagnames.get_definition("x"))

    def test_get_remaining_tag_names(self):
        answered_tag_names = ["!DOCTYPE", "a", "abbr", "address", "area", 
        "article", "aside", "audio", "b", "base", "bdi", "bdo"]
        remaining_tags = {
            "blockquote": "Specifies a long quotation",
            "body": "Specifies the body element",
            "br": "Inserts a single line break",
            "button": "Specifies a push button",
            "canvas": "Define graphics",
            "caption": "Specifies a table caption",
            "cite": "Specifies a citation",
            "code": "Specifies computer code text",
            "col": "Specifies attributes for table columns ",
            "colgroup": "Specifies groups of table columns",
            "data": "Allows for machine-readable data to be provided",
            "datalist": "Specifies an \"autocomplete\" dropdown list",
            "dd": "Specifies a definition description",
            "del": "Specifies deleted text",
            "details": "Specifies details of an element",
            "dfn": "Defines a definition term",
            "dialog": "Specifies that part of an application is interactive.",
            "div": "Specifies a section in a document",
            "dl": "Specifies a definition list",
            "dt": "Specifies a definition term",
            "em": "Specifies emphasized text ",
            "embed": "Specifies external application or interactive content",
            "fieldset": "Specifies a fieldset",
            "figcaption": "Specifies caption for the figure element.",
            "figure": "Specifies a group of media content,and their caption",
            "footer": "Specifies a footer for a section or page",
            "form": "Specifies a form ",
            "h1": "Specifies a heading level 1",
            "h2": "Specifies a heading level 2",
            "h3": "Specifies a heading level 3",
            "h4": "Specifies a heading level 4",
            "h5": "Specifies a heading level 5",
            "h6": "Specifies a heading level 6",
            "head": "Specifies information about the document",
            "header": "Specifies a group of introductory or navigational aids,including hgroup elements",
            "hgroup": "Specifies a header for a section or page.\nNOTE:  This element has been dropped from W3C HTML5 spec but it is still included in WHATWG Living Standard.\n\n",
            "hr": "Specifies a horizontal rule",
            "html": "Specifies an html document",
            "i": "Specifies italic text",
            "iframe": "Specifies an inline sub window (frame)",
            "img": "Specifies an image",
            "input": "Specifies an input field",
            "ins": "Specifies inserted text",
            "kbd": "Specifies keyboard text",
            "keygen": "Generates a key pair",
            "label": "Specifies a label for a form control",
            "legend": "Specifies a title in a fieldset",
            "li": "Specifies a list item",
            "link": "Specifies a resource reference",
            "main": "Specifies the main content area of an HTML document.",
            "map": "Specifies an image map ",
            "mark": "Specifies marked text",
            "menu": "Specifies a menu list",
            "menuitem": "Specifies a command that a user can invoke from a popup menu.",
            "meta": "Specifies meta information",
            "meter": "Specifies measurement within a predefined range",
            "nav": "Specifies navigation links",
            "noscript": "Specifies a noscript section",
            "object": "Specifies an embedded object",
            "ol": "Specifies an ordered list",
            "optgroup": "Specifies an option group",
            "option": "Specifies an option in a drop-down list",
            "output": "Specifies some types of output",
            "p": "Specifies a paragraph",
            "param": "Specifies a parameter for an object",
            "pre": "Specifies preformatted text",
            "progress": "Specifies progress of a task of any kind",
            "q": "Specifies a short quotation",
            "rb": "Marks the base text component of a ruby annotation.",
            "rp": "Used for the benefit of browsers that don't support ruby annotations",
            "rt": "Specifies the ruby text component of a ruby annotation.",
            "rtc": "Marks a ruby text container for ruby text components in a ruby annotation.",
            "ruby": "Specifies a ruby annotation (used in East Asian typography)",
            "s": "Indicates text that's no longer accurate or relevant.",
            "samp": "Specifies sample computer code",
            "script": "Specifies a script",
            "section": "Specifies a section",
            "select": "Specifies a selectable list",
            "small": "Specifies small text",
            "source": "Specifies media resources",
            "span": "Specifies a section in a document",
            "strong": "Specifies strong text",
            "style": "Specifies a style definition",
            "sub": "Specifies subscripted text",
            "summary": "Specifies a summary / caption for the <details> element",
            "sup": "Specifies superscripted text",
            "table": "Specifies a table",
            "tbody": "Specifies a table body",
            "td": "Specifies a table cell",
            "template": "Declares HTML fragments that can be cloned and inserted in the document by script.",
            "textarea": "Specifies a text area",
            "tfoot": "Specifies a table footer",
            "th": "Specifies a table header",
            "thead": "Specifies a table header",
            "time": "Specifies a date/time",
            "title": "Specifies the document title",
            "tr": "Specifies a table row",
            "track": "Specifies a text track for media such as video and audio",
            "u": "Specifies text with a non-textual annotation.",
            "ul": "Specifies an unordered list",
            "var": "Specifies a variable",
            "video": "Specifies a video",
            "wbr": "Specifies a line break opportunity for very long words and strings of text with no spaces."
        }
        self.assertEquals(remaining_tags, 
            tagnames.get_remaining_tags(answered_tag_names))
