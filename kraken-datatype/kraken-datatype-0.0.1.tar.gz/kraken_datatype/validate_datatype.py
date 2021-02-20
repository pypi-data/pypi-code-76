
import validators


class Validate_datatype:
    '''
    determine datatype fo a value (url, email, phone, etc)
    '''
    
    def __init__(self):
        a=1
        
    
    
    def is_url(self, value):
        '''
        test if value is is_url
        returns true if so
        '''
        if not value:
            return False


        return validators.url(value)
    

    def is_domain(self, value):
        '''
        test if value is is domain
        returns true if so
        '''
        if not value:
            return False


        return validators.domain(value)

    
    def is_email(self, value):
        
        if not value:
            return False


        return validators.email(value)
            
    def is_uuid(self, value):
        
        if not value:
            return False


        return validators.uuid(value)


    def is_country(self, value):
        
        return
    
    
    def is_city(self, value):
    
    
        return
    
    
    def is_phone(self, value):
        
        return
    
    
    
    def is_address(self, value):
        
        return
    
    
    def is_color(self, value):
        
        return
    
    
    
    def is_gender(self, value):
        
        return
    
    