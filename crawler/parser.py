"""
Here define parser functions to parse url and title

@Author : rcy17
@Date   : 2020/1/27
"""
from urllib.parse import urljoin


def title_in_attr_href_in_attr(url, node):
    """
    <a href="/related/url" title="the title">the shown title</a>
    """
    return {
        'title': node.get('title'),
        'url': urljoin(url, node.get('href')),
    }


def title_in_text_href_in_attr(url, node):
    """
    <a href="/related_url">the title</a>
    """
    return {
        'title': node.text.replace('\n', ' ').strip(),
        'url': urljoin(url, node.get('href')),
    }


def chongqing_parser(url, node):
    """
    <a href="/related_url">
        <span>date</span>
        <span title="the title">the shown title</span>
    </a>
    """
    return {
        'title': node.find('span').find_next_sibling().get('title'),
        'url': urljoin(url, node.get('href')),
    }


def henan_parser(url, node):
    """
    It seems that Henan has two list respectively ordered by time,
    so I should find the second list's first news
    """
    import re
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
    result = node
    last_date = pattern.search(node.text).group()
    while node.find_next_sibling():
        node = node.find_next_sibling()
        node_date = pattern.search(node.text).group()
        if node_date > last_date:
            result = node
            break
        last_date = node_date
    node = node.find('a')
    return {
        'title': node.text,
        'url': urljoin(url, node.get('href'))
    }