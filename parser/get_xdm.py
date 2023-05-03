import os

import pandas as pd

from parser import utils


def v(string, start, n_bytes=2):
    # Value from byte string
    return int.from_bytes(string[start:start + n_bytes], byteorder='little')


def opt(file):
    result = [['time', 'ne', 'object', 'param', 'last', 'min', 'max']]
    with open(file, 'rb') as f:
        s = f.read()
    n = s.find(b'\x0a')
    while n < len(s):
        if v(s, n + 1) != 2:
            n += 46
            continue  # Skip data with "Disconnected NE 0x0A...00000000"
        time = v(s, n + 23, 4)
        ne = v(s, n + 5)
        objectId = v(s, n + 9)
        count = v(s, n + 27)
        for i in range(int(count / 3)):
            paramId = v(s, n + 29 + i * 26)
            r = [time, ne, objectId, paramId]
            for j in range(3):
                absValue = v(s, n + 31 + i * 26 + j * 8)
                negative = v(s, n + 33 + i * 26 + j * 8)
                _ = v(s, n + 35 + i * 26 + j * 8)  # I don't know, 6 or 7
                degree = v(s, n + 37 + i * 26 + j * 8)
                value = absValue / degree
                if negative == 1:
                    value *= -1
                r.append(value)
            result.append(r)
        n = n + 14 * 2 + int(count / 3) * 13 * 2
    return result


def filter_UES_TEC_10(data):
    data_Tx_UES = data[(data['ne'] == 5) & (data['object'] == 293) & (data['param'] == 271)]
    data_Rx_UES = data[(data['ne'] == 5) & (data['object'] == 165) & (data['param'] == 280)]

    data_Tx_TEC_10 = data[(data['ne'] == 8) & (data['object'] == 293) & (data['param'] == 271)]
    data_Rx_TEC_10 = data[(data['ne'] == 8) & (data['object'] == 165) & (data['param'] == 280)]

    # переименовываем столбцы для дальнейшей конкатенации
    data_Tx_UES = data_Tx_UES.rename(columns={'last': 'Tx Optical Power(dBm)'})
    data_Rx_UES = data_Rx_UES.rename(columns={'last': 'Rx Optical Power(dBm)'})

    data_Tx_TEC_10 = data_Tx_TEC_10.rename(columns={'last': 'Tx Optical Power(dBm)'})
    data_Rx_TEC_10 = data_Rx_TEC_10.rename(columns={'last': 'Rx Optical Power(dBm)'})

    UES_to_TEC_10 = pd.merge(data_Tx_UES[['time', 'Tx Optical Power(dBm)']],
                             data_Rx_TEC_10[['time', 'Rx Optical Power(dBm)']], on=["time"])
    UES_to_TEC_10.insert(1, 'ne', 'UES - TEC-10')

    TEC_10_to_UES = pd.merge(data_Tx_TEC_10[['time', 'Tx Optical Power(dBm)']],
                             data_Rx_UES[['time', 'Rx Optical Power(dBm)']], on=["time"])
    TEC_10_to_UES.insert(1, 'ne', 'TEC-10 - UES')

    return pd.concat([UES_to_TEC_10, TEC_10_to_UES])


def get_xdm_pandas(filename):
    """
    UES, M9 OM_OFA_B 2, Tx Power > TEC-10, M9 OM_OFA_P 1, Rx Power
    ne = 5, object = 293, param = 271 > ne = 8, object = 165, param = 280

    TEC-10, M9 OM_OFA_B 2, Tx Power > UES, M9 OM_OFA_P 1, Rx Power
    ne = 8, object = 293, param = 271 > ne = 5, object = 165, param = 280
    """
    data = pd.DataFrame(opt(filename))
    data.columns = data.iloc[0]
    data = data[1:]

    # время сбора данных на ne = 5 разнится с ne = 8 на одну секунду
    data.loc[data['ne'] == 8, 'time'] += 1

    UES_TEC_10 = filter_UES_TEC_10(data)

    UES_TEC_10['damping'] = UES_TEC_10['Tx Optical Power(dBm)'] - UES_TEC_10['Rx Optical Power(dBm)']

    UES_TEC_10['time'] = pd.to_datetime(UES_TEC_10['time'], unit='s')

    return utils.rename_xdm_dataframe(UES_TEC_10[
                                          [
                                              'time',
                                              'ne',
                                              'Tx Optical Power(dBm)',
                                              'Rx Optical Power(dBm)',
                                              'damping'
                                          ]
                                      ])


def get_xdm_all_files_pandas(folder_path):
    files = sorted(os.listdir(folder_path))
    data = get_xdm_pandas(folder_path + files[0])

    for filename in files[1:]:
        filename = folder_path + filename
        data = pd.concat([data, get_xdm_pandas(filename)])

    return data


if __name__ == '__main__':
    folder_path = "../data/XDM/"
    data = get_xdm_all_files_pandas(folder_path)
    print(data.to_string(index=False))
