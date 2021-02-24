from dateutil.parser import parse



class Html_field:

    def __init__(self):

        a = 1


    def get(self, record_type, record_id, key, value):

        content = ''
        path = None

        # Assign path for record if both exist
        if record_type and record_id:
            path = '/' + record_type + '/' + record_id



        # Check if object, if so puts a link to it

        if isinstance(value, dict):
            sub_type = value.get('@type', '')
            sub_id = value.get('@id', '')
            sub_path = '/' + sub_type + '/' + sub_id

            content = self.format_link(sub_id, sub_path)


        # Check if date, if so format it. 
        elif 'date' in key.lower():
            content = self.format_date(value)

        # Check if id or name of record 
        elif path and key in ['@id', 'schema:name']:

            content = self.format_link(value, path)

        # Check if url
        elif path and key in ['schema:url', 'schema:contenturl']:

            content = self.format_link(value, value)
        
        # Check if phone
        elif path and key in ['schema:phone', 'schema:telephone', 'schema:fax']:

            content = self.format_phone(value, value)

        # Check if email
        elif path and key in ['schema:email']:

            content = self.format_email(value, value)
        
        # Check if sms
        elif path and key in ['schema:sms']:

            content = self.format_sms(value, value)

        # Check if number
        elif self.format_number(value):
            content = self.format_number(value)



        else:
            content = value

        return content






    def format_number(self, value):
        # Convert value to right aligned 

        content = None
        i_value = None

        try:
            i_value = int(value)

        except:
            try: 
                i_value = float(value)
            except:
                a = 1

        if i_value:
            content = '<p style="text-align:right;">{value}</p>'.format(value=str(i_value))

        return content


    def format_sms(self, value, link):
        # Convert value to html link

        content = '<a href="sms:{link}">{value}</a>'.format(value=str(value), link=str(link))

        return content


    def format_email(self, value, link):
        # Convert value to html link

        content = '<a href="mailto:{link}">{value}</a>'.format(value=str(value), link=str(link))

        return content



    def format_phone(self, value, link):
        # Convert value to html link

        content = '<a href="tel:{link}">{value}</a>'.format(value=str(value), link=str(link))

        return content



    def format_link(self, value, link):
        # Convert value to html link

        content = '<a href="{link}">{value}</a>'.format(value=str(value), link=str(link))

        return content


    def format_date(self, value):
        # Check if value if of type date and formats it if so.

        try:
            a = parse(str(value))
            value = a.strftime("%Y-%m-%d, %H:%M")

        except:
            a = 1

        return value