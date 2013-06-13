import os, web, socket, json, pprint, time

# render
render = web.template.render( os.path.dirname(__file__) + '/templates/')

# db connect

abspath = os.path.dirname(__file__)
os.chdir(abspath)

urls = (
    '/', 'webmain',
    )
app = web.application(urls, globals())


def return_composite_parts(main):
    header = unicode(render.header())
    footer = unicode(render.footer())
    return render.layout(header, main, footer)


class webmain:
    def GET(self):
        main = unicode(render.main(self))
        return return_composite_parts(main)


if __name__ == '__main__':
    app.run()
