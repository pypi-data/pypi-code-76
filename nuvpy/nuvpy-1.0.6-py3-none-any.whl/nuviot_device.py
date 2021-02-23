import json
import nuvpy.nuviot_srvc as nuviot_srvc
import nuvpy.nuviot_util as nuviot_util

def get_device_types(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/api/devicetypes')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def get_device_configs(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/api/deviceconfigs')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def print_device_types(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/api/devicetypes')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("Device Types", nuviot_util.to_item_array(rj))

def print_device_configs(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/api/deviceconfigs')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("Device Configs", nuviot_util.to_item_array(rj))

def get_device_groups(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/repo/groups')        
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj) 

def get_device_repos(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/repo/groups')
    if responseJSON == None:
        return
    
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def get_devices_by_group(ctx, group_id):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/repo/group/' + group_id + '/devices')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def get_devices(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/devices')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def print_device_groups(ctx, repoid = None):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/repo/groups')

    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("Device Groups",nuviot_util.to_item_array(rj))
    
def print_devices(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/devices')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("Devices by Repo", nuviot_util.to_item_array(rj, "deviceId"))
    
def print_devices_by_group(ctx, group_id):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/repo/group/' + group_id + '/devices')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("Devices by Group", nuviot_util.to_item_array(rj))
