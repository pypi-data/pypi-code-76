from kraken_html.html_field import Html_field

from dateutil.parser import parse

class Html_record:

    def __init__(self):

        a=1

    def record(self, keys, value):

        # Define link data. 
        record_type = value.get('@type', None)
        record_id = value.get('@id', None)



        content = ''

        content += '<div class="container-fluid">'

        content += '<dl class="row">'

        for i in keys:

            cell_value = value.get(i, None)

            # Convert value into datatype (url, etc)
            cell_value = value.get(i, None)

            

            content += self._record_line(record_type, record_id, i, cell_value)

        content += '</dl>'

        content += '</div>'

        return content

    def _record_line(self, record_type, record_id, key, values):

        if isinstance(values, str):
            values = [values]

        if not isinstance(values, list):
            values = [values]


        content = ''
        content +=  '<dt class="col-sm-3">'
        content +=  str(key) 
        content += ':</dt>'


        content += '<dd class="col-sm-9">'

        for value in values:

            html_field = Html_field()
            value = html_field.get(record_type, record_id, key, value)

            content += value + '<br>'

        content += '</dd>'

        return content


    def record_detail(self, keys, value):

        # Define link data. 
        record_type = value.get('@type', None)
        record_id = value.get('@id', None)



        content = ''

        content += '<div class="container-fluid">'

        content += '<dl class="row">'

        for i in keys:

            # COnvert value into datatype (url, etc)
            cell_dict = value.get(i, None)
            
            content += self._record_line_detail(record_type, record_id, i, cell_dict)

        content += '</dl>'

        content += '</div>'

        return content
    
    
    
    def _record_line_detail(self, record_type, record_id, key, values):

        # Shows full data info (credibility, etc)

        if not isinstance(values, list):
            values = [values]




        # Start generating html

        content = ''
        content +=  '<dt class="col-sm-3">'
        content +=  str(key) 
        content += ':</dt>'


        content += '<dd class="col-sm-9">'
        
        


        for value in values:

            # Format datatype
            if isinstance(value, dict):
                html_field = Html_field()
                value['value'] = html_field.get(record_type, record_id, key, value.get('value', None))



            content += '<dl class="row">'


            # Define list of keys, value first then alpha
            keys = ['value']
            all_keys = []
            if isinstance(value, dict):
                all_keys = sorted(value.keys())
            
            for i in all_keys:
                if i not in keys:
                    keys.append(i)


            # Generate subtable
            for i in keys:

                i_value = value
                if isinstance(value, dict):
                    i_value = value.get(i, value)

                content += '<dt class="col-sm-4">{i}</dt>'.format(i=i)
                content += '<dd class="col-sm-8">{i_value}</dd>'.format(i_value = i_value)
            
            
            content += '</dl>'
        
        
        
        #content += value 
        content += '</dd>'

        return content