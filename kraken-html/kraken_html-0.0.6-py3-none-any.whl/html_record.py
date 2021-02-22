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