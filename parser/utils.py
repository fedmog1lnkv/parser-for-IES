def rename_bg_dataframe(dataframe):
    return dataframe.rename(
        columns={'Date Time': 'date_time', 'NE': 'in_out_cannels', 'Tx Optical Power(dBm)': 'tx_optical_power',
                 'Rx Optical Power(dBm)': 'rx_optical_power'})


def rename_xdm_dataframe(dataframe):
    return dataframe.rename(
        columns={'time': 'date_time', 'ne': 'in_out_cannels', 'Tx Optical Power(dBm)': 'tx_optical_power',
                 'Rx Optical Power(dBm)': 'rx_optical_power'})

def rename_172_30_26_81(dataframe):
    return dataframe.rename(
        columns={'date_time_81': 'date_time', 'ne_81': 'in_out_cannels', 'PoutAmp_81': 'tx_optical_power',
                 'PinLn': 'rx_optical_power'})

def rename_172_30_26_106(dataframe):
    return dataframe.rename(
        columns={'date_time_106': 'date_time', 'ne_106': 'in_out_cannels', 'PoutAmp_106': 'tx_optical_power',
                 'PinRX': 'rx_optical_power'})