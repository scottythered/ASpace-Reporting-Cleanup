from asnake.client import ASnakeClient
import pandas as pd
from tqdm import tqdm
import datetime

client = ASnakeClient(baseurl='xxx',
                      username='xxx',
                      password='xxx')
client.authorize()


def extract_finding_aid_notes():
    """Extract finding aid notes from each ASpace collection."""
    print('Extracting finding aid notes...')
    fin_aid_note_column = []
    collection_num_column = []
    title_column = []
    resource_recs = client.get('repositories/2/resources', params={'all_ids': True}).json()
    for record in tqdm(resource_recs):
        rec_uri = client.get('repositories/2/resources/' + str(record)).json()
        try:
            fin_note = rec_uri['finding_aid_note']
            if fin_note:
                coll_num = rec_uri['id_0']
                title = rec_uri['title']
                collection_num_column.append(coll_num)
                fin_aid_note_column.append(fin_note)
                title_column.append(title)
        except KeyError:
            coll_num = rec_uri['id_0']
            title = rec_uri['title']
            except_note = 'No note'
            collection_num_column.append(coll_num)
            title_column.append(title)
            fin_aid_note_column.append(except_note)
    df = pd.DataFrame()
    df['Collection_Number'] = collection_num_column
    df['Collection_Title'] = title_column
    df['Finding_Aid_Note'] = fin_aid_note_column
    indexed_df = df.set_index(['Collection_Number'])
    print('Finding aid notes extracted.')
    return indexed_df


def extract_collection_notes():
    """Extract collection notes from each ASpace collection if they mention storage locations."""
    print('Extracting collection notes...')
    conditions_note_column = []
    collection_num_column = []
    resource_recs = client.get('repositories/2/resources', params={'all_ids': True}).json()
    for record in tqdm(resource_recs):
        rec_uri = client.get('repositories/2/resources/' + str(record)).json()
        try:
            notes = rec_uri['notes']
            for note in notes:
                type_field = note['type']
                if type_field == 'accessrestrict':
                    cond_note = note['subnotes'][0]['content'].strip().replace('\n', ' ')
                    if 'Stored ' in cond_note:
                        coll_num = rec_uri['id_0']
                        collection_num_column.append(coll_num)
                        conditions_note_column.append(cond_note)
                    elif 'stored ' in cond_note:
                        coll_num = rec_uri['id_0']
                        collection_num_column.append(coll_num)
                        conditions_note_column.append(cond_note)
                else:
                    pass
        except KeyError:
            coll_num = rec_uri['id_0']
            except_cond_note = 'No note'
            collection_num_column.append(coll_num)
            conditions_note_column.append(except_cond_note)
    df = pd.DataFrame()
    df['Collection_Number'] = collection_num_column
    df['Access_Notes_Regarding_Storage_Locations'] = conditions_note_column
    # deduped_df = df.drop_duplicates('Collection_Number')
    print('Collection notes extracted.')
    return df


def merge_dfs(x, y):
    """Merge the two dataframes and download a CSV."""
    df = pd.merge(x, y, on='Collection_Number', how='outer')
    indexed_df = df.set_index(['Collection_Number'])
    indexed_df['Access_Notes_Regarding_Storage_Locations'].fillna('No note', inplace=True)
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    output_file = 'storage_locations_' + str(today) + '.csv'
    indexed_df.to_csv(output_file)
    print('Location report exported as ' + output_file)
    return indexed_df


df1 = extract_finding_aid_notes()
df2 = extract_collection_notes()
df3 = merge_dfs(df1, df2)
