from ..todo import LogToDo
import elasticapm

def log(response, status_code, index: str, doc, args=None, params=None, headers=None):
    metadata = response.get('metadata')
    status = response.get('status')
    elasticapm.set_context(
        response
    )
    elasticapm.label(
        apm_transaction_id=elasticapm.get_transaction_id(),
        index=index,
        status=response.get('status')
    )
    todo = LogToDo(response, status_code, index, doc, args, headers, params)
    results = todo.process()
    transaction = {
        'status': status,
        'index': index,
        'apm_transaction_id': elasticapm.get_transaction_id(),
    }
    for result in results:
        transaction.update(result)

    metadata.update({
        'transaction': transaction
    })
    return response, status_code
