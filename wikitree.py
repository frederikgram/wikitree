""" """

import os
import sys

from typing import List, Iterator
from requests_html import HTMLSession
from dataclasses import dataclass, field

session = HTMLSession()

@dataclass
class Node:
    """ Simple data structure for storing tree nodes """

    self.link: str
    self.parent: Node = field(default=None)
    self.children: List[Node] = field(default_factory=list)


def get_links(url: str) -> Iterator[str]:
    """ yield absolute links founds in the given url,
        if the link contains BASE_PATH and is not 
        a link to itself.
    """

    r = session.get(_url)

    for link in r.html.absolute_links:
        if BASE_PATH in link and ":" not in link[len(BASE_PATH):] and link != url:
            yield link


def generate_tree(root: Node, max_depth: int=0):
    """ Breadth First Search algorithm
        used to generate a node-relation
        structure, from the links
        found in the given absolute link.
    """

    nodes = []
    stack = [root]
    depth = 0

    links_per_article = 5

    # Set default value for tree depth
    if max_depth == 0:
        max_depth = links_per_article ** 3

    # Generate nodes using Breadth First Search
    while stack and max_depth is None or depth < max_depth:
        c_node = stack[0]
        stack = stack[1:]

        nodes.append(c_node)
        for link in get_links(c_node.link)[:links_per_article]:
            n = Node(link=link, parent=c_node)
            stack.append(n)
            c_node.children.append(n)

        depth += 1


def visualize(node: Node, indent: int=0):
    """ Recursive Depth First Search,
        Visualizes a tree structures
        to stdout using sys.stdout.write
    """
    sys.stdout.write("[{0}] {1}: {2}\n".format(str(indent // 2), '-' * indent, node.link))

    indent += 2
    for child in _node.children:
        visualize(child, indent=indent)


if __name__ == "__main__":

    lang = "en"
    BASE_PATH = "https://{lang}.wikipedia.org/wiki/".format(lang=lang)

    query = input("Topic: ") or "physics"
    query.replace(' ', '_')

    url = os.path.join(BASE_PATH, query)

    root = Node(link=url)
    generate_tree(root)

    visualize(root)
    sys.stdout.write("\n [n] symbolises article depth from [0] root")

    session.close()
