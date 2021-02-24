


class Html_section:

    def __init__(self):

        a = 1


    def section(self, title, content, expanded = False):
        
        # Inserts html_content into a collapsable section

        # Remove non aascii characters for system title
        system_title = title.encode("ascii", "replace")
        system_title = 'section_' + system_title.decode("ascii", "replace").lower()

        # Convert true false in string
        js_expanded = str(expanded).lower()


        t = '''
            <p>
                <a class="btn btn-link" data-toggle="collapse" data-bs-toggle="collapse" href="#{system_title}" role="button" aria-expanded="{expanded}" aria-controls="{system_title}">{title}</a>
            </p>
            <div class="collapse" id="{system_title}">
                <div class="card card-body">
                    {html_content}
                </div>
            </div>
            '''

    
        d = { 'title': title, 'system_title': system_title, 'html_content': content, 'expanded': js_expanded}

        content = t.format(**d)

        return content