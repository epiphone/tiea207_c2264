from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def index():
    __lineoffset__ = -5
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<div class="container">\n'])
    extend_([u'<div class="hero-unit">\n'])
    extend_([u'\n'])
    extend_([u'<h1>Joukkoliikenteen hintavertailu</h1><small>prototyyppi</small>\n'])
    extend_([u'<form class="form-horizontal" method="GET" action="/haku">\n'])
    extend_([u'  <input type="hidden" id="inputTyyppi" name="aikatyyppi" value="saapumisaika"/>\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputMista" class="control-label">Mist\xe4</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input class="input" id="inputMista" type="text" name="mista" autocomplete="off" required autofocus/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputMihin" class="control-label">Mihin</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input id="inputMihin" type="text" name="mihin" autocomplete="off" required/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputTunnit" class="control-label">Aika ja Pvm</label>\n'])
    extend_([u'    <div class="controls form-inline">\n'])
    extend_([u'      <input type="text" class="input-xmini" id="inputTunnit" name="h"/>\n'])
    extend_([u'      <input type="text" class="input-xmini" id="inputMinuutit" name="min"/>\n'])
    extend_([u'      <input type="text" class="input-small" id="inputPvm" name="pvm"/>\n'])
    extend_([u'\n'])
    extend_([u'      <div class="btn-group">\n'])
    extend_([u'        <button id="btnAikatyyppi" class="btn dropdown-toggle" data-toggle="dropdown">Saapumisaika<span class="caret"></span>\n'])
    extend_([u'        </button>\n'])
    extend_([u'        <ul class="dropdown-menu">\n'])
    extend_([u'          <li><a id="aAikatyyppi">L\xe4ht\xf6aika</a></li>\n'])
    extend_([u'        </ul>\n'])
    extend_([u'      </div>\n'])
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
    extend_([u'</div> <!-- /.hero-unit -->\n'])
    extend_([u'</div> <!-- /.container -->\n'])
    extend_([u'\n'])
    extend_([u'<script src="static/js/paikannimet.js"></script>\n'])
    extend_([u'<script>\n'])
    extend_([u'window.onload = function() {\n'])
    extend_([u'  // Asetetaan oletusl\xe4ht\xf6aika ja l\xe4ht\xf6pvm\n'])
    extend_([u'  var dt = new Date();\n'])
    extend_([u'  ', u'$', u'("#inputPvm").val([dt.getDate(), dt.getMonth() + 1, dt.getFullYear()].join("."));\n'])
    extend_([u'  ', u'$', u'("#inputTunnit").val(dt.getHours() + 1);\n'])
    extend_([u'  ', u'$', u'("#inputMinuutit").val(dt.getMinutes());\n'])
    extend_([u'\n'])
    extend_([u'  // L\xe4ht\xf6aika/Saapumisaika-valitsin\n'])
    extend_([u'  ', u'$', u'("#aAikatyyppi").click(function() {\n'])
    extend_([u'    var btn = ', u'$', u'("#btnAikatyyppi")[0],\n'])
    extend_([u'        vanhaTyyppi = ', u'$', u'(btn).text().trim(),\n'])
    extend_([u'        uusiTyyppi = ', u'$', u'(this).text().trim();\n'])
    extend_([u'    ', u'$', u'(this).text(vanhaTyyppi);\n'])
    extend_([u'    ', u'$', u'(btn).text(uusiTyyppi);\n'])
    extend_([u'    if (uusiTyyppi == "L\xe4ht\xf6aika") {\n'])
    extend_([u'      ', u'$', u'("#inputTyyppi").val("lahtoaika");\n'])
    extend_([u'    } else {\n'])
    extend_([u'      ', u'$', u'("#inputTyyppi").val("saapumisaika");\n'])
    extend_([u'    }\n'])
    extend_([u'  })\n'])
    extend_([u'\n'])
    extend_([u'  ', u'$', u'("#inputTyyppi").val("saapumisaika"); // Asetetaan oletusarvo\n'])
    extend_([u'\n'])
    extend_([u'  // Datepicker\n'])
    extend_([u'  var dpSettings = {\n'])
    extend_([u'    dateFormat: "dd.mm.yy",\n'])
    extend_([u'    dayNamesMin: ["Ma","Ti","Ke","To","Pe","La","Su"],\n'])
    extend_([u'    monthNames: ["Tammi","Helmi","Maalis","Huhti","Touko","Kes\xe4", "Hein\xe4","Elo","Syys","Loka","Marras","Joulu"],\n'])
    extend_([u'    defaultDate: null\n'])
    extend_([u'  };\n'])
    extend_([u'  ', u'$', u'("#inputPvm").datepicker(dpSettings);\n'])
    extend_([u'\n'])
    extend_([u'  // Autocomplete\n'])
    extend_([u'  ', u'$', u'("input[name=\'mista\'],input[name=\'mihin\']").typeahead({source: paikat});\n'])
    extend_([u'}\n'])
    extend_([u'</script>\n'])

    return self

index = CompiledTemplate(index, 'templates/index.html')
join_ = index._join; escape_ = index._escape

# coding: utf-8
def results (matkat, params, t):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<strong>', escape_(t, True), u' s</strong>\n'])
    for k, v in loop.setup(params.iteritems()):
        extend_([escape_(k, True), u'=<strong>', escape_(v, True), u'</strong>\n'])
        extend_([u'\n'])
    if len(matkat) == 0 or matkat is None:
        extend_([u'<h1>Ei tuloksia</h1>\n'])
        extend_([u'\n'])
    else:
        if "juna" in matkat:
            extend_([u'<h2>Junayhteydet:</h2>\n'])
            if "virhe" in matkat["juna"]:
                extend_([u'<strong>Virhe! ', escape_(matkat["juna"]["virhe"], True), u'</strong>\n'])
            else:
                for yhteys in loop.setup(matkat["juna"]):
                    extend_([u'<strong>#', escape_(loop.index, True), u' ', escape_(yhteys["mista"], True), u' - ', escape_(yhteys["mihin"], True), u'</strong> (', escape_(yhteys["lahtoaika"], True), u' - ', escape_(yhteys["saapumisaika"], True), u') - Kesto: ', escape_(yhteys["kesto"], True), u' Hinta: ', escape_(yhteys["hinnat"][0], True), u'\u20ac<br>\n'])
                    for vaihto in loop.setup(yhteys["vaihdot"]):
                        if "lahtopaikka" in vaihto:
                            extend_([u'<small> - ', escape_(vaihto["tyyppi"], True), u' ', escape_(vaihto["lahtopaikka"], True), u' - ', escape_(vaihto["saapumispaikka"], True), u' (', escape_(vaihto["lahtoaika"], True), u' - ', escape_(vaihto["saapumisaika"], True), u')</small><br>\n'])
                        elif "mista" in vaihto:
                            extend_([u'<small> - ', escape_(vaihto["tyyppi"], True), u' ', escape_(vaihto["mista"], True), u' - ', escape_(vaihto["mihin"], True), u' (', escape_(vaihto["lahtoaika"], True), u' - ', escape_(vaihto["saapumisaika"], True), u')</small><br>\n'])
                    extend_([u'<br>\n'])
                    extend_([u'\n'])
        if "bussi" in matkat:
            extend_([u'<h2>Bussiyhteydet:</h2>\n'])
            if "virhe" in matkat["bussi"]:
                extend_([u'<strong>Virhe!</strong> ', escape_(matkat["bussi"]["virhe"], True), u'\n'])
            else:
                for yhteys in loop.setup(matkat["bussi"]):
                    extend_([u'<strong>#', escape_(loop.index, True), u' ', escape_(yhteys["mista"], True), u' - ', escape_(yhteys["mihin"], True), u'</strong> (', escape_(yhteys["lahtoaika"], True), u' - ', escape_(yhteys["saapumisaika"], True), u') - Kesto: ', escape_(yhteys["kesto"], True), u' Hinta: ', escape_(yhteys["hinnat"][0], True), u'\u20ac<br>\n'])
                    for vaihto in loop.setup(yhteys["vaihdot"]):
                        extend_([u'<small> - ', escape_(vaihto["tyyppi"], True), u' ', escape_(vaihto["mista"], True), u' - ', escape_(vaihto["mihin"], True), u' (', escape_(vaihto["lahtoaika"], True), u' - ', escape_(vaihto["saapumisaika"], True), u')</small><br>\n'])
                    extend_([u'<br>\n'])
                    extend_([u'\n'])
        if "auto" in matkat:
            extend_([u'<h2>Autoyhteydet:</h2>\n'])
            if "virhe" in matkat["auto"]:
                extend_([u'<strong>Virhe!</strong> ', escape_(matkat["auto"]["virhe"], True), u'\n'])
            else:
                extend_([u'<strong>', escape_(matkat["auto"]["mista"], True), u' - ', escape_(matkat["auto"]["mihin"], True), u'</strong><br>\n'])
                extend_([u'Matkan pituus: ', escape_(matkat["auto"]["matkanpituus"], True), u' km<br>\n'])
                extend_([u'Kesto: ', escape_(matkat["auto"]["kesto"], True), u'<br>\n'])
                if "hinnat" in matkat["auto"]:
                    h1, h2, strong = matkat["auto"]["hinnat"]
                    extend_([u'Hinnat: <b>', escape_(h1, True), u'</b>\u20ac (95E10), <b>', escape_(h2, True), u'</b>\u20ac (98E), <b>', escape_(strong, True), u'</b>\u20ac (Diesel)<br>\n'])
                else:
                    extend_([u'Hintojen hakeminen ep\xe4onnistui.\n'])
            extend_([u'<br>\n'])
            extend_([u'\n'])
    extend_([u'<a href="/">Takaisin</a>\n'])

    return self

results = CompiledTemplate(results, 'templates/results.html')
join_ = results._join; escape_ = results._escape

# coding: utf-8
def results_vis (matkat, params, t, dt, pvm):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<strong>', escape_(t, True), u' s</strong>\n'])
    for k, v in loop.setup(params.iteritems()):
        extend_([escape_(k, True), u'=<strong>', escape_(v, True), u'</strong>\n'])
    extend_([escape_(dt, True), u'=<strong>', escape_(dt, True), u'</strong>\n'])
    extend_([u'\n'])
    extend_([u'<div id="option">\n'])
    extend_([u'    <input type="button" value="l\xe4ht\xf6" onclick="sortByDt1()"/>\n'])
    extend_([u'    <input type="button" value="saapuminen" onclick="sortByDt2()"/>\n'])
    extend_([u'    <input type="button" value="kesto" onclick="sortByDuration()"/>\n'])
    extend_([u'    <input type="button" value="hinta" onclick="sortByPrice()"/>\n'])
    extend_([u'    <input type="button" value="vaihdot" onclick="sortByTransfers()"/>\n'])
    extend_([u'</div>\n'])
    extend_([u'<div class="results"></div>\n'])
    extend_([u'\n'])
    extend_([u'<script>\n'])
    
    def hinta(hinnat):
        for h in hinnat:
            if h:
                return h
        return 999.9
    
    extend_([u'var query_date = "', escape_(dt, True), u'";\n'])
    extend_([u'var data = [\n'])
    if "juna" in matkat:
        for matka in loop.setup(matkat["juna"]):
            extend_([u'{"transfers":', escape_(len(matka["vaihdot"]), True), u', "type":"juna", "price":', escape_(matka["hinnat"][1], True), u',"date":"', escape_(formatoi_aika_js(pvm, matka["lahtoaika"]), True), u'", "total":', escape_(kesto_tunneiksi(matka["kesto"]), True), u', "duration":"', escape_(matka["kesto"], True), u'", "name":"', escape_(matka["mista"], True), u' - ', escape_(matka["mihin"], True), u'"},\n'])
    if "bussi" in matkat:
        for matka in loop.setup(matkat["bussi"]):
            extend_([u'{"transfers":', escape_(len(matka["vaihdot"]), True), u', "type":"bussi", "price":', escape_(hinta(matka["hinnat"]), True), u',"date":"', escape_(formatoi_aika_js(pvm, matka["lahtoaika"]), True), u'", "total":', escape_(kesto_tunneiksi(matka["kesto"]), True), u', "duration":"', escape_(matka["kesto"], True), u'", "name":"', escape_(matka["mista"], True), u' - ', escape_(matka["mihin"], True), u'"},\n'])
    if "auto" in matkat:
        matka = matkat["auto"]
        extend_([u'{"type":"auto", "price":', escape_(matka["hinnat"][0], True), u',"date":"', escape_(formatoi_aika_js(pvm, matka["lahtoaika"]), True), u'", "total":', escape_(kesto_tunneiksi(matka["kesto"]), True), u', "duration":"', escape_(matka["kesto"], True), u'", "name":"', escape_(matka["mista"], True), u' - ', escape_(matka["mihin"], True), u'"},\n'])
        extend_([u'\n'])
    extend_([u'//{"transfers":3,"duration":"3:20","type":"juna","name":"JunaBussi","price":36.44,"date":"2013-05-16T02:30","total":2}\n'])
    extend_([u'];\n'])
    extend_([u'\n'])
    extend_([u'\n'])
    extend_([u'\n'])
    extend_([u'</script>\n'])
    extend_([u'<script src="/static/js/d3.v3.min.js"></script>\n'])
    extend_([u'<script src="/static/js/d3testi.js"></script>\n'])

    return self

results_vis = CompiledTemplate(results_vis, 'templates/results_vis.html')
join_ = results_vis._join; escape_ = results_vis._escape

# coding: utf-8
def base (content):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<!DOCTYPE html>\n'])
    extend_([u'<html>\n'])
    extend_([u'<head>\n'])
    extend_([u'  <meta charset="utf-8">\n'])
    extend_([u'  <title>Joukkoliikenteen hintavertailu - prototyyppi</title>\n'])
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
    extend_([u'<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>\n'])
    extend_([u'<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"></script>\n'])
    extend_([u'<script src="/static/js/bootstrap.min.js"></script>\n'])
    extend_([u'\n'])
    extend_([u'</body>\n'])
    extend_([u'</html>\n'])

    return self

base = CompiledTemplate(base, 'templates/base.html')
join_ = base._join; escape_ = base._escape

