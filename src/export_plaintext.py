import os
from legacy_to_plaintext import to_plaintext

TEXT_DIR = '../output/'
IN_PATH = str(os.environ["HW_XML_MCS"])


# Delete previous run
for the_file in os.listdir(TEXT_DIR):
    file_path = os.path.join(TEXT_DIR, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)


def getXmlFiles(path):
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if os.path.splitext(f)[1] == '.xml']
    return result

def simplifyXml(file):
    output = to_plaintext(file)
    filename = os.path.basename(file)
    name,ext = filename.split('.')
    new_name = name+'.txt'
    with open(TEXT_DIR + new_name, "w") as text_file:
        text_file.write(output)


all_files = getXmlFiles(IN_PATH)
for file in all_files:
    simplifyXml(file)

