#!/usr/bin/env python

import argparse
import requests

parser = argparse.ArgumentParser(description='Convert elasticsearch mapping to JSON-Schema.')
parser.add_argument('source', metavar='N', type=str, help='elasticsearch URL + index or JSON schema file path.')
args = parser.parse_args()

argSource = args.source

es2schemaTypes = { 'keyword' : 'string', 'text' : 'string' }

def es2schema(mapping):
    ret = {}

    for field in mapping:
        value = mapping[field]

        if 'properties' in value:
            ret[field] = { 'type' : 'object', 'properties' : es2schema(value['properties']) }
        else:
            ret[field] = { 'type' : es2schemaTypes[value['type']] if value['type'] in es2schemaTypes else value['type'] }

    return ret

if argSource.startswith('http://') or argSource.startswith('https://'):
    buffer = requests.get(argSource + '/_mapping').json()

    mappings = buffer.itervalues().next()['mappings']
    mappingTitle = mappings.iterkeys().next()
    mapping = mappings[mappingTitle]['properties']

    schema = { "$schema": "http://json-schema.org/draft-06/schema#", "title" : mappingTitle, "type" : "object", "properties" : es2schema(mapping) }

    print schema
