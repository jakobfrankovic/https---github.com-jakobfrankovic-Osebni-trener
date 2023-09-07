import model
import hashlib
import datetime

def password_md5(s):
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

def login():
    mail = input("Vnesite e-pošto: ")
    geslo = input("Vnesite geslo: ")
    geslo = password_md5(geslo)
    veljavnost = model.Uporabnik.preveri_mail_in_geslo(mail, geslo)
    
    if veljavnost:
        print("Odobren vstop")
        return mail
    else:
        print("Napačna e-pošta ali geslo. Poskusite znova.")
        return None

def signup():
    try:
        ime = input("Vnesite ime: ")
        priimek = input("Vnesite priimek: ")
        datum_rojstva = float(input("Vnesite datum rojstva (YYYY-MM-DD): "))
        teza = float(input("Vnesite težo: "))
        visina = float(input("Vnesite višino: "))
        geslo = input("Vnesite geslo: ")
        geslo = password_md5(geslo)
        mail = input("Vnesite e-pošto: ")
        spol = input("Vnesite spol (M/Ž): ").upper()
        if spol not in ['M', 'Ž']:
            print("Napačen vnos spola. Poskusite znova.")
            return None

        uporabnik = model.Uporabnik(mail, ime, priimek, datum_rojstva, teza, visina, geslo, spol)
        uporabnik.shrani_v_bazo()

        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        dnevnik = model.Dnevni_vnos(date, mail)
        dnevnik.dodaj_v_dnevni_vnos()

        print("Uspešno ste se registrirali!")
        return mail
    except:
        print("Napačen vnos. Poskusite znova")

def add_food(user_mail):
    zivila = model.Zivilo.dobi_imena_vseh_zivil()
    slovar = {}
    for i, zivilo in enumerate(zivila, 1):
        print(f"{i}. {zivilo[0]}")
        slovar[i] = zivilo[0]

    try:
        ime_zivila = int(input("Vnesite številko živila: "))
        kolicina = int(input("Vnesite količino v gramih: "))
        cas_obroka = input("Vnesite čas obroka (YYYY-MM-DD HH:MM:SS): ")
        vrsta_obroka = input("Vnesite vrsto obroka (zajtrk/kosilo/večerja): ")

        obrok = model.Obrok(vrsta_obroka, cas_obroka)
        obrok.dodaj(user_mail)

        obrok.dodaj_zivilo(slovar[ime_zivila], kolicina)
        print("Živilo dodano!")
    except:
        print('Napaka pri vnosu. Poskusite znova.')

def add_activity(user_mail):
    aktivnosti = model.Aktivnost.dobi_imena_vseh_aktivnosti()
    aktivnosti_dict = {}
    
    print("Izberite aktivnost:")
    for i, aktivnost in enumerate(aktivnosti, 1):
        print(f"{i}. {aktivnost[0]}")
        aktivnosti_dict[i] = aktivnost[0]
        
    try:
        izbira_aktivnosti = int(input("Vnesite številko aktivnosti: "))
        if izbira_aktivnosti not in aktivnosti_dict:
            print("Napačna izbira. Poskusite znova.")
            return
    except ValueError:
        print("Vnesite veljavno številko.")
        return
    
    čas_aktivnosti = input("Vnesite čas aktivnosti (YYYY-MM-DD HH:MM:SS): ")
    trajanje_aktivnosti = input("Vnesite trajanje aktivnosti (v minutah): ")
    
    
    rekreacija = model.Rekreacija(aktivnosti_dict[izbira_aktivnosti], čas_aktivnosti, trajanje_aktivnosti)
    id_dnevnika = model.Dnevni_vnos.return_dnevnik(user_mail)
    rekreacija.dodaj_aktivnost(id_dnevnika)
    print("Aktivnost dodana!")

def pregled(user_mail):
    try:
        uporabnik_prikaz = model.Uporabnik(user_mail)
        print("1: Čas posamezne rekreacije")
        print("2: Skupni čas rekreacije")
        print("3: Prikaz zaužitih vitaminov")
        print("4: Prikaz zaužitih mineralov")
        print("5: Prikaz povprečnega počutja")
        izbira = int(input("Vnesi številko izbire"))
        if izbira == 1:
            print(model.Aktivnost.cas_posamezne_rekreacija(user_mail))
        elif izbira == 2:    
            print(model.Aktivnost.cas_vsa_rekreacija(user_mail))
        elif izbira == 3:
            slovar_vitaminov = uporabnik_prikaz.get_vitamin_totals()
            print("Vitamin Data:")
            print("=" * 40)
            for vitamin, data in slovar_vitaminov.items():
                print(f"{vitamin}:")
                print(f"  - Skupaj: {data['total']}")
                print(f"  - PDV: {data['pdv']}")
                print("-" * 40)
        elif izbira == 4:
            slovar_mineralov = uporabnik_prikaz.get_mineral_totals()
            print("Mineral Data:")
            print("=" * 40)
            for mineral, data in slovar_mineralov.items():
                print(f"{mineral}:")
                print(f"  - Skupaj: {data['total']}")
                print(f"  - PDV: {data['pdv']}")
                print("-" * 40)
        elif izbira == 5:
            print(uporabnik_prikaz.get_feeling_avg())

    except:
        print("Vnos ni veljaven. Poskusite znova.")

def add_feeling(user_mail):
    try:
        ocena = int(input("Oceni svoje počutje od 1 do 10:"))
        id_dnevnika = model.Dnevni_vnos.return_dnevnik(user_mail)
        pocutje = model.Pocutje(ocena, id_dnevnika)
        pocutje.shrani_v_bazo()
    except:
        print("Vnos ni veljaven. Poskusite znova")

def main():
    user_mail = None
    
    while True:
        print("\n--- Meni ---")
        print("1: Prijava")
        print("2: Registracija")
        print("3: Dodaj hrano")
        print("4: Dodaj aktivnost")
        print("5: Oceni svoje počutje")
        print("6: Pregled podatkov")
        
        izbira = input("\nIzberite možnost: ")
        
        if izbira == "1":
            user_mail = login()
        
        elif izbira == "2":
            user_mail = signup()
        
        elif izbira == "3":
            if user_mail:
                add_food(user_mail)
            else:
                print("Najprej se prijavite ali registrirajte.")
        
        elif izbira == "4":
            if user_mail:
                add_activity(user_mail)
            else:
                print("Najprej se prijavite ali registrirajte.")

        elif izbira == '5':
            if user_mail:
                add_feeling(user_mail)
            else:
                print("Najprej se prijavite ali registrirajte.")
        elif izbira == "6":
            if user_mail:
                pregled(user_mail)
            else:
                print("Najprej se prijavite ali registrirajte.")

main()