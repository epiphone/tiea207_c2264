# -*-coding:utf-8-*-
# Joukkoliikenteen hintavertailusovellus


import web


urls = (
    "/", "Index"
)

render = web.template.render("templates/", base="base")


class Index:
    def GET(self):
        return render.index()


if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    web.config.debug = True
    app.run()
