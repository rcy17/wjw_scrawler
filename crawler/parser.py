"""
Here define parser functions to parse url and title

@Author : rcy17
@Date   : 2020/1/27
"""


def title_in_attr_href_in_attr(url, node):
    """
    <a href="/related/url" title="the title">the shown title</a>
    """
    return {
        'title': node.get('title'),
        'url': url + node.get('href'),
    }


def title_in_text_href_in_attr(url, node):
    """
    <a href="/related_url">the title</a>
    """
    return {
        'title': node.text,
        'url': url + node.get('href'),
    }