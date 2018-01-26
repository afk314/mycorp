# Python
import os
import json
import argparse
import re
import time

# Local
import legacy_to_plaintext as l2p
import evn_api


def process_args():
    global args
    parser = argparse.ArgumentParser(description='Export HW XML to plain text')
    parser.add_argument('dest')
    parser.add_argument("--src", help="Directory with HW XML files", )
    parser.add_argument("--num", help="Number of XML files to process", type=int)
    args = parser.parse_args()
    if not args.src:
        args.src = SRC_DIR
    if not args.num:
        args.num = 99999999999


def delete_previous():
    '''Not totally sure why this exists'''
    global args
    for the_file in os.listdir(args.src):
        file_path = os.path.join(args.src, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def get_xml_files(path):
    '''Return a list of files from the src dir'''
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if
              os.path.splitext(f)[1] == '.xml']
    return result


def simplify_xml(file):
    output = l2p.to_plaintext(file)
    filename = os.path.basename(file)
    name, ext = filename.split('.')
    new_name = name + '.txt'
    with open(args.src + new_name, "w") as text_file:
        text_file.write(output)


def file_as_dict(file):
    line = {}
    line["text"] = l2p.to_plaintext(file)
    return line

def asset_id_from_filename(file):
    head, tail = os.path.split(file)
    name, ext = tail.split('.')
    return name

def load_entity_map():
    map = {}
    with open('/Users/akimball/Desktop/labels.txt') as f:
        lines = f.read().splitlines()
    for line in lines:
        hwcv_id, phrase = line.split("\t")
        # Build the regexp
        r_e = re.compile(r'\b{0}\b'.format(phrase))
        inner = {
            'id': hwcv_id,
            're': r_e,
            'phrase' : phrase
        }
        map[phrase] = inner

    return map

def normalize(entity_map,asset):
    for replace_obj in entity_map.values():
        if len(replace_obj['phrase']) < 5:
            continue
        asset['text'], count = re.subn(replace_obj['re'], ' '+replace_obj['id']+' ', asset['text'])
    return asset

def merge_asset_metadata(asset, metadata):
    try:
        if metadata['concepts']:
            inline_concepts = ''
            for concept in metadata['concepts']:
                inline_concepts = 'hwcv_'+str(concept)+' hwcv_'+str(concept)+' '+inline_concepts
            asset['text'] = inline_concepts+' '+asset['text']
    except KeyError:
        pass
    return {**asset, **metadata}

def files_to_jsonl(src, dest, num):
    entity_map = load_entity_map()

    with open(dest, 'w') as outfile:
        overall_time = 0.0
        start_time = time.time()
        for i, file in enumerate(get_xml_files(src)):
            asset_plaintext = file_as_dict(file)
            asset = normalize(entity_map, asset_plaintext)
            metadata = evn_api.get_metadata(asset_id_from_filename(file))

            asset_composite = merge_asset_metadata(asset, metadata)
            asset_composite['id'] = asset_id_from_filename(file)

            outfile.write(json.dumps(asset_composite) + '\n')

            if num & (i+1) == num:
                print('*', end='', flush=True)
                return
            elif (i+1) % 20 == 0:
                now = time.time()
                elapsed = now-start_time
                print(str(elapsed/i+1) +" per doc")


if __name__ == "__main__":
    process_args()
    print("Source dir is: " + args.src)
    print("Dest file is: " + args.dest)
    if args.num:
        print("Files to process: "+str(args.num))
    #delete_previous()
    files_to_jsonl(args.src, args.dest, args.num)
