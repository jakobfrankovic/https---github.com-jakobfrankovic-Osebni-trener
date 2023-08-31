import bottle 
import model
import sqlite3
import datetime
import hashlib


@bottle.route('/static/css/<filename:re:.*\.css>')
def send_css(filename):
    return bottle.static_file(filename, root='static/css')

@bottle.route('/static/img/<filename:re:.*\.png>')
def send_img(filename):
    return bottle.static_file(filename, root='static/img')

@bottle.route('/static/javascript/<filename:re:.*\.js>')
def send_javascript(filename):
    return bottle.static_file(filename, root='static/javascript')

@bottle.get("/login")    
@bottle.get("/")    
def get_login():                   
    return bottle.template("login.html")

@bottle.post("/login") 
@bottle.post("/") 
def add_login():
    mail = bottle.request.forms.get('mail')
    geslo = bottle.request.forms.get('geslo')
    #zašifriramo geslo
    geslo = password_md5(geslo)
    veljavnost = model.Uporabnik.preveri_mail_in_geslo(mail, geslo)
    if veljavnost:
        print("Odobren vstop")
        bottle.response.set_cookie('mail', mail, path='/')
        bottle.redirect("/home")
    else:
        print("ponovi geslo")
        bottle.redirect("/login")
        
@bottle.get("/signup")    
def get_signup():                   
    return bottle.template("signup.html")

@bottle.post("/signup") 
def add_signup():
    ime = bottle.request.forms.get('ime')
    priimek = bottle.request.forms.get('priimek')
    datum_rojstva = bottle.request.forms.get('datum_rojstva')
    teza = bottle.request.forms.get('teza')
    visina = bottle.request.forms.get('visina')
    geslo = bottle.request.forms.get('geslo')
    #geslo zašifriramo
    geslo = password_md5(geslo) 
    mail = bottle.request.forms.get('mail')
    spol = bottle.request.forms.get('spol')
    uporabnik = model.Uporabnik(mail, ime, priimek, datum_rojstva, teza, visina, geslo, spol)
    uporabnik.shrani_v_bazo()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    dnevnik = model.Dnevni_vnos(date, mail)
    dnevnik.dodaj_v_dnevni_vnos()

    bottle.redirect("/login")

 
def password_md5(s):
    """
    MD5 hash funkcija za geslo
    """
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


def get_user():
    """
    Vrne uporabnikov mail.
    """
    uporabnik_mail = bottle.request.get_cookie('mail')
    if uporabnik_mail is not None:
        return uporabnik_mail
    else:
        return None

@bottle.get("/home")    
def get_home():
    uporabnik = model.Uporabnik(mail=bottle.request.get_cookie('mail'))
    vitamin_totals = uporabnik.get_vitamin_totals()
    mineral_totals = uporabnik.get_mineral_totals()
    other_totals = uporabnik.get_other_totals()
    feel = uporabnik.get_feeling_avg()
    activity = uporabnik.get_all_activity()
    burned_calories = uporabnik.get_sum_of_exercise()
    return bottle.template("home.html", vitamin_totals=vitamin_totals, mineral_totals=mineral_totals, other_totals=other_totals, feel = feel, activity = activity, burned_calories=burned_calories)

@bottle.get("/food")    
def get_food():   
    ime_hrane = model.Zivilo.dobi_imena_vseh_zivil()  
    uporabnik_mail = bottle.request.get_cookie('mail')              
    return bottle.template("food.html", hrana = ime_hrane)

@bottle.post("/food")
def add_food():
    ime_zivila = bottle.request.forms.getall('hrana')
    cas_obroka = bottle.request.forms.get('cas_obroka')
    vrsta_obroka = bottle.request.forms.get("vrsta_obroka")
    obrok = model.Obrok(vrsta_obroka, cas_obroka)
    obrok.dodaj(bottle.request.get_cookie('mail'))
    ime = ime_zivila[1::2] 
    kolicina = ime_zivila[2::2]
    for i, k in zip(ime, kolicina):
        if obrok.preveri_zivilo(i) != None:
            obrok.dodaj_zivilo(i, k)
    bottle.redirect("/food")

@bottle.get("/activity")  
def get_activity():
    ime_aktivnosti = model.Aktivnost.dobi_imena_vseh_aktivnosti()                
    return bottle.template("activity.html", aktivnost = ime_aktivnosti)


@bottle.post("/activity")  
def add_activity():
    ime_aktivnosti = bottle.request.forms.get("ime_aktivnost")
    cas_aktivnosti = bottle.request.forms.get("cas_aktivnosti")
    trajanje_aktivnosti = bottle.request.forms.get("trajanje")
    rekreacija = model.Rekreacija(ime_aktivnosti, cas_aktivnosti, trajanje_aktivnosti)
    mail = get_user()
    id_dnevnika = model.Dnevni_vnos.return_dnevnik(mail)
    rekreacija.dodaj_aktivnost(id_dnevnika)
    bottle.redirect("/activity")

    #Tukaj napiši katere podatke rabiš za bazo

@bottle.get("/feeling")  
def get_feeling():               
    return bottle.template("feeling.html")


@bottle.post("/feeling")  
def add_feeling():
    ocena = bottle.request.forms.get("ocena")
    mail = get_user()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    id_dnevnika = model.Dnevni_vnos.return_dnevnik(mail)
    pocutje = model.Pocutje(ocena, id_dnevnika)
    pocutje.shrani_v_bazo()
    bottle.redirect("/feeling")

@bottle.get('/logout')
def logout():
    bottle.response.delete_cookie('mail')
    bottle.redirect('/')
    
@bottle.get("/vitamins")       
def get_vitamins():     
    uporabnik = model.Uporabnik(mail=bottle.request.get_cookie('mail'))  
    data = uporabnik.get_vitamins()
    return bottle.template("vitamins.html", data=data)

@bottle.get("/minerals")      
def get_minerals():     
    uporabnik = model.Uporabnik(mail=bottle.request.get_cookie('mail'))  
    data = uporabnik.get_minerals()           
    return bottle.template("minerals.html", data=data, mineral=None)

@bottle.get("/info")      
def get_info_vse_aktivnosti():   
    cas_telovadbe1 = model.Aktivnost.cas_vsa_rekreacija(get_user())
    cas_telovadbe2 = model.Aktivnost.cas_posamezne_rekreacija(get_user())
    povp_pocutje = model.Pocutje.povprečje_počutja(get_user())
    if len(cas_telovadbe1) == 0:
        cas_telovadbe1 = [('vpišite podatke pod akti', 'vpišite podatke pod Aktivnost')]
        cas_telovadbe2 = [('vpišite podatke pod Aktivnost', 'vpišite podatke pod Aktivnost')]
        povp_pocutje = [(0.0, 0)]
    
    return bottle.template("info.html", data = [cas_telovadbe1, cas_telovadbe2, povp_pocutje])


def run_bottle():
    bottle.run(debug=True, reloader=False)


