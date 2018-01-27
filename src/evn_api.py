"""
This module will fetch metadata for a given asset id.  If no metadata exists, an empty object will be returned
"""
import requests
import json
import random

evnapi_server = 'hw-en-pcrs-ap01'
evnapi_port = '8088'
evn_api_endpoint = '/v1/evn/assets/'

def get_metadata(asset_id):
    """Your one stop shop for metadata"""
    response = get_page(asset_id)
    if (not response == {}):
        return clean_metadata(response)
    else:
        return {}

def get_page(asset_id):
    """Call the EVN API and return the payload or {} if not found"""
    url = 'http://' + evnapi_server + ':' + evnapi_port + evn_api_endpoint + asset_id
    r = requests.get(url)
    if (not r.ok):
        return {}
    return json.loads(r.content)


def drop_unnecessary(metadata):
    """Remove some unnecessary metadata field, typically dependent properties or those not interesting right now"""
    remove = ['_id', 'content_asset_id', 'last_updated', 'codewords', 'asset_relations', 'facets',
              'behaviorChange', 'codes', 'keywords', 'emr_max_age', 'emr_min_age', 'specialties', 'cached', 'hash']
    for remove_me in remove:
        del metadata[remove_me]



def concepts_to_int(metadata):
    """De-dupe and return a list of HWCV ids without the HWCV_ prefix"""
    concept_ids = set()
    for concept in metadata['concepts']:
        int_id = int(concept['concept_id'][5:])
        concept_ids.add(int_id)
    if not concept_ids:
        return None
    l = list(concept_ids)
    return l
    #return list(concept_ids)


def categories_to_int(metadata):
    """De-dupe and return a list of category ids without the cat previf"""
    category_ids = set()
    for cat in metadata['categories']:
        c = int(cat['id'][3:])
        category_ids.add(c)
    #return list(category_ids)
    if not category_ids:
        return None
    consumer = []
    clinical = []
    for cat in category_ids:
        if cat < 1499:
            consumer.append(cat)
        else:
            clinical.append(cat)
    return (consumer,clinical)


def genders_to_int(metadata):
    """0 = female, 1 = male, 2 = both"""
    if not metadata['gender'] or len(metadata) == 0 or len(metadata['gender']) > 1:
        return 2
    elif metadata['gender'][0] == 'male':
        return 1
    else:
        return 0


def audience_to_int(metadata):
    """0 = none, 1 = Caregiver, 2 = Parent, 3 = Patient, 4 = many"""
    if len(metadata['audience']) == 0:
        return 0
    elif len(metadata['audience']) > 1:
        return 4
    elif metadata['audience'][0] == 'Caregiver':
        return 1
    elif metadata['audience'][0] == 'Parent':
        return 2
    else:
        return 3


def settings_to_int(metadata):
    """0 = none, inpatient = 1, outpatient = 2, many = 3"""
    if len(metadata['delivery_setting']) == 0:
        return 0
    elif len(metadata['delivery_setting']) > 1:
        return 3
    elif metadata['delivery_setting'][0] == 'Outpatient':
        return 2
    else:
        return 1


def clean_metadata(metadata):
    """Get a simplified metadata report for an asset"""
    drop_unnecessary(metadata)

    # Handle nested concepts
    concept_ids = concepts_to_int(metadata)
    metadata['concepts'] = concept_ids

    # Handle nested categories


    consumer, clinical = categories_to_int(metadata)
    metadata['consumer_cats'] = consumer
    metadata['clinical_cats'] = clinical
    del metadata['categories']

    # Handle Gender
    genders = genders_to_int(metadata)
    metadata['gender'] = genders

    # Handle Gender
    settings = settings_to_int(metadata)
    del metadata['delivery_setting']
    metadata['setting'] = settings

    # Handle Audience
    audience = audience_to_int(metadata)
    metadata['audience'] = audience

    return metadata


