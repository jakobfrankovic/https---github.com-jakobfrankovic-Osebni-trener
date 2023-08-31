import sqlite3
import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}\b'

conn = sqlite3.connect("osebni_trener.db")
# Nastavimo, da sledi tujim ključem
conn.execute("PRAGMA foreign_keys = ON")

class Uporabnik:
    def __init__(self, mail, ime = None, priimek = None, datum_rojstva = None, teza = None, visina = None, geslo = None, spol= None):
        #self.id_uporabnika = stevilo_uporabnikov("osebni_trener.sqlite3") + 1
        self.ime = ime
        self.priimek = priimek
        self.datum_rojstva = datum_rojstva
        self.teza = teza
        self.geslo = geslo
        self.mail = mail
        self.spol = spol
        self.visina = visina
    def email_je_ze_v_uporabi(self):
        '''Preverimo ali je mail že v uporabi'''
        with conn:
            cursor = conn.execute("SELECT 1 FROM uporabnik WHERE mail = ?", [self.mail])
            return bool(cursor.fetchone())

    def get_feeling_avg(self):
        with conn:
            query = """
            SELECT avg(ocena) FROM Pocutje
                JOIN Dnevni_vnos ON Dnevni_vnos.id_dnevnika = Pocutje.id_dnevni_vnos
                JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                WHERE Uporabnik.mail = ?;
            """
            cursor = conn.execute(query, [self.mail])               
            return cursor.fetchone()[0]

    def get_all_activity(self):
        with conn:
            query = """
            SELECT id_aktivnost FROM Rekreacija
                JOIN Dnevni_vnos ON Dnevni_vnos.id_dnevnika = Rekreacija.id_dnevni_vnos
                JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                WHERE Uporabnik.mail = ?;
            """
            cursor = conn.execute(query, [self.mail])               
            return cursor.fetchall()
        
    def get_all(self):
        '''Get all minerals for particular user by food eaten'''
        with conn:
            query = """
            SELECT name, kolicina, fiber_g, sodium_mg, iron_mg, potassium_mg, magnesium_mg, zink_mg FROM Zivilo
                  JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                  JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                  JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                  JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                  WHERE Uporabnik.mail = ?;
            """
            cursor = conn.execute(query, [self.mail])               
            return cursor.fetchall()


    def get_vitamins(self):
        '''Get all vitamins for particular user by food eaten'''
        with conn:
            query = """
            SELECT name, kolicina, vitamin_a_IU, vitamin_b12_mcg, vitamin_b6_mg, vitamin_c_mg, vitamin_d_IU, vitamin_e_mg, vitamin_k_mcg  FROM Zivilo
                  JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                  JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                  JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                  JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                  WHERE Uporabnik.mail = ?;
            """
            cursor = conn.execute(query, [self.mail])               
            return cursor.fetchall()
    def get_minerals_sorted(self, name):
        '''Get all minerals for particular user by food eaten'''
        with conn:
            query = """
            SELECT name, kolicina, fiber_g, sodium_mg, iron_mg, potassium_mg, magnesium_mg, zink_mg FROM Zivilo
                  JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                  JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                  JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                  JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                  WHERE Uporabnik.mail = ?
                  ORDER BY ? DESC;
            """
            cursor = conn.execute(query, [self.mail, name])               
            return cursor.fetchall()

    def get_minerals(self):
        '''Get all minerals for particular user by food eaten'''
        with conn:
            query = """
            SELECT name, kolicina, fiber_g, sodium_mg, iron_mg, potassium_mg, magnesium_mg, zink_mg FROM Zivilo
                  JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                  JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                  JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                  JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                  WHERE Uporabnik.mail = ?;
            """
            cursor = conn.execute(query, [self.mail])               
            return cursor.fetchall()

    def get_vitamin_totals(self):
        sum_exercise = self.get_sum_of_exercise()
        with conn:
            expected_vitamins = {
                "vitamin_a_IU": self.get_expected("vitamin_a_IU", sum_exercise),
                "vitamin_b12_mcg": self.get_expected("vitamin_b12_mcg", sum_exercise),
                "vitamin_b6_mg": self.get_expected("vitamin_b6_mg", sum_exercise),
                "vitamin_c_mg": self.get_expected("vitamin_c_mg", sum_exercise),
                "vitamin_d_IU": self.get_expected("vitamin_d_IU", sum_exercise),
                "vitamin_e_mg": self.get_expected("vitamin_e_mg", sum_exercise),
                "vitamin_k_mcg": self.get_expected("vitamin_k_mcg", sum_exercise)
            }
            vitamin_to_total = {}
            vitamins = [
                "vitamin_a_IU",
                "vitamin_b12_mcg",
                "vitamin_b6_mg",
                "vitamin_c_mg",
                "vitamin_d_IU",
                "vitamin_e_mg",
                "vitamin_k_mcg"
            ]
            for vitamin in vitamins:
                query = """
                SELECT COALESCE(SUM(Zivilo.{} * ZiviloObrok.kolicina / 100 ), 0) FROM Zivilo
                  JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                  JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                  JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                  JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                  WHERE Uporabnik.mail = ?;
                """.format(vitamin)
                cursor = conn.execute(query, [self.mail])
                vitamin_to_total[vitamin] = {
                    "total": cursor.fetchone()[0],
                    "pdv": expected_vitamins[vitamin]
                }

            return vitamin_to_total

    def get_mineral_totals(self):
        sum_exercise = self.get_sum_of_exercise()
        with conn:
            expected_minerals = {
                "magnesium_mg": self.get_expected("magnesium_mg", sum_exercise),
                "calcium_mg": self.get_expected("calcium_mg", sum_exercise),
                "sodium_mg": self.get_expected("sodium_mg", sum_exercise),
                "iron_mg": self.get_expected("iron_mg", sum_exercise),
                "potassium_mg": self.get_expected("potassium_mg", sum_exercise),
                "zink_mg": self.get_expected("zink_mg", sum_exercise),
            }
            mineral_to_total = {}
            minerals = [
                "magnesium_mg",
                "calcium_mg",
                "sodium_mg",
                "iron_mg",
                "potassium_mg",
                "zink_mg",
            ]
            for mineral in minerals:
                query = """
                SELECT COALESCE(SUM(Zivilo.{} * ZiviloObrok.kolicina / 100), 0) FROM Zivilo
                  JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                  JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                  JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                  JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                  WHERE Uporabnik.mail = ?;
                """.format(mineral)
                cursor = conn.execute(query, [self.mail])
                mineral_to_total[mineral] = {
                    "total": cursor.fetchone()[0],
                    "pdv": expected_minerals[mineral]
                }

            return mineral_to_total
    
    def get_sum_of_exercise(self):
        with conn:
            cursor = conn.execute("""
                    SELECT IFNULL(COALESCE(SUM(Uporabnik.teza * Rekreacija.cas_vadbe_min * Aktivnost.poraba_kalorij_na_kg / 60), 0), 0) FROM Uporabnik
                    JOIN Dnevni_vnos ON Dnevni_vnos.mail = Uporabnik.mail
                    JOIN Rekreacija ON Rekreacija.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                    JOIN Aktivnost ON Aktivnost.id_aktivnost = Rekreacija.id_aktivnost
                    WHERE Uporabnik.mail = ?;
                    """, [self.mail])
            return cursor.fetchone()[0]
        return 0


    def get_expected(self, name, sum_exercise):
        #(kilogrami * čas_aktivnosti * aktivnost  / 60) / kalorije * začetna_vrednost
        #Aktivnost, kilograme, začetno vrednost, vrednost za vsako hranilo posebej
        expected_normal = {
                "fiber_g": 35,
                "carbohydrate_g": 300,
                "protein_g": 56,
                "calories": 2000,
                "magnesium_mg": 400,
                "calcium_mg": 1000,
                "sodium_mg": 500,
                "iron_mg": 8.7,
                "potassium_mg": 2000,
                "zink_mg": 11,
                "vitamin_a_IU": 3000,
                "vitamin_b12_mcg": 2.4,
                "vitamin_b6_mg": 1.7,
                "vitamin_c_mg": 90,
                "vitamin_d_IU": 600,
                "vitamin_e_mg": 15,
                "vitamin_k_mcg": 120
            }
        return expected_normal[name] + sum_exercise / 2000 * expected_normal[name]

    def get_other_totals(self):
        sum_exercise = self.get_sum_of_exercise()
        with conn:
            expected = {
                "fiber_g": self.get_expected("fiber_g", sum_exercise),
                "carbohydrate_g": self.get_expected("carbohydrate_g", sum_exercise),
                "protein_g": self.get_expected("protein_g", sum_exercise),
                "calories": self.get_expected("calories", sum_exercise)
            }
            other_to_total = {}
            others = [
                "fiber_g",
                "carbohydrate_g",
                "protein_g",
                "calories"
            ]
            for other in others:
                query = """
                SELECT COALESCE(SUM(Zivilo.{} * ZiviloObrok.kolicina / 100), 0) FROM Zivilo
                JOIN ZiviloObrok ON ZiviloObrok.ime_zivila = Zivilo.name
                JOIN Obrok ON ZiviloObrok.id_obroka = Obrok.id_obroka
                JOIN Dnevni_vnos ON Obrok.id_dnevni_vnos = Dnevni_vnos.id_dnevnika
                JOIN Uporabnik ON Dnevni_vnos.mail = uporabnik.mail
                WHERE Uporabnik.mail = ?;
                """.format(other)
                cursor = conn.execute(query, [self.mail])
                other_to_total[other] = {
                    "total": cursor.fetchone()[0],
                    "pdv": expected[other]
                }

            return other_to_total
    

    def shrani_v_bazo(self):
        print(self.ime, self.priimek, self.datum_rojstva, self.teza, self.visina, self.geslo, self.mail, self.spol)
        if not self.email_je_ze_v_uporabi():
            with conn:
                conn.execute("""
                INSERT INTO Uporabnik(mail, ime, priimek, datum_rojstva, teza, visina, geslo, spol) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)           
            """, [self.mail, self.ime, self.priimek, self.datum_rojstva, self.teza, self.visina, self.geslo, self.spol])
        else:
            print("Email naslov je že v uporabi.")

    @staticmethod
    def preveri_mail_in_geslo(mail, geslo):
        if mail != None and check(mail):
            with conn:
                cursor = conn.execute("""
                    SELECT geslo
                    FROM uporabnik
                    WHERE mail=?
                """, [mail])
                preveri = cursor.fetchone()
            if preveri == None:
                return False
            return preveri[0] == geslo
        return False
            
def check(mail):
    return re.fullmatch(regex, mail)

class Dnevni_vnos:
    def __init__(self, datum, uporabnik):
        self.datum = datum
        self.uporabnik = uporabnik

    def dodaj_v_dnevni_vnos(self):
        with conn:
            cursor2 = conn.execute("""
            INSERT INTO Dnevni_vnos (datum, mail)
            VALUES (?, ?)                 
            """, [self.datum, self.uporabnik])
    @staticmethod
    def return_dnevnik(mail):
        with conn:
            cursor = conn.execute("SELECT id_dnevnika FROM Dnevni_vnos WHERE mail = ?", [mail])
            podatki = cursor.fetchone()
            return podatki[0]


class Teza:
    def __init__(self, id_teza, tehtanje):
        self.id_teza = id_teza
        self.tehtanje = tehtanje
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Teza (tehtanje)
            VALUES (?)                 
            """, [self.tehtanje])
            self.uid = cursor.lastrowid
class Pocutje:
    def __init__(self, ocena, id_dnevnika):
        self.ocena = ocena
        self.id_dnevnika = id_dnevnika
    def shrani_v_bazo(self):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Pocutje (id_dnevni_vnos, ocena)
            VALUES (?, ?)                 
            """, [self.id_dnevnika, self.ocena])
            self.uid = cursor.lastrowid
    @staticmethod
    def povprečje_počutja(mail):
        '''Vrne čas vse aktivnosti'''
        with conn:
            query = """
            SELECT AVG(ocena) FROM Pocutje JOIN Dnevni_vnos ON Dnevni_vnos.id_dnevnika = Pocutje.id_dnevni_vnos
            WHERE mail = ?;
            """
            cursor = conn.execute(query, [mail])

            return cursor.fetchall()

class Rekreacija:
    def __init__(self, id_aktivnosti, cas_vadbe, trajanje_vadbe_min):
        self.id_aktivnosti = id_aktivnosti
        self.cas_vadbe = cas_vadbe
        self.trajanje_vadbe_min = trajanje_vadbe_min

    def dodaj_aktivnost(self, id_dnevnika):
        with conn:
            cursor = conn.execute("SELECT id_aktivnost FROM Aktivnost WHERE id_aktivnost = ?", [self.id_aktivnosti])
            result = cursor.fetchone()
            if result != None:
                cursor = conn.execute("""
                INSERT INTO Rekreacija (cas_izvedbe, cas_vadbe_min, id_aktivnost, id_dnevni_vnos) 
                VALUES (?, ?, ?, ?)                 
                """, [self.cas_vadbe , self.trajanje_vadbe_min, self.id_aktivnosti, id_dnevnika])
            #self.uid = cursor.lastrowid


class Aktivnost:
    def __init__(self, id_aktivnosti):
        self.id_aktivnosti = id_aktivnosti
    @staticmethod
    def dobi_imena_vseh_aktivnosti():
        with conn:
            cursor = conn.execute("""
                SELECT id_aktivnost
                FROM Aktivnost
            """)
            podatki = list(cursor.fetchall())
            return podatki
        return []
    
    @staticmethod
    def cas_vsa_rekreacija(mail):
        '''Vrne čas vse rekreacije'''
        with conn:
            query = """
            SELECT datum, SUM(cas_vadbe_min) FROM Rekreacija 
            JOIN Dnevni_vnos ON Dnevni_vnos.id_dnevnika = Rekreacija.id_dnevni_vnos WHERE mail = ?
            GROUP BY id_dnevni_vnos;
            """
            cursor = conn.execute(query, [mail])

            return cursor.fetchall()
    @staticmethod
    def cas_posamezne_rekreacija(mail):
        query = """
            SELECT id_aktivnost, sum(cas_vadbe_min) FROM Rekreacija JOIN Dnevni_vnos ON Dnevni_vnos.id_dnevnika = Rekreacija.id_dnevni_vnos WHERE mail = ?
            GROUP BY id_aktivnost;
            """
        cursor = conn.execute(query, [mail])
        return cursor.fetchall()
    
    
class Zivilo:
    def __init__(self, id_zivilo = None, ime_zivilo = None):
        self.id_zivilo = id_zivilo
        self.ime_zivilo = ime_zivilo

    @staticmethod
    def dobi_imena_vseh_zivil():
        with conn:
            cursor = conn.execute("""
                SELECT name 
                FROM Zivilo
            """)
            podatki = list(cursor.fetchall())
            return podatki
        return []

class Obrok:
    def __init__(self, ime_obroka, cas_obroka, id_obroka=None, zivilo = []):
        self.id_obroka = id_obroka
        self.ime_obroka = ime_obroka
        self.kolicina = 0
        self.cas_obroka = cas_obroka
        self.zivilo = zivilo # zivilo je tabela, ki vsebuje id (oziroma ime zivila) in njegovo količino

    def dodaj(self, mail):
        with conn:
            cursor = conn.execute("""
            INSERT INTO Obrok (cas_obroka, ime_obroka, id_dnevni_vnos)
            VALUES (?, ?, (SELECT id_dnevnika FROM (
                    SELECT id_dnevnika
                    FROM Dnevni_vnos
                    WHERE mail = ?
                    ORDER BY datum DESC
                    LIMIT 1
                )));
            """, [self.cas_obroka, self.ime_obroka, mail])
            self.id_obroka = cursor.lastrowid #for znak in ime_zivila:

    def dodaj_zivilo(self, ime_zivila, kolicina):
        """doda zivilo v ZiviloObrok"""
        with conn:
            cursor = conn.execute("""
            INSERT INTO ZiviloObrok (ime_zivila, id_obroka, kolicina)
            VALUES (?, ?, ?)                 
            """, [ime_zivila, self.id_obroka, kolicina])
            self.uid = cursor.lastrowid #for znak in ime_zivila:


    def preveri_zivilo(self, ime_zivila):
        with conn:
            cursor = conn.execute("""
            SELECT Name FROM Zivilo WHERE Name = ?                 
            """, [ime_zivila])
            return cursor
        
