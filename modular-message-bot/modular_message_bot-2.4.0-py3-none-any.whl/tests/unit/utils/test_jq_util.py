from modular_message_bot.utils.jq_util import jq_filter_data


def test_jq_filter_data():
    # Given
    jq_vars = {"names": ".[] | select(.age > 12)  | .name", "ages": ".[] | .age"}
    jq_var_join = ","
    data = [
        {"name": "Alex", "country": "NZ", "age": 10},
        {"name": "Bob", "country": "NZ", "age": 12},
        {"name": "Clarke", "country": "Aus", "age": 13},
        {"name": "Codie", "country": "Aus", "age": 15},
        {"name": "Duane", "country": "UK", "age": 20},
    ]

    # When
    results = jq_filter_data(jq_vars, jq_var_join, data)

    # Then
    assert results == {"ages": "10,12,13,15,20", "names": "Clarke,Codie,Duane"}
