from uuid import getnode        
def get_current_mac():
    mac = getnode()
    macString = ':'.join(("%012X" % mac) [i:i+2] for i in range(0,12,2))
    return f'{macString.lower()}'
