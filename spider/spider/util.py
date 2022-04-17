import re
import requests
from bs4 import BeautifulSoup


def get_words_from_html(html):
    ignore_tags = ['script', 'head', 'style']

    text = ''
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.select('p');
    for tag in tags:
        text += tag.get_text() + ' '


    # q = SimpleQueue()
    # q.put(soup)

    # while not q.empty():
    #     node = q.get()
    #     if node.name is None:
    #         text += node.string + ' '
    #     else:
    #         children = node.children
    #         for child in children:
    #             if child.name in ignore_tags:
    #                 continue

    #             q.put(child)


    patt = re.compile('\w+')
    return list(set(re.findall(patt, text)))


if __name__ == '__main__':
    url = 'https://stackoverflow.com/questions/71855183/how-to-read-a-json-file-and-put-it-into-multiple-array-without-knowing-the-key-i'
    resp = requests.get(url)
    text = resp.text
    print(get_words_from_html(text))
