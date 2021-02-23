import json
import nuvpy.nuviot_srvc as nuviot_srvc
import nuvpy.nuviot_util as nuviot_util
from nuvpy.nuviot_srvc import NuvIoTRequest
from nuvpy.nuviot_srvc import NuvIoTResponse

def get_streams(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/datastreams')
    if responseJSON == None:
        return

    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)   

def print_streams(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/datastreams')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.print_array("Data Stream", nuviot_util.to_item_array(rj))  

def get_stream(ctx, stream_id, device_id, page_size=1500):
    rqst = NuvIoTRequest('/clientapi/datastream/' + stream_id + '/data/' + device_id)
    rqst.pageSize = page_size
    responseJSON = nuviot_srvc.get_paged(ctx, rqst)
    if responseJSON == None:
        return
    
    rj = json.loads(responseJSON)
    response = NuvIoTResponse(rj)
    return response.rows