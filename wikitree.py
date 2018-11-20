from requests_html import HTMLSession
import sys
import os

session = HTMLSession()


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


def generate_tree(root: Node, max_depth: int=0) -> None:
    """ # Breadth First Search (generation)
    :param root: node of type Node
    :param max_depth: Optional, set a max article depth as an integer
    :return: Generates a tree structures with max_depth from root
    """

    nodes = []
    stack = [root]
    depth = 0

    links_per_article = 5

    max_depth = max_depth or links_per_article ** 3

    while stack and depth < max_depth:
        c_node = stack[0]
        stack = stack[1:]

        nodes.append(c_node)
        for link in get_sublinks(c_node.link)[:links_per_article]:
            n = Node(link=link, parent=c_node)
            stack.append(n)
            c_node.children.append(n)

        depth += 1


def visualize(node: Node, indent: int=0) -> None:
    """ # Recursive Depth First Search
    :param node: node of type Node
    :param indent: int(x) how many dashes should be added per depth level
    :return: Visualizes a tree structures to stdout using sys.stdout.write
    """
    sys.stdout.write("[{0}] {1}: {2}\n".format(str(indent // 2), '-'*indent, node.link))

    indent += 2
    for child in node.children:
        visualize(child, indent=indent)


if __name__ == "__main__":

    lang = "en"
    BASE_PATH = "https://{lang}.wikipedia.org/wiki/".format(lang=lang)

    query = input("""topic (e.g. "physics"): """) or "physics"
    query.replace(' ', '_')

    url = os.path.join(BASE_PATH, query)

    root = Node(link=url)
    generate_tree(root)

    visualize(root)
    sys.stdout.write("\n [n] symbolises article depth from [0] root")

    session.close()
