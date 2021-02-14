from django import template


register = template.Library()

@register.simple_tag
def full_url_without_tags(request, *args):
    """Removes all values of arg from the given string"""

    full_path = request.get_full_path()
    query_part = full_path.split('?')
    
    if len(query_part) == 1:
        return full_path
     
    tags = [ x.split('=') for x in query_part[1].split('&')]
    
    tags_final = []
    for item in tags:
        if item[0] not in args:
            tags_final.append('='.join(item))
    
    
    full_path = f'{query_part[0]}?{"&".join(tags_final)}'
    
    return full_path
