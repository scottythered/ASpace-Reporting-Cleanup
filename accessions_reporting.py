#!/usr/bin/env python

from asnake.client import ASnakeClient
import pandas as pd
import datetime
from tqdm import tqdm

client = ASnakeClient(baseurl='XXX',
                      username='XXX',
                      password='XXX')
client.authorize()

accession_records = client.get('repositories/2/accessions', params={'all_ids': True}).json()

unit_column = []
extent_column = []
collection_no_column = []
created_column = []

start = datetime.datetime.strptime('2017-07-01', '%Y-%m-%d')
end = datetime.datetime.strptime('2018-07-31', '%Y-%m-%d')

for record in tqdm(accession_records):
    accession_uri = client.get('repositories/2/accessions/' + str(record)).json()
    create_date = accession_uri['create_time'][0:10]
    date_parsed = datetime.datetime.strptime(create_date, '%Y-%m-%d')
    if start <= date_parsed <= end:
        coll_num = accession_uri['id_0']
        extents = accession_uri['extents']
        for x in extents:
            units = x['extent_type']
            length = x['number']
            collection_no_column.append(coll_num)
            created_column.append(create_date)
            extent_column.append(length)
            unit_column.append(units)
    else:
        pass
print('Done')

df = pd.DataFrame()
df['Collection_Number'] = collection_no_column
df['Create_Date'] = created_column
df['Extent'] = extent_column
df['Extent_Units'] = unit_column
indexed_df = df.set_index(['Collection_Number'])

indexed_df.to_csv('2018_accession_report.csv')
print('Exported')
