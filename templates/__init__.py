from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def base (content):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE html>\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'  <meta charset="UTF-8">\n'])
    extend_([u'  <title>Joukkoliikenteen hintavertailu</title>\n'])
    extend_([u'  <meta name="description" content="description t\xe4h\xe4n">\n'])
    extend_([u'  <meta name="keywords" content="keywordsit t\xe4h\xe4n">\n'])
    extend_([u'  <meta name="author" content="authorit t\xe4h\xe4n">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/style.css">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap-responsive.min.css">\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'\n'])
    extend_([u'  ', escape_(content, False), u'\n'])
    extend_([u'\n'])
    extend_([u'<script src="/static/js/jquery.js"></script>\n'])
    extend_([u'<script src="/static/js/bootstrap.min.js"></script>\n'])
    extend_([u'\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

base = CompiledTemplate(base, 'templates\\base.html')
join_ = base._join; escape_ = base._escape

# coding: utf-8
def index():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<div class="container">\n'])
    extend_([u'<div class="row">\n'])
    extend_([u'<div class"span4">\n'])
    extend_([u'\n'])
    extend_([u'<form class="form-horizontal" method="GET" action="/haku">\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label class="control-label">Mist\xe4</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'        <input class="input" type="text" name="mista" placeholder="Mist\xe4"/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label class="control-label">Mihin</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input type="text" name="mihin" placeholder="Mihin"/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label class="control-label">L\xe4ht\xf6aika</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input type="text" name="lahtoaika" placeholder="01.01.2013 02:01"/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label class="control-label">Mist\xe4</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input type="text" name="saapumisaika" placeholder="01.01.2013 02:01"/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <label class="checkbox inline">\n'])
    extend_([u'        <input type="checkbox" name="juna" checked> Juna\n'])
    extend_([u'      </label>\n'])
    extend_([u'      <label class="checkbox inline">\n'])
    extend_([u'        <input type="checkbox" name="bussi" checked> Bussi\n'])
    extend_([u'      </label>\n'])
    extend_([u'      <label class="checkbox inline">\n'])
    extend_([u'        <input type="checkbox" name="auto" checked> Auto\n'])
    extend_([u'      </label>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control group">\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <button class="btn btn-primary" type="submit">Hae yhteyksi\xe4</button>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'</form>\n'])
    extend_([u'\n'])
    extend_([u'</div>\n'])
    extend_([u'</div>\n'])
    extend_([u'</div>\n'])

    return self

index = CompiledTemplate(index, 'templates\\index.html')
join_ = index._join; escape_ = index._escape

