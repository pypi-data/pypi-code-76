
from dateutil.parser import parse

class Html_record:

    def __init__(self):

        a=1

    def record(self, keys, value):

        content = ''

        content += '<div class="container-fluid">'

        content += '<dl class="row">'

        for i in keys:

            i_value = value.get(i, None)

            # Convert to datetime and then to simple date format
            try:
                date_value = parse(i_value)
                i_value = date_value.strftime("%Y-%m-%d, %H:%M")
            except:
                a = 1

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