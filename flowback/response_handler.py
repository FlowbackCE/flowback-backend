
def success_response(data, message):
    result = {}
    result['status'] = "success"
    result['message'] = message
    if data is not None:
        result['data'] = data
    return result


def failed_response(data, message):
    result = {}
    result['status'] = "failed"
    result['message'] = message
    if data is not None:
        result['data'] = data
    return result
