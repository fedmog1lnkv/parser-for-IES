import json
import datetime

from influxdb import InfluxDBClient

import parser.get_bg as bg
import parser.get_xdm as xdm
import parser.get_pusk as pusk


def json_for_idb(data, table_name):
    json_body = json.loads(data.to_json(orient='records'))
    data_json = []

    for i in range(len(json_body)):
        if json_body[i]['date_time'] == None:
            continue
        else:
            data_json.append({
                'measurement': table_name,
                'tags': {
                   'in_out_channels': json_body[i]['in_out_channels']
                },
                'time': datetime.datetime.fromtimestamp((json_body[i]['date_time'])/1000-28800).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'fields': {
                    'tx_optical_power': json_body[i]['tx_optical_power'],
                    'rx_optical_power': json_body[i]['rx_optical_power'],
                    'damping': json_body[i]['damping']
                }
            })

    return data_json


def data_to_db(db_name, data, hostname='localhost'):
    my_Client = InfluxDBClient(host=hostname, port=8086)
    db_list = my_Client.get_list_database()
    check = False
    for db in db_list:
        if (db['name'] == 'ies_data'):
            check = True
    if check == False:
        my_Client.create_database('ies_data')
    my_Client.switch_database(db_name)
    my_Client.write_points(json_for_idb(data, 'channels_data'))


if __name__ == '__main__':
    bg_folder_path = "data/BG/"
    bg_data = bg.get_bg_all_files_pandas(bg_folder_path)
    xdm_folder_path = "data/XDM/"
    xdm_data = xdm.get_xdm_all_files_pandas(xdm_folder_path)
    pusk_folder_path = "data/PUSK/"
    pusk_data = pusk.get_pusk_all_files_pandas(pusk_folder_path)
    data_to_db('ies_data', bg_data)
    data_to_db('ies_data', xdm_data)
    data_to_db('ies_data', pusk_data)
    print('ok')

