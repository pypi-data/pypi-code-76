


class Html_record:

    def __init__(self):

        a=1

    def record(self, keys, value):

        content = ''

        content += '<div class="container-fluid">'

        content += '<dl class="row">'

        for i in keys:
            content += self._record_line(i, value.get(i, None))

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