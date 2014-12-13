#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from __future__ import print_function

import os
import sys

from coredata import CoredataClient, Entity


def get_padding(key, results):
    """ Gets the length of the longest property in results """
    return len(sorted([x[key] for x in results], key=len, reverse=True)[0])

try:
    username = os.environ['COREDATA_USERNAME']
    password = os.environ['COREDATA_PASSWORD']
except KeyError:
    print ('You need to set your Coredata username and passwords as the '
           'environ variables: COREDATA_USERNAME and COREDATA_PASSWORD '
           'respectivly.')
    sys.exit(1)

client = CoredataClient(
    host='https://azazo.coredata.is', auth=(username, password))

search_terms = {'title': sys.argv[1]} if len(sys.argv) > 1 else None
contacts = client.get(Entity.Contacts, search_terms=search_terms)

results = [{'name': contact['title'],
            'phones': ', '.join([x['number'] for x in contact['phones']]),
            'emails': ', '.join([x['email'] for x in contact['emails']])}
           for contact in contacts]

title_padding = get_padding('name', results)
phone_padding = get_padding('phones', results)
email_padding = get_padding('emails', results)

for contact in results:
    print(u'{name} | {phones} | {emails}'.format(
        name=contact['name'].ljust(title_padding),
        phones=contact['phones'].ljust(phone_padding),
        emails=contact['emails'].ljust(email_padding)))
