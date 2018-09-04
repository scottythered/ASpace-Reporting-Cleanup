#!/usr/bin/env python

from asnake.client import ASnakeClient
from tqdm import tqdm
import pandas as pd
import datetime
import re

client = ASnakeClient(baseurl='XXX',
                      username='XXX',
                      password='XXX')
client.authorize()


def pattern_matcher(x):
    """Match a resource title that ends with a comma."""
    pattern_match = re.compile(r'^.*\>$|^\<.*$|^.*\<.*$|\>')
    result = pattern_match.match(x)
    return result


def data_framer(rec_ids, rec_index, rec_titles):
    """Create a DataFrame from generated lists."""
    rec_df = pd.DataFrame()
    rec_df['Resource_no'] = rec_index
    rec_df['Identifier'] = rec_ids
    rec_df['Collection_Title'] = rec_titles
    indexed_rec_df = rec_df.set_index(['Identifier'])
    return indexed_rec_df


def html_hunter_titles(y):
    """Look for ArchivesSpace resources that match pattern_matcher, then save them in a list and generate a CSV report."""
    if y == 'record titles':
        recs = client.get('repositories/2/resources', params={'all_ids': True}).json()
        base_uri = 'repositories/2/resources/'
        rec_type = 'record_titles'
        identifier = 'id_0'
    elif y == 'object titles':
        recs = client.get('repositories/2/archival_objects', params={'all_ids': True}).json()
        base_uri = 'repositories/2/archival_objects/'
        rec_type = 'object_titles'
        identifier = 'digital_object_id'
    rec_index = []
    rec_titles = []
    rec_ids = []
    print('Searching ' + y + ' for HTML...')
    for record in tqdm(recs):
        uri = base_uri + str(record)
        record_detail = client.get(uri).json()
        try:
            record_title = record_detail['title']
            if pattern_matcher(record_title):
                rec_id = record_detail[identifier]
                rec_index.append(record)
                rec_titles.append(record_title)
                rec_ids.append(rec_id)
        except (KeyError, IndexError):
            pass
    print('Found ' + str(len(rec_index)) + ' ' + y + ' containing suspected HTML.')
    indexed_rec_df = data_framer(rec_ids, rec_index, rec_titles)
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    file_name = 'legacy_html_' + rec_type + '_' + str(today_date) + '.csv'
    indexed_rec_df.to_csv(file_name)
    return indexed_rec_df


def html_hunter_notes():
    recs = client.get('repositories/2/resources', params={'all_ids': True}).json()
    rec_index = []
    rec_titles = []
    rec_ids = []
    print('Searching notes for HTML...')
    for record in tqdm(recs):
        record_detail = client.get('repositories/2/resources/' + str(record)).json()
        try:
            rec_uri_notes = record_detail['notes']
            for note in rec_uri_notes:
                subnotes = note['subnotes']
                if subnotes:
                    for subnote in subnotes:
                        if subnote['jsonmodel_type'] == 'note_text':
                            note_string = subnote['content']
                            if pattern_matcher(note_string):
                                perm_id = note['persistent_id']
                                rec_index.append(record)
                                rec_titles.append(note_string)
                                rec_ids.append(perm_id)
        except (KeyError, IndexError):
            pass
    print('Found ' + str(len(rec_index)) + ' notes containing suspected HTML.')
    data_framer(rec_ids, rec_index, rec_titles)
    indexed_rec_df = data_framer(rec_ids, rec_index, rec_titles)
    today_date = datetime.datetime.today().strftime('%Y-%m-%d')
    file_name = 'legacy_html_notes_' + str(today_date) + '.csv'
    indexed_rec_df.to_csv(file_name)
    return indexed_rec_df


html_hunter_titles('record titles')
html_hunter_titles('object titles')
html_hunter_notes()
