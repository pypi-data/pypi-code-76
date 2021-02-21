


class Html_card:

    def __init__(self):

        a = 1

    def card(self, title, text, contenturl, url):



        card = '''
            <div class="card">
                <img class="card-img-top" src="{card_url}" alt="Card image cap">
                <div class="card-body">
                <h6 class="card-title">{card_title}</h6>
                <p class="card-text">{card_text}</p>
                </div>
                <div class="card-footer">
                <small class="text-muted">Last updated 3 mins ago</small>
                </div>
            </div>
                '''
        d = { 'card_title': title, 'card_text': text, 'card_url': contenturl, 'card_record_link': url }
        content = card.format(**d)

        return content

    def card_backup(self, title, contenturl, url):



        card = '''
            <a href="{card_record_link}">
            <div class="card">
                <img src="{card_url}" class="card-img-top" alt="{card_title}">
                <div class="card-body">
                
                </div></div>
                </a>
                '''
        d = { 'card_title': title, 'card_url': contenturl, 'card_record_link': url }
        content = card.format(**d)

        return content


    def cards(self, values):

        content = ''
        content += '<div class="card-columns">'

        for i in values:

            title = self._get_title(i)
            contenturl = self._get_contenturl(i)
            url = self._get_record_url(i)

            content += self.card(title, '', contenturl, url)

        content += '</div>'

        return content




    def _get_contenturl(self, value):

        contenturl = None

        fields = ['schema:contenturl', 'schema:thumbnailurl']

        for i in fields:
            contenturl = value.get(i, None)
            if contenturl:
                return contenturl

        return ''

    def _get_title(self, value):

        new_value = None

        fields = ['schema:name', '@id']

        for i in fields:
            new_value = value.get(i, None)
            if new_value:
                return new_value

        return ''

    def _get_record_url(self, value):

        new_value = '/' + value.get('@type', None) + '/' + value.get('@id', None)

        return new_value
