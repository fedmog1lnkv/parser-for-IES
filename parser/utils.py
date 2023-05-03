def rename_bg_dataframe(dataframe):
    return dataframe.rename(
        columns={'Date Time': 'date_time', 'NE': 'in_out_cannels', 'Tx Optical Power(dBm)': 'tx_optical_power',
                 'Rx Optical Power(dBm)': 'rx_optical_power'})


def rename_xdm_dataframe(dataframe):
    return dataframe.rename(
        columns={'time': 'date_time', 'ne': 'in_out_cannels', 'Tx Optical Power(dBm)': 'tx_optical_power',
                 'Rx Optical Power(dBm)': 'rx_optical_power'})
