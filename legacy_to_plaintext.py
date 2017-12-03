from bs4 import BeautifulSoup, Comment
import urllib.request


def to_plaintext(filename):
    output = ""
    url = "file://"+filename
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml", from_encoding='utf-8')
    remove_rubbish(soup)
    sections = soup.find_all("div", class_="HwNavigationSection")

    output += get_title(soup, "Consumer")+"\n\n"
    clinical = get_title(soup, "Clinical")
    if (clinical is not None):
        output += clinical+"\n\n"


    for section in sections:
        st = section.find("h2", class_="HwSectionTitle")
        if (st is not None):
            stt = " ".join(st.text.split())
            output += stt+"\n"
            #print(stt + "\n")
        for p in section.findAll(["p", "li"]):
            t = " ".join(p.text.split())

            if (p.name == 'li'):
                output += "* " + t
                #print("* " + t)
            else:
                output += t+"\n"
                #print(t+"\n")
    return output


def get_title(node, type):
    n = node.find('meta-data.title', attrs={'audience': type})
    if (n is None):
        return ""
    else:
        return n.text

def remove_rubbish(node):
    remove_comments(node)
    remove_gotoweb(node)

def remove_comments(node):
    for comments in node.findAll(text=lambda text:isinstance(text, Comment)):
        comments.extract()

def remove_gotoweb(node):
    gotowebs=  node.find_all('div', attrs={'class': 'HwGoToWeb'})
    for gotoweb in gotowebs:
        gotoweb.decompose()




