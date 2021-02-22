import datetime


class html_object:
    def  __init__(self):
        self.content = ''

    def table(self, record):
        return ''

    def editor(self):
        print('get html editor')
        self.content = get_html_text_editor()
        print(self.content)
        return self.content

class helper_html:
    def __init__(self):
        self.value = ''
    
    def get_card(self, record):
        self.value = get_html_card(record)
        return self.value

    def get_html_carddeck(self, records):
        self.value = get_html_carddeck(records)
        return self.value

    def get_html_table(self, records):
        self.value = get_html_table(records)
        return self.value

    def get_html_record(self, record):
        self.value = get_html_record(record)
        return self.value    

    def get_html_media(self, record):
        self.value = get_html_media(record)
        return self.value

    def get_html_link(self, url, text = None):
        self.value = get_html_link(url, text)
        return self.value

    def get_html_section(self, title, html_content = None):
        self.value = get_html_section(title, html_content)
        return self.value
    
    def get_html_records_sections(self, records, title = None):
        self.value = get_html_records_sections(records, title)
        return self.value

    def editor(self):
        self.value = get_html_text_editor()
        return self.value



def get_html_card(record):

    record_type = record.get('@type', None)
    record_id = record.get('@id', None)


    if not record:
        return ''

    card_title = record.get('schema:name', None)
    card_url = record.get('schema:contenturl', None)
    card_record_link = '/' + record_type + '/' + record_id + '?format=html'


    card = '''
        <a href="{card_record_link}">
        <div class="card">
            <img src="{card_url}" class="card-img-top" alt="{card_title}">
            <div class="card-body">
            
            </div></div>
            </a>
            '''
    d = { 'card_title': card_title, 'card_url': card_url, 'card_record_link': card_record_link }
    html_card = card.format(**d)

    return html_card


def get_html_carddeck(records):
        
    
    if not records:
        return ''

    card_deck = '<div class="row row-cols-1 row-cols-md-4">'
    for i in records:

        card_deck = card_deck + '<div class="col mb-4">'
        card_deck = card_deck + get_html_card(i)
        card_deck = card_deck + '</div>'
       
    card_deck = card_deck + '</div>'

    return card_deck


def get_html_table(records): 
    if not records:
        return ''

    if isinstance(records, str):
        return ''

    if isinstance(records, dict):
        records = [records]

    # Remove empty 
    new_records = []
    for i in records:
        if i:
            i_type =  i.get('@type', None)
            i_id = i.get('@id', None)
            if i_type and i_id:
                new_records.append(i)
    records = new_records

    # get keys:
    keys = set().union(*(d.keys() for d in records))
    sorted_keys = sorted(keys)


    p = []
    # Initialize table
    p.append('<table>')

    # Generate table header
    p.append('<thead><tr>')

    p.append('<th>@type</th>')

    p.append('<th>@id</th>')

    p.append('<th>Name</th>')


    p.append('<th>Status</th>')

    p.append('<th># values</th>')
    
    p.append('<th># extracted</th>')


    if len(records) > 1 and records[0].get('kraken:datapoint_id', None):
        p.append('<th>kraken:datapoint_id</th>')

    ''''
    for i in sorted_keys:
        p.append('<th>' + i + '</th>')
    p.append('</tr></thead>')
    '''

    # Generate table body
    def make_html_row(k, value):
        # Make html table row (<td>)
        if isinstance(value, dict):
            sub_value_type = value.get('@type', None)
            sub_value_id = value.get('@id', None)
            record_name = value.get('schema:name', None)
        
            if record_name:
                text = record_name
            else:
                text = sub_value_id
            
            if sub_value_type and sub_value_id:
                # Test if valid record
                if not isinstance(sub_value_type, str): 
                    return ''
                if not isinstance(sub_value_id, str): 
                    return ''

                url = '/' + sub_value_type + '/' + sub_value_id + '?format=html'
                value = get_html_link(url, text)

            else: 
                value = 'More'


        elif isinstance(value, list) and not isinstance(value, str):
            value = 'list: ' + str(len(value)) + ' items'
        elif isinstance(value, datetime.datetime):
            value = value.isoformat()
        else:
            # If id exist, generate link to record
            if k == '@id':
                sub_value_type = i.get('@type', '')
                sub_value_id = i.get('@id', '')
                datapoint_id = i.get('kraken:datapoint_id', '')

                sub_record_name = i.get('schema:name', None)
        
                if sub_record_name:
                    text = sub_record_name
                else:
                    text = sub_value_id
                
                url = '/' + sub_value_type + '/' + sub_value_id + '?format=html'
                value = get_html_link(url, text)
           
            elif k=='kraken:datapoint_id':
                sub_value_type = i.get('@type', '')
                sub_value_id = i.get('@id', '')
                datapoint_id = i.get('kraken:datapoint_id', '')

                sub_record_name = i.get('schema:name', None)
                    
                text = datapoint_id
                url = '/' + sub_value_type + '/' + sub_value_id + '/datapoint/' + datapoint_id + '?format=html'

                value = get_html_link(url, text)
            
            
            
            
            else: 
                if len(str(value)) > 50:
                    value = value[:30] + '...'
                else:
                    value = value
        
        new_value = '<td>'
        new_value = new_value + str(value)
        new_value = new_value + '</td>'

        
        return new_value



    # Initialize table body
    p.append('<tbody>')
    sorted_records = sorted(records, key = lambda i: (i['@type'], i['@id'])) 


    
    for i in sorted_records:
       

        # Start new row (<tr>)
        p.append('<tr>')
        p.append(make_html_row('@type', i.get('@type', None)))
        p.append(make_html_row('@id', i.get('@id', None)))
        p.append(make_html_row('Name', i.get('schema:name', None)))

        p.append(make_html_row('Status', i.get('schema:actionstatus', None)))

        p.append(make_html_row('# values', 'na'))
        extracted = i.get('kraken:extracted', None)
        if extracted: 
            len_extract = len(extracted)
        else: 
            len_extract = 0
        p.append(make_html_row('# extracted', str(len_extract)))
        
        if i.get('kraken:datapoint_id', None):
            p.append(make_html_row('kraken:datapoint_id', i.get('kraken:datapoint_id', None)))


        # Make columns (<td>)
        '''
        for k in sorted_keys:
            if k == '@id' or k == '@type' or k == 'kraken:datapoint_id':
                continue
            value = i.get(k, '')

            p.append(make_html_row(k, value))
        '''


        p.append('</tr>')
    p.append('</tbody></table>')

    html_table = '\n'.join(p)




    return html_table


def get_html_record(record):

    if not record:
        return ''

    def get_line_item(k, v):
        
        value = ''

        if isinstance(v, dict):
            
            # if record is a dict, first check if it refers to a separate record, in which case show a link. 
            record_type = v.get('@type', None)
            record_id = v.get('@id', None)
            record_url = v.get('schema:url', None)
            record_name = v.get('schema:name', None)
            
            
            if record_name:
                text = record_name
            else:
                text = record_id


            # if type and id, Set value to link
                        
            
            if record_type and record_id:
                # Test if valid record
                if not isinstance(record_type, str): 
                    return ''
                if not isinstance(record_id, str): 
                    return ''


                url = '/' + record_type + '/' + record_id + '?format=html'
                value = get_html_link(url, text)
                return value
            
            # Else show values
            else:
                for sk in v:
                    path = k + '.' + sk
                    value = value + get_line_item(path, v[sk])
                return value

        # If list, iterate through items
        elif isinstance(v, list) and not isinstance(v, str): 
            for sv in v:
                value = value + get_line_item(k, sv) + '<br>'
            return value
                
        else:
            # If path is more than one element, show it
            if k.find('.') != -1:
                new_path = k + ': '
            else:
                new_path = ''
            # Add new data point
            if k.endswith('url'):
                value = get_html_link(str(v), str(v))
            else:
                value = value + new_path + str(v) + '<br>'
            return value


    # Get record info
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    record_url = record.get('schema:url', None)
    thumbnail_url = record.get('schema:thumbnailurl', None)

    image_records = record.get('schema:image', None)

    if image_records:
        if not isinstance(image_records,list):
            image_records = [image_records]
        image_record = image_records[0]

        if isinstance(image_record, str):
            image_record = {
                '@type': 'schema:imageobject',
                '@id': image_record,
                'schema:contenturl': image_record,
                'schema:url': image_record

            }

        image_record_type = image_record.get('@type, None')
        image_record_id = image_record.get('@id', None)
        if image_record_type and image_record_id:
            image_url = '/media/' + image_record_type + '/' + image_record_id
        else: image_url = None

    else:
        image_url = None

    # Get record html
    # iterate through dict 
    record_html = ''
    for k, v in sorted(record.items()):
        if k == 'kraken:related' or k == 'schema:links' or k == 'kraken:extracted' or k == 'kraken:process':
            continue
        item_value = get_line_item(k, v)
        record_html = record_html + '<dt class="col-sm-3">'
        record_html = record_html + str(k) + ':</dt>'
        record_html = record_html + '<dd class="col-sm-9">'
        record_html = record_html + item_value + '</dd>'

    record_html = '<dl class="row">' + record_html + '</dl>'
    
    return record_html


def get_html_media(record):
    # Returns empty string if not record
    if not record:
        return ''

    record_type = record.get('@type', None)
    record_contenturl = record.get('schema:contenturl', None)
    record_url = record.get('schema:url', None)
    record_thumbnailurl = record.get('schema:thumbnailurl', None)

    # Selects an url in order
    if record_thumbnailurl:
        media_url = record_thumbnailurl 
    elif record_contenturl:
        media_url = record_contenturl 
    else:
        return ''



    # Get media

    # If video, show player
    media_html = ''
    if record_type == 'schema:videoobject':
        value = '<div class="container-fluid"><video controls> <source src="'
        value = value + media_url
        value = value + '" type="video/mp4">Error</video></div><br><br>'
        media_html = value

    # if image object, show image
    else:
        value = '<div class="container-fluid"><img src="'
        value = value + media_url
        value = value + '" class="img-fluid"></div><br>'
        media_html = value

    return media_html

    
def get_html_link(url, text = None):
    ''' 
    Given a url and text, geenrate a html link'
    '''
    if not url:
        return ''

    if not text:
        text = url

    html_link = '<a href="'
    html_link = html_link + url
    html_link = html_link + '">'
    html_link = html_link + text
    html_link = html_link + '</a>'

    return html_link


def get_html_form(fields, action_url):
    '''
    Given an array of field names, return a html form
    '''

    html_form = ''

    # Form header
    html_form = html_form + '<form action="'
    html_form = html_form + action_url
    html_form = html_form + '">'

    # Add fields
    for i in fields:
        # Generate label
        f = '<label for="'
        f = f + i
        f = f + '">'
        f = f + i
        f = f + '</label><br>'

        # Generate input
        if fields[i].get('type', 'text') == 'text':
            f = f + '<input type="text" id="'
            f = f + i
            f = f + '" name="' + i + '" ><br>'

        elif fields[i].get('type', 'text') == 'textarea':
            f = f + '<textarea name="'
            f = f + i 
            f = f + '" rows="20" cols="60">'
            f = f + str(fields[i].get('default', ''))
            f = f + '</textarea><br>'

        # Combine iterator to main record
        html_form = html_form + f
    
    # Add submit button
    html_form = html_form + '<input type="submit" value="Submit">'
    
    # Finish form
    html_form = html_form + '</form>'

    return html_form


def get_html_section(title, html_content):
    
    # Inserts html_content in to oa collapsable section

    system_title = title.lower()
    system_title = system_title.replace(' ', '_')
    system_title = system_title.replace('(', '_')
    system_title = system_title.replace(')', '_')
    system_title = system_title.replace(':', '_')
    system_title = system_title.replace('/', '_')




    t = '''
        <p>
            <a class="btn btn-link" data-toggle="collapse" href="#{system_title}" role="button" aria-expanded="false" aria-controls="{system_title}">
                {title}
            </a>'
        </p>
        <div class="collapse" id="{system_title}">
            <div class="card card-body">
                {html_content}
            </div>
        </div>
    '''

   
    d = { 'title': title, 'system_title': system_title, 'html_content': html_content}
    html_section = t.format(**d)

    return html_section


def get_html_records_sections(extracted_records, main_title):
    # Get record types in extracted records for grouping
    
    # Error handling
    if not extracted_records:
        return ''
    if not isinstance(extracted_records, list):
        return ''
    if len(extracted_records) == 0:
        return ''


    # Process
    ext_record_types = []
    extracted_records_grouped = {}
    
    if extracted_records:
        for i in extracted_records:

            if i and isinstance(i, dict):
                ext_record_type = i.get('@type', None)
            else:
                ext_record_type = None
            
            # Add to type list if not duplicate
            if ext_record_type and ext_record_type not in ext_record_types:
                ext_record_types.append(ext_record_type)
                extracted_records_grouped[ext_record_type] = []
        
            # Add to records if not duplicate
            if i and ext_record_type and i not in extracted_records_grouped.get(ext_record_type, []):
                extracted_records_grouped[ext_record_type].append(i)

    if ext_record_types:
        ext_record_types.sort()


    # Get html for each sections
    extracted_content = ''
    for i in ext_record_types:

        extracted_records_grouped_sorted = sorted(extracted_records_grouped.get(i, []), key = lambda s: s.get('@id', ''))
        extracted_content_records = get_html_table(extracted_records_grouped_sorted)
        
        title = main_title + ' - ' + i + ' (' + str(len(extracted_records_grouped[i])) + ')'

        extracted_content_group = get_html_section(title, extracted_content_records)
        

        # Combine with others
        extracted_content = extracted_content + extracted_content_group
    return extracted_content


def get_html_text_editor():
    content = '''
        <!-- Include stylesheet -->
        <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">

        <!-- Create the editor container -->
        <div id="editor">
        <p>Hello World!</p>
        <p>Some initial <strong>bold</strong> text</p>
        <p><br></p>
        </div>

        <!-- Include the Quill library -->
        <script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>

        <!-- Initialize Quill editor -->
        <script>
        var quill = new Quill('#editor', {
            theme: 'snow'
        });
        </script>


    '''
    return content