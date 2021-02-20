from typing import Any, Dict

import pyjq


def jq_filter_data(jq_vars: Dict[str, str], jq_var_join: str, data: Any) -> Dict[str, str]:
    results: Dict[str, str] = {}
    for var, jq_query in jq_vars.items():
        jq_results = pyjq.all(jq_query, data)
        joined_result = jq_var_join.join(map(str, jq_results))
        value = str(joined_result)
        results[var] = value
    return results
