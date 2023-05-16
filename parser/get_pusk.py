import os
from datetime import datetime

import chardet
import pandas as pd

from parser import utils


def get_encoding(filename):
    with open(filename, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    return encoding


def get_172_30_26_81_pandas(filename):
    data = []
    ne = 'dtrssampa4'

    with open(filename, 'r', encoding=get_encoding(filename)) as file:
        for line in file:
            if ne in line:
                parts = line.split('=>')
                date_time = parts[0][2:-1]
                date_time = datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S')

                parameters = parts[1][parts[1].find('->') + 2:].split(';')
                if 'LDCurrent' in parameters[0]:
                    PoutAmp = float(parameters[3].replace('PoutAmp=', ''))
                    PinRX = float(parameters[1].replace('PinRX=', ''))
                    data.append([date_time, ne, PoutAmp, PinRX])

    return pd.DataFrame(data, columns=['date_time', 'ne', 'PoutAmp', 'PinRX'])


def get_172_30_26_106_pandas(filename):
    data = []
    ne = 'dtrssampai6'
    with open(filename, 'r', encoding=get_encoding(filename)) as file:
        for line in file:
            if ne in line:
                parts = line.split('=>')
                date_time = parts[0][2:-1]
                date_time = datetime.strptime(date_time, '%d/%m/%Y %H:%M:%S')

                parameters = parts[1][parts[1].find('->') + 2:].split(';')
                if 'ILDHMax' not in parameters[0]:
                    PoutAmp = float(parameters[3].replace('PoutAmp=', ''))
                    PinLn = float(parameters[1].replace('PinLn=', ''))
                    data.append([date_time, ne, PoutAmp, PinLn])

    return pd.DataFrame(data, columns=['date_time', 'ne', 'PoutAmp', 'PinLn'])


def filter_BGES_NPS_4(data_172_30_26_81, data_172_30_26_106):
    merg = data_172_30_26_81.join(data_172_30_26_106, lsuffix='_81', rsuffix='_106')

    data_172_30_26_81 = merg.loc[:, ['date_time_81', 'ne_81', 'PoutAmp_81', 'PinLn']]
    data_172_30_26_106 = merg.loc[:, ['date_time_106', 'ne_106', 'PoutAmp_106', 'PinRX']]

    data_172_30_26_81 = utils.rename_172_30_26_81(data_172_30_26_81)
    data_172_30_26_106 = utils.rename_172_30_26_106(data_172_30_26_106)

    return pd.concat([data_172_30_26_81, data_172_30_26_106])


def get_pusk_pandas(filename):
    """
    172.30.26.106, dtrssampai6, PoutAmp >
    172.30.26.81, dtrssampa4, PinRX

    172.30.26.81, dtrssampa4, PoutAmp >
    172.30.26.106, dtrssampai6, PinLn
    """

    data_172_30_26_81 = get_172_30_26_81_pandas(filename.replace('-folder-', '172.30.26.81'))
    data_172_30_26_106 = get_172_30_26_106_pandas(filename.replace('-folder-', '172.30.26.106'))

    BGES_NPS_4 = filter_BGES_NPS_4(data_172_30_26_81, data_172_30_26_106)

    BGES_NPS_4['damping'] = BGES_NPS_4['tx_optical_power'] - BGES_NPS_4['rx_optical_power']

    BGES_NPS_4['in_out_channels'] = BGES_NPS_4['in_out_channels'].replace('dtrssampa4', 'NPS4 - BGES').replace(
        'dtrssampai6', 'BGES - NPS4')

    BGES_NPS_4 = BGES_NPS_4.sort_values('date_time')

    return BGES_NPS_4


def get_pusk_all_files_pandas(folder_path):
    files = sorted(os.listdir(folder_path + '172.30.26.81/'))
    data = get_pusk_pandas(folder_path + "-folder-/" + files[0])

    for filename in files[1:]:
        filename = folder_path + "-folder-/" + filename
        data = pd.concat([data, get_pusk_pandas(filename)])

    return data


if __name__ == '__main__':
    folder_path = "../data/PUSK/"
    file = '../data/PUSK/-folder-/20230101.jipg'
    data = get_pusk_all_files_pandas(folder_path)
    print(data.to_string(index=False))
