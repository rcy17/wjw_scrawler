"""
Here define parser functions to parse url and title

@Author : rcy17
@Date   : 2020/1/27
"""
from urllib.parse import urljoin
import re


def title_in_attr_href_in_attr(base, node):
    """
    <a href="/related/url" title="the title">the shown title</a>
    """
    return {
        'title': node.get('title'),
        'url': urljoin(base, node.get('href')),
    }


def title_in_text_href_in_attr(base, node):
    """
    <a href="/related_base">the title</a>
    """
    return {
        'title': node.text.replace('\n', ' ').strip(),
        'url': urljoin(base, node.get('href')),
    }


def chongqing_parser(base, node):
    """
    <a href="/related_base">
        <span>date</span>
        <span title="the title">the shown title</span>
    </a>
    """
    return {
        'title': node.find('span').find_next_sibling().get('title'),
        'url': urljoin(base, node.get('href')),
    }


def henan_parser(base, node):
    """
    It seems that Henan has two list respectively ordered by time,
    so I should find the second list's first news
    """
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
    node = result.find('a')
    return {
        'title': node.text,
        'url': urljoin(base, node.get('href'))
    }


def guizhou_parser(base, node):
    """
    Here we get JavaScript code, and I try to parser code like:
        var str_3 = "xxxx";
    """
    url, title = re.search(r'var str_1 = "(.*?)"[\s\S]*?var str_3 = "(.*?)"', node.text).groups()
    return {
        'title': title,
        'url': urljoin(base, url)
    }


def wuxi_parser(base, node):
    """
    <a href="/related_base">
        <h3>the title</h3>
        <p>the content</p>
    </a>
    """
    return {
        'title': node.find('h3').text,
        'url': urljoin(base, node.get('href'))
    }
