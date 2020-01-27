"""
Here define parser functions to parse url and title

@Author : rcy17
@Date   : 2020/1/27
"""
from urllib.parse import urljoin


def title_in_attr_href_in_attr(host, node):
    """
    <a href="/related/url" title="the title">the shown title</a>
    """
    return {
        'title': node.get('title'),
        'url': urljoin(host, node.get('href')),
    }


def title_in_text_href_in_attr(host, node):
    """
    <a href="/related_url">the title</a>
    """
    return {
        'title': node.text.replace('\n', ' ').strip(),
        'url': urljoin(host, node.get('href')),
    }


def chongqing_parser(host, node):
    """
    <a href="/related_url">
        <span>date</span>
        <span title="the title">the shown title</span>
    </a>
    """
    return {
        'title': node.find('span').find_next_sibling().get('title'),
        'url': urljoin(host, node.get('href')),
    }
