from bs4 import BeautifulSoup, Comment
import urllib.request


def medline_to_plaintext(filename):
    count = 0
    url = "file://"+filename
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml", from_encoding='utf-8')

    topics = soup.find_all("health-topic")
    for topic in topics:
        render_topic(topic)
        count = count + 1
        if count > 5:
            exit()



def render_topic(topic):
    title = topic['title']
    description = topic['meta-desc']
    url = topic['url']
    language = topic['language']
    also_called = get_also_called(topic)
    full_summary = topic.find('full-summary')
    output = ""
    for p in full_summary.findAll(["p", "li"]):
        t = " ".join(p.text.split())

        if (p.name == 'li'):
            output += "* " + t + "\n"
        else:
            output += "\n" + t + "\n"
    print(output)


def get_also_called(topic):
    l = []
    alsos = topic.find_all('also-called')
    for also in alsos:
        l.append(also.text)
    return l


def get_description(topic):
    return topic['meta-desc']

def get_title(topic):
    return topic['title']


def remove_rubbish(node):
    remove_comments(node)
    remove_divs(node)

def remove_comments(node):
    for comments in node.findAll(text=lambda text:isinstance(text, Comment)):
        comments.extract()

def remove_divs(node):
    gotowebs=  node.find_all('div', attrs={'class': 'HwGoToWeb'})
    for gotoweb in gotowebs:
        gotoweb.decompose()
    references = node.find_all('div', attrs={'class': 'HwSectionReferences'})
    for reference in references:
        reference.decompose()
    contentInfos = node.find_all('div', attrs={'class': 'HwContentInformation'})
    for contentInfo in contentInfos:
        contentInfo.decompose()
    credits = node.find_all('div', attrs={'class': 'HwCreditsSection'})
    for credit in credits:
        credit.decompose()



def do_it():
    print("Starting...")
    file = "/home/akimball/Downloads/mplus_topics_2017-12-02.xml"
    medline_to_plaintext(file)


do_it()