from tqdm import tqdm
import datetime
from copy import deepcopy
from asnake.client import ASnakeClient
import asnake.logging as logging
today_date = datetime.datetime.today().strftime('%Y-%m-%d')
logging.setup_logging(filename='extent_type_changer_' + str(today_date) + '.log')
logger = logging.get_logger('extent_type_changes_log')


def main():
    client = ASnakeClient(baseurl='XXXX',
                          username='XXXX',
                          password='XXXX')
    client.authorize()

    changes = {'linear_feet': ['Linear Feet', 'linear ft.', 'Linear Foot'],
               'cubic_feet': ['Cubic Feet'], 'gigabytes': ['Gigabytes']}

    res_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()
    found_records = set([])

    for record in tqdm(res_records):
        rec_uri = 'repositories/2/resources/{0}'.format(record)
        res_record = client.get(rec_uri).json()
        updated_record = deepcopy(res_record)
        try:
            extents = res_record['extents']
            for ext_index, extent in enumerate(extents):
                for key, value in changes.items():
                    if extent['extent_type'] in value:
                        updated_record['extents'][ext_index]['extent_type'] = key
                        break
                    else:
                        pass
            if res_record['extents'] != updated_record['extents']:
                response = client.post(rec_uri, json=updated_record)
                if response.status_code == 200:
                    logger.info('Extent change successfully pushed', rec=record, response=response)
                    found_records.add(record)
                else:
                    logger.info('Extent change failed', rec=record, response=response)
            else:
                pass
        except:
            pass

    print('{0} resource records checked; {1} records updated.'.format(len(res_records), len(found_records)))


if __name__ == "__main__":
    main()
