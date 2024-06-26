from collections import defaultdict
from dotenv import load_dotenv
import json
import boto3
import os

load_dotenv()

def get_kv_map(file_name):
    with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    textract = session.client('textract')
    response = textract.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS'])

    blocks = response['Blocks']
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    return key_map, value_map, block_map


def get_kv_relationship(key_map, value_map, block_map):
    kvs = defaultdict(list)
    for block_id, key_block in key_map.items():
        value_block = find_value_block(key_block, value_map)
        key = get_text(key_block, block_map)
        val = get_text(value_block, block_map)
        kvs[key].append(val)
    return kvs


def find_value_block(key_block, value_map):
    for relationship in key_block['Relationships']:
        if relationship['Type'] == 'VALUE':
            for value_id in relationship['Ids']:
                value_block = value_map[value_id]
    return value_block


def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = blocks_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
                    if word['BlockType'] == 'SELECTION_ELEMENT':
                        if word['SelectionStatus'] == 'SELECTED':
                            text += 'X '

    return text


def print_kvs(kvs):
    for key, value in kvs.items():
        print(key, ":", value)

def get_document_type(blocks):
    for block in blocks:
        if block['BlockType'] == 'WORD' and block['Text'].upper() in ['DOWOD', 'OSOBISTY', 'PASZPORT']:
            return block['Text']
    return None

def extract_form_values(image_path):
    key_map, value_map, block_map = get_kv_map(image_path)
    kvs = get_kv_relationship(key_map, value_map, block_map)
    
    trimmed_kvs = {"TYP": get_document_type(block_map.values()).upper()}
    for key, value in kvs.items():
        trimmed_kvs[key.strip()] = [v.strip() for v in value] if isinstance(value, list) else value.strip()
        
    return trimmed_kvs