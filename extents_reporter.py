from asnake.client import ASnakeClient
import pandas as pd
from tqdm import tqdm
import json
import datetime


def main():
    client = ASnakeClient(baseurl='XXXX',
                          username='XXXX',
                          password='XXXX')
    client.authorize()

    catalog = {'linear': ['linear_feet', 'Linear Feet', 'linear ft.', 'Linear Foot'],
               'cubic': ['cubic_feet', 'Cubic Feet'], 'gb': ['gigabytes', 'Gigabytes']}

    res_records = (client.get('repositories/2/resources', params={'all_ids': True})).json()

    data_list = []

    print('Compiling resource records from API...')

    for record in tqdm(res_records):
        res_record = client.get('repositories/2/resources/{0}'.format(record)).json()
        try:
            extents = res_record['extents']
            for x in extents:
                if x['extent_type'] == 'megabytes':
                    data_list.append({'id': res_record['id_0'], 'amount': str(float(x['number']) / 1000), 'units': 'gigabytes'})
                else:
                    data_list.append({'id': res_record['id_0'], 'amount': x['number'], 'units': x['extent_type']})
        except:
            pass

    linear_ms = 0
    linear_ua = 0
    gb_ms = 0
    gb_ua = 0
    cubic_ms = 0
    cubic_ua = 0

    print('Analyzing extents in resource data...')

    for entry in data_list:
        try:
            if entry['id'].startswith('MS') and entry['units'] in catalog['linear']:
                linear_ms += float(entry['amount'])
            elif entry['id'].startswith('UA') and entry['units'] in catalog['linear']:
                linear_ua += float(entry['amount'])
            elif entry['id'].startswith('MS') and entry['units'] in catalog['gb']:
                gb_ms += float(entry['amount'])
            elif entry['id'].startswith('UA') and entry['units'] in catalog['gb']:
                gb_ua += float(entry['amount'])
            elif entry['id'].startswith('MS') and entry['units'] in catalog['cubic']:
                cubic_ms += float(entry['amount'])
            elif entry['id'].startswith('UA') and entry['units'] in catalog['cubic']:
                cubic_ua += float(entry['amount'])
            else:
                pass
        except:
            exception = input('Uh oh, looks like the analysis ran into a snag; most likely, '
                              'a unit of extent for {0} ({1}) is not a pure number. Enter '
                              '\'stop\' to kill the process so you can fix the record. Alternatively, '
                              'you can enter \'continue\' to skip this entry and keep the analysis '
                              'going.'.format(entry['id'], entry['amount']))
            if (exception.lower()).strip() == 'continue':
                pass
            elif (exception.lower()).strip() == 'stop':
                quit()

    report = {
        'MS Linear feet': round(linear_ms, 2),
        'UA Linear feet': round(linear_ua, 2),
        'Total linear feet': round((linear_ua + linear_ms), 2),
        'MS GB': round(gb_ms, 2),
        'UA GB': round(gb_ua, 2),
        'Total GB': round((gb_ms + gb_ua), 2),
        'MS Cubic feet': round(cubic_ms, 2),
        'UA Cubic feet': round(cubic_ua, 2),
        'Total Cubic feet': round((cubic_ua + cubic_ms), 2)
    }

    print('Generating report as JSON...')

    with open(('extent_calculator_' + (datetime.datetime.today().strftime('%Y-%m-%d')) + '.json'), 'w') as f:
        json.dump(report, f)


if __name__ == "__main__":
    main()
