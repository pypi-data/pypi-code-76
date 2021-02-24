
'''
Initialize bavbar by sending title and array of 'link' and 'text' values for menu


'''

class Html_navbar:

    def __init__(self):
        a=1


    def navbar(self, title, value):

        content = ''

        content += self._navbar_header(title)

        for i in value:
            content += self._navbar_item(i)
        
        content += self._navbar_footer()

        return content


    def _navbar_header(self, title):

        content = '''
            <header>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <a class="navbar-brand" href="#">Navbar</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
            '''
        return content

    def _navbar_item(self, value):

        content = '''
            <li class="nav-item active">
                <a class="nav-link" href="{link}">{text}<span class="sr-only">(current)</span></a>
            </li>
            '''.format(link = value.get('link', ''), text = value.get('text', ''))

        return content



    def _navbar_footer(self):
        content = '''            
                        </ul>
                    </div>
                </nav>
                </header>
            '''
        
        return content