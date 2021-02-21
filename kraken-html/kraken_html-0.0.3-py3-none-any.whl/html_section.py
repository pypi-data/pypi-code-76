


class Html_section:

    def __init__(self):

        a = 1


    def section(self, title, content):
        
        # Inserts html_content into a collapsable section

        system_title = title.encode("ascii", "ignore")



        t = '''
            <p>
                <a class="btn btn-link" data-toggle="collapse" href="#{system_title}" role="button" aria-expanded="false" aria-controls="{system_title}">
                    {title}
                </a>
            </p>
            <div class="collapse" id="{system_title}">
                <div class="card card-body">
                    {html_content}
                </div>
            </div>
        '''

    
        d = { 'title': title, 'system_title': system_title, 'html_content': content}

        content = t.format(**d)

        return content