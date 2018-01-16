import os
import json
import legacy_to_plaintext
import evn_api

SRC_DIR = str(os.environ["HW_XML_MCS"])
DEST_FILE = '/usr/local/tmp/out.jsonl'


# Delete previous run
for the_file in os.listdir(SRC_DIR):
    file_path = os.path.join(SRC_DIR, the_file)
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
    with open(SRC_DIR + new_name, "w") as text_file:
        text_file.write(output)

def asDict(file):
    line = {}
    stop_split = file.index('.xml')
    line["text"] = legacy_to_plaintext.to_plaintext(file)
    return line



def files_to_jsonl(IN_PATH):
    all_files = getXmlFiles(IN_PATH)
    count = 1
    stop_at = 10000
    #printProgressBar(0, 15000, prefix='Progress:', suffix='Complete', length=50)

    with open(DEST_FILE, 'w') as outfile:

        for i, file in enumerate(all_files):
            r = asDict(file)

            head, tail = os.path.split(file)
            asset_id, ext = tail.split('.')
            r['id'] = asset_id
            md = evn_api.get_metadata(asset_id)
            # if (not md):
            #     # Skip empties
            #     continue

            combined = {**r, **md}

            outfile.write(json.dumps(combined)+'\n')
            if (count == stop_at):
                exit()
            if count % 20 == 0:
                print('.', end='', flush=True)
                #printProgressBar(i + 1, 150000, prefix='Progress:', suffix='Complete', length=50)

            count += 1


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()



if __name__ == "__main__":
    print("Source dir is: " + SRC_DIR)
    print("Dest file is: "+DEST_FILE)
    files_to_jsonl(SRC_DIR)
