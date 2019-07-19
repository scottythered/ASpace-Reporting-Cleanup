from asnake.client import ASnakeClient
from tqdm import tqdm
import datetime
import pandas as pd


client = ASnakeClient(baseurl='xxx',
                      username='xxx',
                      password='xxx')
client.authorize()


def main():
    data = []
    resource_recs = client.get('repositories/2/digital_objects',  params={'all_ids': True}).json()
    for record in tqdm(resource_recs):
        rec_uri = client.get('repositories/2/digital_objects/' + str(record)).json()
        try:
            do_id = rec_uri['digital_object_id']
        except:
            do_id = 'None'
        try:
            title = rec_uri['title']
        except:
            title = 'None'
        try:
            temp = []
            for version in rec_uri['file_versions']:
                temp.append('id {0} -- {1}'.format(version['identifier'],
                            version['file_uri']))
            versions = '||'.join(temp)
        except:
            versions = 'None'
        try:
            lang = rec_uri['language']
        except:
            lang = 'None'
        try:
            temp = []
            for link in rec_uri['linked_instances']:
                temp.append(link)
            links = '||'.join(temp)
        except:
            links = 'None'
        try:
            temp = []
            for extent in rec_uri['extents']:
                temp.append('{0} {1}'.format(extent['number'],
                            extent['extent_type']))
            extents = '||'.join(temp)
        except:
            extents = 'None'
        if rec_uri['dates']:
            if len(rec_uri['dates']) == 1:
                dates = 'Single date'
            elif len(rec_uri['dates']) > 1:
                dates = 'Multiple dates'
            else:
                dates = 'No dates'
        if rec_uri['notes']:
            temp = []
            for note in rec_uri['notes']:
                temp.append(note['type'])
            temp = list(dict.fromkeys(temp))
            notes = '||'.join(temp)
        else:
            notes = 'None'
        try:
            digital_object_type = rec_uri['digital_object_type']
        except:
            digital_object_type = 'None'
        data.append({'as_id': record, 'do_id': do_id, 'title': title,
                     'publish': rec_uri['publish'],
                     'do_type': digital_object_type,
                     'file_versions': versions, 'lang': lang,
                     'restrict': rec_uri['restrictions'], 'links': links,
                     'extents': extents, 'dates': dates,
                     'notes_present': notes})
    df = pd.DataFrame(data).set_index('do_id')
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    output_file = 'digital_objects_report_' + str(today) + '.csv'
    df.to_csv(output_file)


if __name__ == '__main__':
    main()
