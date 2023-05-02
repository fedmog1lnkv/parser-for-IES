def rename_bg_dataframe(dataframe):
    return dataframe.rename(columns={'Date Time': 'date_time', 'NE': 'in_out_cannels', 'Tx Optical Power(dBm)': 'tx_optical_power', 'Rx Optical Power(dBm)': 'rx_optical_power'})
