import os
import json
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

def asDict(file):
    line = {}
    stop_split = file.index('.xml')
    line["id"] = file[0:stop_split]
    line["text"] = to_plaintext(file)
    return line

# Return the asset metadata from evn-cache
def getMetadata(id):
    return None


def files_to_jsonl(IN_PATH):
    all_files = getXmlFiles(IN_PATH)
    all = []
    count = 0
    for file in all_files:
        # simplifyXml(file)
        r = asDict(file)
        all.append(r)
        # if (count > 1000):
        #     with open('/usr/local/tmp/out.jsonl', 'w') as outfile:
        #         for entry in all:
        #             json.dump(entry, outfile)
        #             outfile.write('\n')
        #     exit()
        # count += 1
    return all




