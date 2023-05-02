import datetime
import os

import pandas as pd

import parser.utils as utils


def open_file_in_pandas(filename):
    return pd.read_csv(filename)


def get_date_time(filename: str) -> datetime:
    # LaserPerformance20230331075358.csv
    date = filename[-18:-10]  # 20230103
    time = filename[-10:-4]  # 073311

    return datetime.datetime.strptime(date + time, "%Y%m%d%H%M%S")


def filter_UES_BG_Sputnik(data):
    USE_BG = data.loc[(data['NE'] == 'UES_BG') & (data['Card'] == 'XS A:SAM_16') & (data['Object'] == 'oPort 1-SFP')]
    Sputnik = data.loc[(data['NE'] == 'Sputnik') & (data['Card'] == 'XS B:SAM_16') & (data['Object'] == 'oPort 1-SFP')]
    return pd.concat([USE_BG, Sputnik])


def get_bg_pandas(filename):
    """
    UES_BG, XS A:SAM_16, oPort 1-SFP, Tx Optical Power(dBm) >
    Sputnik, XS B:SAM_16, oPort 1-SFP, Rx Optical Power(dBm)

    Sputnik, XS B:SAM_16, oPort 1-SFP, Tx Optical Power(dBm) >
    UES_BG, XS A:SAM_16, oPort 1-SFP, Rx Optical Power(dBm)

    """
    data = open_file_in_pandas(filename)
    UES_BG_Sputnik = filter_UES_BG_Sputnik(data)
    UES_BG_Sputnik.insert(0, 'Date Time', [get_date_time(filename)] * 2)

    UES_BG_Sputnik['NE'] = UES_BG_Sputnik['NE'].replace('UES_BG', 'UES_BG - Sputnik')
    UES_BG_Sputnik['NE'] = UES_BG_Sputnik['NE'].replace('Sputnik', 'Sputnik - UES_BG')

    UES_BG_Sputnik['damping'] = UES_BG_Sputnik['Tx Optical Power(dBm)'] - UES_BG_Sputnik['Rx Optical Power(dBm)']

    return utils.rename_bg_dataframe(UES_BG_Sputnik[
                                         [
                                             'Date Time',
                                             'NE',
                                             'Tx Optical Power(dBm)',
                                             'Rx Optical Power(dBm)',
                                             'damping'
                                         ]
                                     ])


def get_bg_all_files_pandas(folder_path):
    files = sorted(os.listdir(folder_path))
    data = get_bg_pandas(folder_path + files[0])

    for filename in files[1:]:
        filename = folder_path + filename
        data = pd.concat([data, get_bg_pandas(filename)])

    return data


if __name__ == "__main__":
    folder_path = "../data/BG/"
    data = get_bg_all_files_pandas(folder_path)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print(data.to_string(index=False))
