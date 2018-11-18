from requests_html import HTMLSession
import sys
import os

session = HTMLSession()

lang = input("language: ") or "en"
BASE_PATH = "https://{lang}.wikipedia.org/wiki/".format(lang=lang)

m_depth = 10


class Node:
    """ Simple data structure for storing tree nodes """

    def __init__(self, link: str, parent=None):
        self.parent = parent
        self.link = link
        self.children = []


def get_sublinks(url: str) -> list:
    """
    :param url: str(url) with base_path https://{lang}.wikipedia.org/wiki/
    :return: list of str(links)
    """
    r = session.get(url)

    return [link for link in r.html.absolute_links if  # Basic filtering included
            BASE_PATH in link and ":" not in link[len(BASE_PATH):] and link != url]


def generate_tree(root_node: Node) -> None or list:
    """ # Breadth First Search
    :param root_node: node of type Node
    :return: Generates a tree structures with max_depth from root_node
    """

    def _some_recursive_function(some_var: Node) -> None or Node:
        pass

    current_depth = 0

    pass


def visualize(node: Node, indent: int=0) -> None:
    """ # Recursive Depth First Search
    :param node: node of type Node
    :param indent: int(x) how many dashes should be added per depth level
    :return: Visualizes a tree structures to stdout using sys.stdout.write
    """
    sys.stdout.write("[{0}] {1}: {2}\n".format(str(indent // 2), '-'*indent, node.link))
    indent += 2
    for child in node.children:
        node.visualize(child, indent=indent)

# TODO breadth first search


if __name__ == "__main__":
    query = input("Root topic: ") or "Denmark"
    url = os.path.join(BASE_PATH, query)
    root_node = Node(link=url)

    generate_tree(root_node)
    visualize(root_node)

    session.close()
