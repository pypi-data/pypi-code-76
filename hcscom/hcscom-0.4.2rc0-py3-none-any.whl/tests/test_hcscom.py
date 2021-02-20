from hcscom.hcscom import split_data_to_values

def test_split_bytes():
    assert split_data_to_values(data=b"112233", width=3, decimals=1) == (11.2, 23.3)
    assert split_data_to_values(data=b"22221111", width=4, decimals=2) == (22.22, 11.11)


