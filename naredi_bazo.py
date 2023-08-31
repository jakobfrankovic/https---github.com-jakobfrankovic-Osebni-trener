import sqlite3
import pandas as pd



def pripravi_bazo(): 
    db = sqlite3.connect("osebni_trener.db")
    hranila = []
    df1 = pd.read_csv(r'data/modified.csv')
    for col in df1.columns:
        hranila.append(col) #hranila vsebuje imena stolpcev, dolzina je 77
    with db as cursor:
        # Uporabnik (#1)
        cursor.execute(""" CREATE TABLE IF NOT EXISTS Uporabnik
            (
                mail TEXT INTEGER PRIMARY KEY,
                ime TEXT,
                priimek TEXT,
                datum_rojstva DATE NOT NULL,
                visina INTEGER NOT NULL,
                teza INTEGER NOT NULL,
                geslo VARCHAR(255) NOT NULL,
                spol SMALLINT NOT NULL
            );""")
        # Dnevni vnos (#2)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Dnevni_vnos
            (
                id_dnevnika INTEGER PRIMARY KEY AUTOINCREMENT,
                datum DATE NOT NULL,
                mail TEXT NOT NULL,
                FOREIGN KEY (mail) REFERENCES Uporabnik(mail)
            );""")

        # Pocutje (#3)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Pocutje
            (
                id_pocutja INTEGER PRIMARY KEY AUTOINCREMENT,
                id_dnevni_vnos INTEGER,
                ocena INTEGER NOT NULL,
                FOREIGN KEY (id_dnevni_vnos) REFERENCES Dnevni_vnos(id_dnevnika) 
            );""")
        # Rekreacija (#4)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Rekreacija
            (
                id_rekreacije INTEGER PRIMARY KEY AUTOINCREMENT,
                cas_izvedbe TIME NOT NULL,
                cas_vadbe_min INTEGER NOT NULL,
                id_aktivnost TEXT NOT NULL,
                id_dnevni_vnos INTEGER,
                FOREIGN KEY (id_dnevni_vnos) REFERENCES Dnevni_vnos(id_dnevnika) 
                FOREIGN KEY (id_aktivnost) REFERENCES Aktivnost(id_aktivnost)
            );""")

        # Aktivnost (#5) #ali je tukaj autoincrement ?? #Mogoče namesto id aktivnosti kar ime kot primary key?
        cursor.execute("""CREATE TABLE IF NOT EXISTS Aktivnost
            (
                id_aktivnost TEXT PRIMARY KEY,
                poraba_kalorij_na_kg DECIMAL NOT NULL
            );""")

        # Obrok (#6)
        cursor.execute("""CREATE TABLE IF NOT EXISTS Obrok
            (
                id_obroka INTEGER PRIMARY KEY AUTOINCREMENT,
                ime_obroka TEXT NOT NULL,
                cas_obroka TIME NOT NULL,
                id_dnevni_vnos INTEGER,
                FOREIGN KEY (id_dnevni_vnos) REFERENCES Dnevni_vnos(id_dnevnika)
            );""")

        # Zivilo (#7)
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Zivilo
            (   {hranila[0]}  TEXT PRIMARY KEY NOT NULL,
                {hranila[1]}  TEXT NOT NULL,
                {hranila[2]}  TEXT NOT NULL,
                {hranila[3]}  TEXT NOT NULL,
                {hranila[4]}  TEXT NOT NULL,
                {hranila[5]}  TEXT NOT NULL,
                {hranila[6]}  TEXT NOT NULL,
                {hranila[7]}  TEXT NOT NULL,
                {hranila[8]}  TEXT NOT NULL,
                {hranila[9]}  TEXT NOT NULL,
                {hranila[10]} TEXT NOT NULL,
                {hranila[11]} TEXT NOT NULL,
                {hranila[12]} TEXT NOT NULL,
                {hranila[13]} TEXT NOT NULL,
                {hranila[14]} TEXT NOT NULL,
                {hranila[15]} TEXT NOT NULL,
                {hranila[16]} TEXT NOT NULL,
                {hranila[17]} TEXT NOT NULL,
                {hranila[18]} TEXT NOT NULL,
                {hranila[19]} TEXT NOT NULL,
                {hranila[20]} TEXT NOT NULL,
                {hranila[21]} TEXT NOT NULL,
                {hranila[22]} TEXT NOT NULL,
                {hranila[23]} TEXT NOT NULL,
                {hranila[24]} TEXT NOT NULL,
                {hranila[25]} TEXT NOT NULL,
                {hranila[26]} TEXT NOT NULL,
                {hranila[27]} TEXT NOT NULL,
                {hranila[28]} TEXT NOT NULL,
                {hranila[29]} TEXT NOT NULL,
                {hranila[30]} TEXT NOT NULL,
                {hranila[31]} TEXT NOT NULL,
                {hranila[32]} TEXT NOT NULL,
                {hranila[33]} TEXT NOT NULL,
                {hranila[34]} TEXT NOT NULL,
                {hranila[35]} TEXT NOT NULL,
                {hranila[36]} TEXT NOT NULL,
                {hranila[37]} TEXT NOT NULL,
                {hranila[38]} TEXT NOT NULL,
                {hranila[39]} TEXT NOT NULL,
                {hranila[40]} TEXT NOT NULL,
                {hranila[41]} TEXT NOT NULL,
                {hranila[42]} TEXT NOT NULL,
                {hranila[43]} TEXT NOT NULL,
                {hranila[44]} TEXT NOT NULL,
                {hranila[45]} TEXT NOT NULL,
                {hranila[46]} TEXT NOT NULL,
                {hranila[47]} TEXT NOT NULL,
                {hranila[48]} TEXT NOT NULL,
                {hranila[49]} TEXT NOT NULL,
                {hranila[50]} TEXT NOT NULL,
                {hranila[51]} TEXT NOT NULL,
                {hranila[52]} TEXT NOT NULL,
                {hranila[53]} TEXT NOT NULL,
                {hranila[54]} TEXT NOT NULL,
                {hranila[55]} TEXT NOT NULL,
                {hranila[56]} TEXT NOT NULL,
                {hranila[57]} TEXT NOT NULL,
                {hranila[58]} TEXT NOT NULL,
                {hranila[59]} TEXT NOT NULL,
                {hranila[60]} TEXT NOT NULL,
                {hranila[61]} TEXT NOT NULL,
                {hranila[62]} TEXT NOT NULL,
                {hranila[63]} TEXT NOT NULL,
                {hranila[64]} TEXT NOT NULL,
                {hranila[65]} TEXT NOT NULL,
                {hranila[66]} TEXT NOT NULL,
                {hranila[67]} TEXT NOT NULL,
                {hranila[68]} TEXT NOT NULL,
                {hranila[69]} TEXT NOT NULL,
                {hranila[70]} TEXT NOT NULL,
                {hranila[71]} TEXT NOT NULL,
                {hranila[72]} TEXT NOT NULL,
                {hranila[73]} TEXT NOT NULL,
                {hranila[74]} TEXT NOT NULL,
                {hranila[75]} TEXT NOT NULL
            );""")
        
        # ZiviloObrok (#8):
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS ZiviloObrok
            (   ime_zivila TEXT NOT NULL,
                id_obroka INTEGER NOT NULL,
                kolicina INTEGER,
                FOREIGN KEY (ime_zivila) REFERENCES Zivilo(name),
                FOREIGN KEY (id_obroka) REFERENCES Obrok(id_obroka)) 
                 """)
        # Omejitve (#9)
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Omejitve
            (   id_omejitve INTEGER PRIMARY KEY AUTOINCREMENT,
                id_uporabnika INTEGER NOT NULL,
                magnesium_mg INTEGER NOT NULL,
                vitamin_a_IU DECIMAL NOT NULL,
                vitamin_b12_mcg DECIMAL NOT NULL,
                vitamin_b6_mg DECIMAL NOT NULL,
                vitamin_c_mg INTEGER NOT NULL,
                vitamin_d_IU INTEGER NOT NULL,
                vitamin_e_mg INTEGER NOT NULL,
                vitamin_k_mcg INTEGER NOT NULL,
                calcium_mg INTEGER NOT NULL,
                protein_g INTEGER NOT NULL,
                carbohydrate_g INTEGER NOT NULL,
                fiber_g INTEGER NOT NULL,
                sodium_mg INTEGER NOT NULL,
                iron_mg DECIMAL NOT NULL,
                potassium_mg INTEGER NOT NULL,
                zink_mg INTEGER NOT NULL,
                water_g INTEGER NOT NULL  
            );""")

def napolni_nujne_podatke(conn):
    #Napolni tabelo zivilo
    with conn:
        df1 = pd.read_csv(r'data/modified.csv')
        df2 = pd.read_csv(r'data/exercise_dataset.csv')
        hranila = []
        for col in df1.columns:
            hranila.append(col) #hranila vsebuje imena stolpcev, dolzina je 77
        for vrstica in df1.itertuples():
            i = 0
            # mogoce je ena več ali ena manj
            try:
                conn.execute(f"""
                INSERT INTO Zivilo ({hranila[0]}, {hranila[1]}, {hranila[2]}, {hranila[3]}, {hranila[4]}, {hranila[5]}, {hranila[6]}, {hranila[7]}, {hranila[8]}, {hranila[9]}, {hranila[10]} , {hranila[11]} , {hranila[12]} ,{ hranila[13]} , {hranila[14]} , {hranila[15]} , {hranila[16]} , {hranila[17]} , {hranila[18]} , {hranila[19]} , {hranila[20]} , {hranila[21]} , {hranila[22]} , {hranila[23]} , {hranila[24]} , {hranila[25]} , {hranila[26]} , {hranila[27]} , {hranila[28]} ,{ hranila[29]} , {hranila[30]} , {hranila[31]} , {hranila[32]} , {hranila[33]} , {hranila[34]} , {hranila[35]} , {hranila[36]} , {hranila[37]} , {hranila[38]} , {hranila[39]} , {hranila[40]} , {hranila[41]} , {hranila[42]} , {hranila[43]} , {hranila[44]} , {hranila[45]} , {hranila[46]} , {hranila[47]} , {hranila[48]} , {hranila[49]} , {hranila[50]} , {hranila[51]} , {hranila[52]} ,{ hranila[53]} , {hranila[54]} , {hranila[55]} ,{ hranila[56]} , {hranila[57]} , {hranila[58]} ,{ hranila[59]} , {hranila[60]} , {hranila[61]} , {hranila[62]} , {hranila[63]} , {hranila[64]} , {hranila[65]} ,{hranila[66]} ,{ hranila[67]} , {hranila[68]} , {hranila[69]} , {hranila[70]} , {hranila[71]} , {hranila[72]} , {hranila[73]} , {hranila[74]}, {hranila[75]} )
                VALUES ('{vrstica[1]}', '{vrstica[2]}', '{vrstica[3]}', '{vrstica[4]}', '{vrstica[5]}', '{vrstica[6]}', '{vrstica[7]}', '{vrstica[8]}', '{vrstica[9]}', '{vrstica[10]}' , '{vrstica[11]}' , '{vrstica[12]}' , '{vrstica[13]}' , '{vrstica[14]}' , '{vrstica[15]}' , '{vrstica[16]}' , '{vrstica[17]}' , '{vrstica[18]}' , '{vrstica[19]}' , '{vrstica[20]}' , '{vrstica[21]}' , '{vrstica[22]}' , '{vrstica[23]}' , '{vrstica[24]}' , '{vrstica[25]}' , '{vrstica[26]}' , '{vrstica[27]}' , '{vrstica[28]}' , '{vrstica[29]}' , '{vrstica[30]}' , '{vrstica[31]}' , '{vrstica[32]}' , '{vrstica[33]}' , '{vrstica[34]}' , '{vrstica[35]}' , '{vrstica[36]}', '{vrstica[37]}', '{vrstica[38]}', '{vrstica[39]}', '{vrstica[40]}', '{vrstica[41]}', '{vrstica[42]}', '{vrstica[43]}', '{vrstica[44]}', '{vrstica[45]}' , '{vrstica[46]}' , '{vrstica[47]}' , '{vrstica[48]}' , '{vrstica[49]}' , '{vrstica[50]}' , '{vrstica[51]}' , '{vrstica[52]}' , '{vrstica[53]}' , '{vrstica[54]}' , '{vrstica[55]}' , '{vrstica[56]}' , '{vrstica[57]}' , '{vrstica[58]}' , '{vrstica[59]}' , '{vrstica[60]}' , '{vrstica[61]}' , '{vrstica[62]}' , '{vrstica[63]}' , '{vrstica[64]}' , '{vrstica[65]}' , '{vrstica[66]}' , '{vrstica[67]}' , '{vrstica[68]}' , '{vrstica[69]}' , '{vrstica[70]}', '{vrstica[71]}', '{vrstica[72]}', '{vrstica[73]}', '{vrstica[74]}', '{vrstica[75]}', {vrstica[76]})
                            """)
            except:
                pass

        for vrstica in df2.itertuples():
            try:
                conn.execute(f""" 
                INSERT INTO Aktivnost (id_aktivnost, poraba_kalorij_na_kg)
                VALUES ('{vrstica[1]}', {vrstica[6]})
                """)
            except:
                pass

def pripravi_in_napolni_bazo():
    db = sqlite3.connect("osebni_trener.db")
    pripravi_bazo()
    print("Baza je pripravljena")
    napolni_nujne_podatke(db)
    print("Baza je napolnjena")
