import os	
import requests
from requests_html import HTMLSession
session = HTMLSession()
import sys
lang = "en"
BASE_PATH = "https://{lang}.wikipedia.org/wiki/".format(lang=lang)

m_depth = 10
depth = 0


class Node:

	def __init__(self, link: str, parent=None):
		self.parent = parent
		self.link = link
		self.children = []

		self.crawl(self)

	@staticmethod
	def crawl(node) -> None:
		global depth

		r = session.get(node.link)

		if depth >= m_depth:
			return

		depth += 1

		links = [link for link in r.html.absolute_links if BASE_PATH in link and ":" not in link[len(BASE_PATH):] and link != node.link]

		for link in links[:10]:
			print(node.link, "making", len(links), "new children \n-- currently on", link + '\n')
			node.children.append(Node(link, parent=node))

	@staticmethod
	def visualize(node, indent=0) -> None:
		sys.stdout.write("[{0}] {1}: {2}\n".format(str(indent // 2), '-'*indent, node.link))
		indent += 2
		for child in node.children:
			node.visualize(child, indent=indent)




query = "physics"

url = os.path.join(BASE_PATH, query)
main_node = Node(link=url)
main_node.visualize(node=main_node)