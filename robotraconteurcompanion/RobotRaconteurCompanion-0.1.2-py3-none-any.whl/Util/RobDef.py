import RobotRaconteur as RR
import importlib.resources

def register_service_type_from_resource(node, package, resource):
    robdef_text = get_service_type_from_resource(package,resource)
    node.RegisterServiceType(robdef_text)

def register_service_types_from_resources(node, package, resources):
    robdefs_text = get_service_types_from_resources(package,resources)
    node.RegisterServiceTypes(robdefs_text)

def get_service_type_from_resource(package, resource):
    ext = ""
    if importlib.resources.is_resource(package, resource + ".robdef"):
        ext = ".robdef"    
    robdef_text = importlib.resources.read_text(package,resource + ext)
    return robdef_text

def get_service_types_from_resources(package, resources):
    robdefs_text = []
    for resource in resources:
        ext = ""
        if importlib.resources.is_resource(package, resource + ".robdef"):
            ext = ".robdef"
        robdef_text = importlib.resources.read_text(package,resource + ext)
        robdefs_text.append(robdef_text)
    return robdefs_text