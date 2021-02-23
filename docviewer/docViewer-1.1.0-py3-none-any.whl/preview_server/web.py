import tornado.web


class LitePreview(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument('filename', None)
        if not filename:
            return self.render('error.html', msg='filename not provide')
        return self.render('lite-preview.html', filename=filename)
