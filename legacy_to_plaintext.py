
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup, SoupStrainer, Comment
import urllib.request


# In[19]:


url = "file:///Users/akimball/dev/content/mcs/11.5/xml/abq7/489/abq7489.xml"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page.read(), "lxml", from_encoding='utf-8')
for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
    comments.extract()


# In[20]:


data = str(soup.find_all('div', attrs={'id' : "results"}))
consumer_title = soup.find('meta-data.title', attrs={'audience' : "Consumer"}).text
clinical_title = soup.find('meta-data.title', attrs={'audience' : "Clinical"}).text


# In[21]:


gotowebs=  soup.find_all('div', attrs={'class': 'HwGoToWeb'})
for gotoweb in gotowebs:
    gotoweb.decompose()


# In[35]:


# HwNavigationSection

sections = soup.find_all("div", class_="HwNavigationSection")

for section in sections:

    st =section.find("h2", class_="HwSectionTitle")
    if (st is not None):
        stt =  " ".join(st.text.split())

        print(stt+"\n")
    for p in section.findAll(["p", "li"]):
        t =  " ".join(p.text.split())
        if (p.name == 'li'):
            print("* "+t)
        else:
            print(t+"\n")
        
    
    

