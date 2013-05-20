from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def index (aleluokat):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'<div class="container index-container">\n'])
    extend_([u'\n'])
    extend_([u'<div class="header">\n'])
    extend_([u'  <div class="hidden-phone">\n'])
    extend_([u'    <h1>Mill\xe4 matkaan?</h1>\n'])
    extend_([u'    <p>Julkisen liikenteen ja henkil\xf6autoilun vertailusovellus</p>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="visible-phone">\n'])
    extend_([u'    <h2>Mill\xe4 matkaan?</h2>\n'])
    extend_([u'    <h4>Julkisen liikenteen ja henkil\xf6autoilun vertailusovellus</h4>\n'])
    extend_([u'  </div>\n'])
    extend_([u'</div> <!-- /.header -->\n'])
    extend_([u'\n'])
    extend_([u'<div class="form-container">\n'])
    extend_([u'<form class="form-horizontal" method="GET" action="/haku">\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputMista" class="control-label">Mist\xe4</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input class="input" id="inputMista" type="text" name="mista" autocomplete="off" required autofocus/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputMihin" class="control-label">Minne</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <input id="inputMihin" type="text" name="mihin" autocomplete="off" required/>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputTunnit" class="control-label">Aika ja Pvm</label>\n'])
    extend_([u'      <div class="controls form-inline">\n'])
    extend_([u'        <input type="text" class="input-xmini" id="inputTunnit" name="h" pattern="([01]?[0-9]|2[0-3])">\n'])
    extend_([u'        <small>:</small>\n'])
    extend_([u'        <input type="text" class="input-xmini" id="inputMinuutit" name="min" pattern="[0-5]?[0-9]">\n'])
    extend_([u'        <input type="text" class="input-small" id="inputPvm" name="pvm" autocomplete="off" required pattern="([0-2]?[0-9]|3[0-1])\\.([1-9]|0[1-9]|1[0-2])\\.(20)?1[3-9]">\n'])
    extend_([u'\n'])
    extend_([u'        <div class="btn-group">\n'])
    extend_([u'          <select id="inputAikatyyppi" class="input-medium" name="tyyppi">\n'])
    extend_([u'            <option value="saapumisaika">Saapumisaika</option>\n'])
    extend_([u'            <option value="lahtoaika">L\xe4ht\xf6aika</option>\n'])
    extend_([u'          </select>\n'])
    extend_([u'        </div>\n'])
    extend_([u'      </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'       <div id="datepicker" style="font-family: default; font-size: 12px; line-height: 18px;">\n'])
    extend_([u'       </div>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputAlennusluokka" class="control-label">Alennusluokka</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <select id="inputAlennusluokka" class="input-medium" name="ale">\n'])
    for val, luokka in loop.setup(aleluokat):
        extend_(['        ', u'<option value="', escape_(val, True), u'">', escape_(luokka, True), u'</option>\n'])
    extend_([u'      </select>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'\n'])
    extend_([u'  <div class="control-group">\n'])
    extend_([u'    <label for="inputKeskikulutus" class="control-label">Auton keskikulutus</label>\n'])
    extend_([u'    <div class="controls">\n'])
    extend_([u'      <select id="inputKeskikulutus" class="input-large" name="kulutus">\n'])
    extend_([u'        <option value="0">95E, Pieni (4,5l/100km)</option>\n'])
    extend_([u'        <option value="1">95E, Keski(6,5l/100km)</option>\n'])
    extend_([u'        <option value="2">95E, Suuri (8,5l/100km)</option>\n'])
    extend_([u'        <option class="select-dash" disabled>----</option>\n'])
    extend_([u'        <option value="3">98E, Pieni (4,5l/100km)</option>\n'])
    extend_([u'        <option value="4">98E, Keski (6,5l/100km)</option>\n'])
    extend_([u'        <option value="5">98E, Suuri (8,5l/100km)</option>\n'])
    extend_([u'        <option class="select-dash" disabled>----</option>\n'])
    extend_([u'        <option value="6">Di, Pieni (3,7l/100km)</option>\n'])
    extend_([u'        <option value="7">Di, Keski (5,7l/100km)</option>\n'])
    extend_([u'        <option value="8">Di, Suuri (7,7l/100km)</option>\n'])
    extend_([u'      </select>\n'])
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
    extend_([u'      <button class="btn btn-primary" type="submit">Hae yhteyksi\xe4 <i class="icon-search icon-white"></i></button>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </div>\n'])
    extend_([u'</form>\n'])
    extend_([u'\n'])
    extend_([u'</div> <!-- /.form-container -->\n'])
    extend_([u'</div> <!-- /.container -->\n'])
    extend_([u'\n'])
    extend_([u'<hr>\n'])
    extend_([u'<div class="container footer">\n'])
    extend_([u'  <a href="/info">Ohje ja tietoja</a>\n'])
    extend_([u'  <small> - </small>\n'])
    extend_([u'  <a href="/palaute">Anna palautetta</a>\n'])
    extend_([u'  <br>\n'])
    extend_([u'  <a href="https://github.com/epiphone/tiea207_c2264">@Github</a>\n'])
    extend_([u'</div>\n'])
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
    extend_([u'  // Datepicker\n'])
    extend_([u'  var dpSettings = {\n'])
    extend_([u'    altField: "#inputPvm",\n'])
    extend_([u'    minDate: 0,\n'])
    extend_([u'    altFormat: "d.m.yy",\n'])
    extend_([u'    dayNamesMin: ["Ma","Ti","Ke","To","Pe","La","Su"],\n'])
    extend_([u'    monthNames: ["Tammi","Helmi","Maalis","Huhti","Touko","Kes\xe4", "Hein\xe4","Elo","Syys","Loka","Marras","Joulu"]\n'])
    extend_([u'  };\n'])
    extend_([u'\n'])
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
def results (matkat, params, t, dt, pvm, h, mins, aikatyyppi, aleluokka, aleluokat):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u'DEBUG\n'])
    extend_([u'<strong>', escape_(t, True), u' s</strong>\n'])
    for k, v in loop.setup(params.iteritems()):
        extend_([escape_(k, True), u'=<strong>', escape_(v, True), u'</strong>\n'])
    extend_([u'dt=<strong>', escape_(dt, True), u'</strong>\n'])
    extend_([u'\n'])
    extend_([u'<div class="container-fluid">\n'])
    extend_([u'<div class="row-fluid">\n'])
    extend_([u'\n'])
    extend_([u'<!-- Hakulomake sivupalkissa -->\n'])
    extend_([u'<div class="span3">\n'])
    extend_([u'<div class="well sidebar-nav sidebar-nav-fixed">\n'])
    extend_([u'  <h4>Hae yhteyksi\xe4</h4>\n'])
    extend_([u'  <div class="breaker"></div>\n'])
    extend_([u'  <br>\n'])
    extend_([u'  <form class="form-horizontal" method="GET" action="/haku">\n'])
    extend_([u'    <label for="inputMista">Mist\xe4</label>\n'])
    extend_([u'    <input class="input input-medium" id="inputMista" type="text" name="mista" autocomplete="off" value="', escape_(params["mista"].title(), True), u'" required autofocus/>\n'])
    extend_([u'    <label for="inputMihin">Minne</label>\n'])
    extend_([u'    <input class="input input-medium" id="inputMihin" type="text" name="mihin" autocomplete="off" value="', escape_(params["mihin"].title(), True), u'" required/>\n'])
    extend_([u'    <div class="breaker"></div>\n'])
    extend_([u'    <br>\n'])
    extend_([u'    <label>Aika ja Pvm</label>\n'])
    extend_([u'    <input type="text" class="input-xmini" id="inputTunnit" name="h" value="', escape_(h, True), u'" pattern="([01]?[0-9]|2[0-3])">\n'])
    extend_([u'    <small>:</small>\n'])
    extend_([u'    <input type="text" class="input-xmini" id="inputMinuutit" name="min" value="', escape_(mins, True), u'" pattern="[0-5]?[0-9]">\n'])
    extend_([u'    <input type="text" class="input-small" id="inputPvm" name="pvm" autocomplete="off" value="', escape_(pvm, True), u'" pattern="([0-2]?[0-9]|3[0-1])\\.([1-9]|0[1-9]|1[0-2])\\.(20)?1[3-9]">\n'])
    extend_([u'    <br>\n'])
    extend_([u'    <select id="inputAikatyyppi" class="input input-medium" name="tyyppi">\n'])
    extend_([u'      <option value="saapumisaika">Saapumisaika</option>\n'])
    if aikatyyppi == "lahtoaika":
        extend_(['      ', u'<option value="lahtoaika" selected>L\xe4ht\xf6aika</option>\n'])
    else:
        extend_(['      ', u'<option value="lahtoaika">L\xe4ht\xf6aika</option>\n'])
    extend_([u'    </select>\n'])
    extend_([u'    <div class="breaker"></div>\n'])
    extend_([u'    <br>\n'])
    extend_([u'    <label>Alennusluokka</label>\n'])
    extend_([u'    <select class="input input-large" name="ale">\n'])
    for val, luokka in loop.setup(aleluokat):
        if aleluokka == val:
            extend_(['      ', u'<option value="', escape_(val, True), u'" selected>', escape_(luokka, True), u'</option>\n'])
        else:
            extend_(['      ', u'<option value="', escape_(val, True), u'">', escape_(luokka, True), u'</option>\n'])
    extend_([u'    </select>\n'])
    extend_([u'    <label>Auton keskikulutus</label>\n'])
    extend_([u'    <select id="inputKeskikulutus" class="input input-large" name="kulutus">\n'])
    extend_([u'      <option value="0">95E, Pieni (4,5l/100km)</option>\n'])
    extend_([u'      <option value="1">95E, Keski(6,5l/100km)</option>\n'])
    extend_([u'      <option value="2">95E, Suuri (8,5l/100km)</option>\n'])
    extend_([u'      <option class="select-dash" disabled>----</option>\n'])
    extend_([u'      <option value="3">98E, Pieni (4,5l/100km)</option>\n'])
    extend_([u'      <option value="4">98E, Keski (6,5l/100km)</option>\n'])
    extend_([u'      <option value="5">98E, Suuri (8,5l/100km)</option>\n'])
    extend_([u'      <option class="select-dash" disabled>----</option>\n'])
    extend_([u'      <option value="6">Di, Pieni (3,7l/100km)</option>\n'])
    extend_([u'      <option value="7">Di, Keski (5,7l/100km)</option>\n'])
    extend_([u'      <option value="8">Di, Suuri (7,7l/100km)</option>\n'])
    extend_([u'    </select>\n'])
    extend_([u'    <br>\n'])
    extend_([u'\n'])
    extend_([u'    <label class="checkbox inline">\n'])
    extend_([u'      <input type="checkbox" name="juna" checked> Juna\n'])
    extend_([u'    </label>\n'])
    extend_([u'    <label class="checkbox inline">\n'])
    extend_([u'      <input type="checkbox" name="bussi" checked> Bussi\n'])
    extend_([u'    </label>\n'])
    extend_([u'    <label class="checkbox inline">\n'])
    extend_([u'      <input type="checkbox" name="auto" checked> Auto\n'])
    extend_([u'    </label>\n'])
    extend_([u'    <br>\n'])
    extend_([u'    <div class="breaker"></div>\n'])
    extend_([u'    <br>\n'])
    extend_([u'    <button class="btn btn-primary" type="submit">Hae yhteyksi\xe4<i class="icon-search icon-white"></i></button>\n'])
    extend_([u'  </form>\n'])
    extend_([u'</div> <!-- /.sidebar-nav-fixed -->\n'])
    extend_([u'</div> <!-- /.span3 -->\n'])
    extend_([u'\n'])
    extend_([u'\n'])
    extend_([u'<!-- Hakutulokset -->\n'])
    extend_([u'<div class="span9 well">\n'])
    extend_([u'<div class="results-header">\n'])
    extend_([u'  <h3>', escape_(params["mista"].title(), True), u' - ', escape_(params["mihin"].title(), True), u'</h3>\n'])
    extend_([u'  <small>J\xe4rjestys:</small>\n'])
    extend_([u'  <div class="btn-group">\n'])
    extend_([u'    <button class="btn btn-link btn-small disabled" onclick="sortByDt1()" >L\xe4ht\xf6</button>\n'])
    extend_([u'    <button class="btn btn-link btn-small" onclick="sortByDt2()">Saapuminen</button>\n'])
    extend_([u'    <button class="btn btn-link btn-small" onclick="sortByDuration()">Kesto</button>\n'])
    extend_([u'    <button class="btn btn-link btn-small" onclick="sortByPrice()">Hinta</button>\n'])
    extend_([u'    <button class="btn btn-link btn-small" onclick="sortByTransfers()">Vaihdot</button>\n'])
    extend_([u'  </div>\n'])
    extend_([u'</div>\n'])
    extend_([u'\n'])
    extend_([u'<div class="results"></div>\n'])
    extend_([u'</div> <!-- /.span* -->\n'])
    extend_([u'</div> <!-- /.container -->\n'])
    extend_([u'</div> <!-- /.row -->\n'])
    extend_([u'\n'])
    extend_([u'<script src="static/js/paikannimet.js"></script>\n'])
    extend_([u'<script>\n'])
    extend_([u'window.onload = function() {\n'])
    extend_([u'\n'])
    extend_([u'// Datepicker:\n'])
    extend_([u'var dpSettings = {\n'])
    extend_([u'    altField: "#inputPvm",\n'])
    extend_([u'    minDate: 0,\n'])
    extend_([u'    altFormat: "d.m.yy",\n'])
    extend_([u'    dayNamesMin: ["Ma","Ti","Ke","To","Pe","La","Su"],\n'])
    extend_([u'    monthNames: ["Tammi","Helmi","Maalis","Huhti","Touko","Kes\xe4", "Hein\xe4","Elo","Syys","Loka","Marras","Joulu"]\n'])
    extend_([u'};\n'])
    extend_([u'$', u'("#inputPvm").datepicker(dpSettings);\n'])
    extend_([u'\n'])
    extend_([u'// Visualisaatio:\n'])
    extend_([u'var query_date = "', escape_(dt, True), u'";\n'])
    extend_([u'var data = [\n'])
    extend_([u'\n'])
    if "auto" in matkat and not "virhe" in matkat["auto"]:
        m = matkat["auto"]
        extend_([u'{"luokka":"auto","lahtoaika":"', escape_(m["js_aika"], True), u'","tunnit":', escape_(m["tunnit"], True), u',"kesto":"', escape_(m["kesto"], True), u'","hinta":', escape_(m["hinta"], True), u',"vaihdot_lkm":0,"tyyppi":"Auto"},\n'])
        extend_([u'\n'])
    
    mh_ja_vr = []
    for x in ["juna", "bussi"]:
        if x in matkat and not "virhe" in matkat[x]:
            mh_ja_vr += matkat[x]
    
    for m in loop.setup(mh_ja_vr):
        extend_([u'{"luokka":"', escape_(m["luokka"], True), u'","lahtoaika":"', escape_(m["js_aika"], True), u'","tunnit":', escape_(m["tunnit"], True), u',"kesto":"', escape_(m["kesto"], True), u'","hinta":', escape_(m["hinta"], True), u',"vaihdot_lkm":', escape_(m["vaihdot_lkm"], True), u',"tyyppi":"', escape_(m["tyyppi"], True), u'"},\n'])
    extend_([u'];\n'])
    extend_([u'\n'])
    extend_([u'init(data, query_date);\n'])
    extend_([u'\n'])
    extend_([u'// Autocomplete\n'])
    extend_([u'$', u'("input[name=\'mista\'],input[name=\'mihin\']").typeahead({source: paikat});\n'])
    extend_([u'}\n'])
    extend_([u'</script>\n'])
    extend_([u'<script src="/static/js/d3.v3.min.js"></script>\n'])
    extend_([u'<script src="/static/js/visualisaatio.js"></script>\n'])

    return self

results = CompiledTemplate(results, 'templates/results.html')
join_ = results._join; escape_ = results._escape

# coding: utf-8
def results_debug (matkat, params, t):
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
                extend_([u'Hinta: ', escape_(matkat["auto"]["hinta"], True), u'<br>\n'])
                extend_([u'Polttoaineen hinta: ', escape_(matkat["auto"]["polttoaineen_hinta"], True), u'\n'])
            extend_([u'<br>\n'])
            extend_([u'\n'])
    extend_([u'<a href="/">Takaisin</a>\n'])

    return self

results_debug = CompiledTemplate(results_debug, 'templates/results_debug.html')
join_ = results_debug._join; escape_ = results_debug._escape

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
    extend_([u'  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap-responsive.min.css">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/style.css">\n'])
    extend_([u'  <link href="http://fonts.googleapis.com/css?family=Days+One|Racing+Sans+One|Monda&subset=latin,latin-ext" rel="stylesheet" type="text/css">\n'])
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

