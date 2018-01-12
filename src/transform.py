



#
#
#  DEPRECATED XML
#


import os, nltk
import lxml.etree as ET

TEXT_DIR = 'output/'
IN_PATH = "/Users/akimball/dev/content/hwxml/xml"
OUT_PATH = '/Users/akimball/dev/python/projects/first/simplified_content'

xslt= ET.parse('/home/akimball/dev/oxygen/nlp/xslt/strip-prebuilt.xsl')
transform = ET.XSLT(xslt)

def getXmlFiles(path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if os.path.splitext(f)[1] == '.xml']
    return result

def simplifyXml(file):
    print("looking at file "+file)
    filename = os.path.basename(file);
    name,ext = filename.split('.')
    new_name = name+'.txt'
    dom = ET.parse(file)
    newdom = transform(dom)
    transformed = ET.tostring(newdom, encoding="UTF8", method="text", pretty_print=True).decode('utf-8')
    transformed = ' '.join(transformed.split())
    with open(TEXT_DIR + new_name, "w") as text_file:
        text_file.write(transformed)


def buildCorpus():
    from nltk.corpus import PlaintextCorpusReader
    return PlaintextCorpusReader(TEXT_DIR, '.*')



# run
#all_files = getXmlFiles(IN_PATH)
#count = 0

#for file in all_files:
#    simplifyXml(file)

corpus = buildCorpus()

for fileid in corpus.fileids():
    num_chars = len(corpus.raw(fileid))
    num_words = len(corpus.words(fileid))
    num_sents = len(corpus.sents(fileid))
    num_vocab = len(set([w.lower() for w in corpus.words(fileid)]))
    #print int(num_chars/num_words), int(num_words/num_sents), int(num_words/num_vocab), fileid
    print(str(round(num_chars/num_words))+", "+str(round(num_words/num_sents))+", "+str(round(num_words/num_vocab))+" : "+fileid)
    #print int(num_chars/num_words), int(num_words/num_sents), int(num_words/num_vocab), fileid







print('done')