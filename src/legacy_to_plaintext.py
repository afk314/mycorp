from bs4 import BeautifulSoup, Comment
import urllib.request


def to_plaintext(filename):
    output = ""
    url = "file://"+filename
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml", from_encoding='utf-8')
    remove_rubbish(soup)
    sections = soup.find_all("div", class_="HwNavigationSection")

    output += get_title(soup, None)+"\n\n"
    #clinical = get_title(soup, "Clinical")
    #if (clinical is not None):
    #    output += clinical+"\n\n"


    for section in sections:
        st = section.find("h2", class_="HwSectionTitle")
        if (st is not None):
            stt = " ".join(st.text.split())
            output += "\n"+stt+"\n\n"
        for p in section.findAll(["p", "li"]):
            t = " ".join(p.text.split())

            if (p.name == 'li'):
                output += "* " + t+"\n"
            else:
                output += "\n"+t+"\n"
    output = output.replace("\n\n\n","\n\n")
    return output.lower()


def get_title(node, type):
    if (type is None):
        n = node.find('meta-data.title')
    else:
        n = node.find('meta-data.title', attrs={'audience': type})
    if (n is None):
        return None
    else:
        return n.text

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





def make_one():
    file = "/home/akimball/dev/content/mcs/11.5/xml/aa18/749/aa18749.xml"
    result = to_plaintext(file)
    print(result)

#make_one()