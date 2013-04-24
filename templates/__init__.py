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
    extend_([u'  <meta charset="utf-8">\n'])
    extend_([u'  <title>Joukkoliikenteen hintavertailu - prototyyppi</title>\n'])
    extend_([u'  <meta name="description" content="description t\xe4h\xe4n">\n'])
    extend_([u'  <meta name="keywords" content="keywordsit t\xe4h\xe4n">\n'])
    extend_([u'  <meta name="author" content="authorit t\xe4h\xe4n">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap.min.css">\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/style.css">\n'])
    extend_([u'  <!-- <link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.10.2/themes/smoothness/jquery-ui.css"> -->\n'])
    extend_([u'  <link rel="stylesheet" type="text/css" href="/static/css/bootstrap-responsive.min.css">\n'])
    extend_([u'</head>\n'])
    extend_([u'<body>\n'])
    extend_([u'\n'])
    extend_([u'  ', escape_(content, False), u'\n'])
    extend_([u'\n'])
    extend_([u'<!-- <script src="/static/js/jquery.js"></script> -->\n'])
    extend_([u'<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>\n'])
    extend_([u'<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js"></script>\n'])
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
    extend_([u'<!-- <div class="row">\n'])
    extend_([u'<div class"span4 offset4">\n'])
    extend_([u' -->\n'])
    extend_([u'<div class="hero-unit">\n'])
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
    extend_([u'<!-- </div>\n'])
    extend_([u'</div>-->\n'])
    extend_([u'</div> <!-- /.hero-unit -->\n'])
    extend_([u'</div> <!-- /.container -->\n'])
    extend_([u'\n'])
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
    extend_([u'  ', u'$', u'("#inputTyyppi").val("saapumisaika"); // asetetaan oletusarvo\n'])
    extend_([u'\n'])
    extend_([u'  // Datepicker\n'])
    extend_([u'  var dpSettings = {\n'])
    extend_([u'    dateFormat: "dd.mm.yy",\n'])
    extend_([u'    dayNamesMin: ["Ma","Ti","Ke","To","Pe","La","Su"],\n'])
    extend_([u'    monthNames: ["Tammi","Helmi","Maalis","Huhti","Touko","Kes\xe4", "Hein\xe4","Elo","Syys","Loka","Marras","Joulu"],\n'])
    extend_([u'    defaultDate: null\n'])
    extend_([u'  };\n'])
    extend_([u'  ', u'$', u'("#inputPvm").datepicker(dpSettings);\n'])
    extend_([u'  // dpSettings["altField"] = "#inputTestiaika";\n'])
    extend_([u'  // ', u'$', u'("#testiaika").datepicker(dpSettings);\n'])
    extend_([u'\n'])
    extend_([u'  // Autocomplete\n'])
    extend_([u"  var vrAsemat = ['Alavus','Dragsvik','El\xe4inpuisto - Zoo','Eno','Enonteki\xf6','Espoo','Haapaj\xe4rvi','Haapam\xe4ki','Haarajoki','Hankasalmi','Hanko','Hanko-Pohjoinen','Harjavalta','Haukivuori','Hein\xe4vesi','Helsinki','Helsinki airport','Herrala','Hiekkaharju','Hiki\xe4','Humppila','Huopalahti','Hyvink\xe4\xe4','H\xe4meenlinna','H\xf6lj\xe4kk\xe4','Iisalmi','Iittala','Ilmala','Imatra','Inari','Inkeroinen','Inkoo','Isokyr\xf6','Ivalo','Joensuu','Jokela','Joroinen','Jorvas','Joutseno','Juupajoki','Jyv\xe4skyl\xe4','J\xe4ms\xe4','J\xe4rvel\xe4','J\xe4rvenp\xe4\xe4','Kajaani','Kannelm\xe4ki','Kannus','Karjaa','Karkku','Kauhava','Kauklahti','Kauniainen','Kausala','Kemi','Kemij\xe4rvi','Kemij\xe4rvi bus station','Kera','Kerava','Kerim\xe4ki','Kes\xe4lahti','Keuruu','Kiilop\xe4\xe4','Kilo','Kilpisj\xe4rvi','Kirkkonummi','Kitee','Kittil\xe4','Kiuruvesi','Kohtavaara','Koivuhovi','Koivukyl\xe4','Kokem\xe4ki','Kokkola','Kolari','Kolho','Kontiom\xe4ki','Koria','Korso','Kotka','Kotkan Satama','Kouvola','Kuhmo','Kuopio','Kupittaa','Kuusamo','Kyl\xe4nlahti','Kymi','Kyminlinna','Kyr\xf6l\xe4','K\xe4pyl\xe4','Lahti','Laihia','Lapinlahti','Lappeenranta','Lappila','Lappohja','Lapua','Lemp\xe4\xe4l\xe4','Lepp\xe4vaara','Levi','Lieksa','Lievestuore','Lohja bus station','Loimaa','Louhela','Loviisa bus station','Luoma','Luosto','Lusto','Malmi','Malminkartano','Mankki','Martinlaakso','Masala','Mikkeli','Misi','Mommila','Moscow (Leningradski)','Muhos','Muijala','Muonio','Muurola','Myllykoski','Myllym\xe4ki','Myyrm\xe4ki','M\xe4kkyl\xe4','M\xe4nts\xe4l\xe4','M\xe4ntyharju','Nastola','Nivala','Nokia','Nummela','Nuppulinna','Nurmes','Oitti','Olos','Orivesi','Orivesi Keskusta','Oulainen','Oulu','Oulunkyl\xe4','Paimenportti','Pallastunturi','Paltamo','Parikkala','Parkano','Parola','Pasila','Pello','Perttil\xe4','Pet\xe4j\xe4vesi','Pieks\xe4m\xe4ki','Pietarsaari','Pihlajavesi','Pit\xe4j\xe4nm\xe4ki','Pohjois-Haaga','Pori','Porvoo bus station','Puistola','Pukinm\xe4ki','Punkaharju','Purola','Pyh\xe4','Pyh\xe4salmi','P\xe4nn\xe4inen','P\xe4\xe4skylahti','Raahe','Rantasalmi','Rauma','Rekola','Retretti','Riihim\xe4ki','Rovaniemi','Ruka','Runni','Ruukki','Ryttyl\xe4','Saariselk\xe4','Salla','Sallatunturi','Salo','Santala','Saunakallio','Savio','Savonlinna','Savonlinna bus station','Sein\xe4joki','Siilinj\xe4rvi','Simpele','Siuntio','Skogby','Sodankyl\xe4','Sotkamo','St. Petersburg (Finljandski)','St.petersburg (Ladozhki)','Sukeva','Suomu','Suonenjoki','Tahko','Tammisaari','Tampere','Tapanila','Tavastila','Tervajoki','Tervola','Tikkurila','Toijala','Tolsa','Tornio','Tornio bus station','Tornio- It\xe4inen','Tuomarila','Turenki','Turku','Turku Satama','Tuuri','Tver','Uimaharju','Utaj\xe4rvi','Utsjoki','Uusikyl\xe4','Vaala','Vaasa','Vainikkala','Vainikkala raja','Valimo','Valtimo','Vammala','Vantaankoski','Varkaus','Veikkola','Vihanti','Vihtari','Viiala','Viinij\xe4rvi','Vill\xe4hde','Vilppula','Virkkala','Vuokatti ras th','Vuokatti urheiluopisto th','Vuonislahti','Vuontispirtti','Vyborg','Ylistaro','Ylitornio','Ylivieska','\xc4ht\xe4ri','\xc4k\xe4slompolo'];\n"])
    extend_([u'    ', u'$', u'("input[name=\'mista\'],input[name=\'mihin\']").typeahead({source: vrAsemat});\n'])
    extend_([u'}\n'])
    extend_([u'</script>\n'])

    return self

index = CompiledTemplate(index, 'templates\\index.html')
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

results = CompiledTemplate(results, 'templates\\results.html')
join_ = results._join; escape_ = results._escape

