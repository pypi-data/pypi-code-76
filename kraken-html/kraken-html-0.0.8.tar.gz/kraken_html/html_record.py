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
            html_field = Html_field()
            i_value = html_field.get(record_type, record_id, i, cell_value)
            

            content += self._record_line(i, i_value)

        content += '</dl>'

        content += '</div>'

        return content

    def _record_line(self, key, value):

        content = ''
        content +=  '<dt class="col-sm-3">'
        content +=  str(key) 
        content += ':</dt>'
        content += '<dd class="col-sm-9">'
        content += value 
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

            cell_value = value.get(i, None)

            # If not dict, then single line
            if not isinstance(cell_value, dict):
                # Convert value into datatype (url, etc)
                cell_value = value.get(i, None)
                html_field = Html_field()
                i_value = html_field.get(record_type, record_id, i, cell_value)
                
                content += self._record_line(i, i_value)

            else:

                # COnvert value into datatype (url, etc)
                cell_dict = value.get(i, None)
                cell_value = cell_dict.get('value', '')
                
                html_field = Html_field()

                cell_dict['value'] = html_field.get(record_type, record_id, i, cell_value)
                
                content += self._record_line_detail(i, cell_dict)

        content += '</dl>'

        content += '</div>'

        return content
    
    
    
    def _record_line_detail(self, key, value):

        # Shows full data info (credibility, etc)




        # Define list of keys, value first then alpha
        keys = ['value']
        all_keys = sorted(value.keys())
        for i in all_keys:
            if i not in keys:
                keys.append(i)


        # Start generating html

        content = ''
        content +=  '<dt class="col-sm-3">'
        content +=  str(key) 
        content += ':</dt>'


        content += '<dd class="col-sm-9">'
        
        
        content += '<dl class="row">'


        # Define list of keys, value first then alpha
        keys = ['value']
        all_keys = sorted(value.keys())
        for i in all_keys:
            if i not in keys:
                keys.append(i)

        # Generate subtable
        for i in keys:
            i_value = value.get(i, '')
            content += '<dt class="col-sm-4">{i}</dt>'.format(i=i)
            content += '<dd class="col-sm-8">{i_value}</dd>'.format(i_value = i_value)
        
        
        content += '</dl>'
        
        
        
        #content += value 
        content += '</dd>'

        return content