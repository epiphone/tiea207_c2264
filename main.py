# -*-coding:utf-8-*-
# Joukkoliikenteen hintavertailusovellus


import web


urls = (
    "/", "Index"
)


class Index:
    def GET(self):
        return "hellou"


if __name__ == "__main__":
    app = web.application(urls, globals(), True)
    web.config.debug = True
    app.run()
