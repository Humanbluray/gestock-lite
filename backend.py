import sqlite3 as sql
import datetime

mybase = "stock.db"


def convertir_date_en_objet(date: str):
    annee = int(date[0: 4])
    mois = int(date[5: 7])
    jour = int(date[8:10])

    objet = datetime.date(annee, mois, jour)
    return objet


def milSep(nombre: int):
    nombre = str(nombre)[::-1]
    resultat = ""
    for i, numero in enumerate(nombre, 1):
        numero_formatte = numero + " " if i % 3 == 0 and i != len(nombre) else numero
        resultat += numero_formatte

    return resultat[::-1]


def connexion_base():
    conn = sql.connect(mybase)
    cur = conn.cursor()

    # Table articles
    cur.execute("""CREATE TABLE IF NOT exists articles (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    reference   TEXT,
                    designation TEXT,
                    unite       TEXT,
                    prix        NUMERIC,
                    casier      TEXT)""")

    # Table entrees
    cur.execute("""CREATE TABLE IF NOT exists entrees (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero       TEXT,
                    bon          TEXT,
                    date         TEXT,
                    id_ref       INTEGER,
                    qte          NUMERIC,
                    prix         NUMERIC,
                    commentaires TEXT)""")

    # Table imputations
    cur.execute("""CREATE TABLE IF NOT EXISTS imputations (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    code        TEXT,
                    designation TEXT)""")

    # Table mouvements
    cur.execute("""CREATE TABLE IF NOT EXISTS mouvements (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    type_mvt   TEXT,
                    numero_mvt TEXT,
                    id_ref     INTEGER,
                    stock_avt  NUMERIC,
                    stock_ap   NUMERIC,
                    qte        NUMERIC,)""")

    # Table des sorties
    cur.execute("""CREATE TABLE IF NOT EXISTS sorties (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero      TEXT,
                    bon         TEXT,
                    date        DATE,
                    imputation  TEXT,
                    id_ref      INTEGER,
                    qte         NUMERIC,
                    commentaire TEXT)""")

    # Table des stocks
    cur.execute("""CREATE TABLE IF NOT EXISTS CREATE TABLE stock (
                    id_ref INTEGER,
                    qte    NUMERIC)""")

    conn.commit()
    conn.close()


def add_article(ref, des, unit, prix, casier):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""INSERT INTO articles VALUES (?,?,?,?,?,?)""", (cur.lastrowid, ref, des, unit, prix, casier))
    conn.commit()
    conn.close()


def all_ref_name():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT reference, designation FROM articles""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def all_imputations_name():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT code FROM imputations""")
    result = cur.fetchall()
    final = [row[0] for row in result]
    conn.commit()
    conn.close()
    return final


def find_article_id_by_ref(ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM articles WHERE reference = ?""", (ref,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def last_article_id():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM articles ORDER by id desc""")
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def article_by_id(id_ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM articles WHERE id = ?""", (id_ref,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def delete_article_by_id(id_ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""DELETE FROM articles WHERE id = ?""", (id_ref,))
    conn.commit()
    conn.close()


def is_exists_ref(ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT reference FROM articles""")
    result = cur.fetchall()
    final = [row[0] for row in result]
    conn.commit()
    conn.close()
    return True if ref in final else False


def find_numero_bon_entree():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM entrees ORDER BY id DESC""")
    result = cur.fetchone()
    if result is None:
        nb = 1
    else:
        nb = result[0] + 1

    if 1 <= nb <= 9:
        numero = "RECP00" + str(nb)
    elif 10 <= nb <= 99:
        numero = "RECP0" + str(nb)
    else:
        numero = 'RECP' + str(nb)

    conn.commit()
    conn.close()
    return numero


def find_numero_bon_sortie():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT id FROM sorties ORDER BY id DESC""")
    result = cur.fetchone()
    if result is None:
        nb = 1
    else:
        nb = result[0] + 1

    if 1 <= nb <= 9:
        numero = "SORT00" + str(nb)
    elif 10 <= nb <= 99:
        numero = "SORT0" + str(nb)
    else:
        numero = 'SORT' + str(nb)

    conn.commit()
    conn.close()
    return numero


def add_stock(id_d_ref, qte):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""INSERT INTO stock VALUES (?,?)""", (id_d_ref, qte))
    conn.commit()
    conn.close()


def update_ref(des, unite, casier, reference):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""UPDATE articles SET designation = ?,
                    unite = ?,
                    casier = ?
                    WHERE reference = ?""", (des, unite, casier, reference))
    conn.commit()
    conn.close()


def update_stock(qte, id_ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""UPDATE stock SET qte = ? WHERE id_ref = ?""", (qte, id_ref))
    conn.commit()
    conn.close()


def update_prix(prix, id_ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""UPDATE articles SET prix = ? WHERE id = ?""", (prix, id_ref))
    conn.commit()
    conn.close()


def all_articles_stock():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""select articles.id, articles.reference, articles.designation, 
                    articles.unite, articles.prix, articles.casier, stock.qte FROM
                    articles, stock WHERE articles.id = stock.id_ref""")

    result = cur.fetchall()
    final = [
        {"id": row[0], "ref": row[1], "des": row[2], "unite": row[3], "prix": row[4], "casier": row[5], "stock": row[6]}
        for row in result
    ]

    conn.commit()
    conn.close()
    return final


def add_entree(num, bon, date, id_ref, qte, prix, commentaire):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""INSERT INTO entrees values (?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, num, bon, date, id_ref, qte, prix, commentaire))
    conn.commit()
    conn.close()


def add_sortie(num, bon, date, imputation, id_ref, qte, commentaire):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("INSERT INTO sorties values (?,?,?,?,?,?,?,?)",
                (cur.lastrowid, num, bon, date, imputation, id_ref, qte, commentaire))
    conn.commit()
    conn.close()


def add_mouvement(type_mvt, num_mvt, id_ref, st_avt, st_ap, qte):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""INSERT INTO mouvements values (?,?,?,?,?,?,?)""",
                (cur.lastrowid, type_mvt, num_mvt, id_ref, st_avt, st_ap, qte))
    conn.commit()
    conn.close()


def sortie_by_numero(numero):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM sorties WHERE numero = ?""", (numero,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def entree_by_numero(numero):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM entrees WHERE numero = ?""", (numero,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


# print(entree_by_numero('RECP1'))


def date_mouvements_by_id(id_mvt):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT type_mvt, numero_mvt FROM mouvements WHERE id = ?""", (id_mvt,))
    result = cur.fetchone()

    if result[0] == "S":
        mvt = sortie_by_numero(result[1])[3]
        date_mvt = convertir_date_en_objet(mvt)
    else:
        mvt = entree_by_numero(result[1])[3]
        date_mvt = convertir_date_en_objet(mvt)

    conn.commit()
    conn.close()
    return date_mvt


def is_histo_exists(id_ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM mouvements WHERE id_ref = ?""", (id_ref,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return False if result is None else True


def check_login(login, password):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT login, password FROM users""")
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return True if (login, password) in result else False


def all_mouvements(ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT mouvements.id, mouvements.type_mvt, mouvements.numero_mvt, articles.reference, 
                    mouvements.stock_avt, mouvements.qte, mouvements.stock_ap 
                    FROM mouvements, articles WHERE articles.id = mouvements.id_ref""")
    result = cur.fetchall()

    # for row in result:
    #     print(result)

    new_res = []
    for row in result:
        date_mvt = date_mouvements_by_id(row[0])
        new_row = row + (date_mvt,)
        new_res.append(new_row)

    dico = [
        {
            'type': row[1], 'numero': row[2], 'date': row[7], 'ref': row[3], 'stock avt': row[4],
            'qte': row[5], 'stock ap': row[6]
        }
        for row in new_res if ref == row[3]
    ]
    final = sorted(dico, key=lambda x: x['date'], reverse=True)

    conn.commit()
    conn.close()
    return final


# print(all_mouvements("TEST"))


def stock_by_id(id_ref):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""SELECT qte FROM stock WHERE id_ref = ?""", (id_ref,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def update_qte_sortie(qte, numero):
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""UPDATE sorties SET qte = ? WHERE numero = ?""", (qte, numero))
    conn.commit()
    conn.close()


def all_entrees():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""select entrees.id, entrees.numero, entrees.bon, entrees.date, entrees.id_ref, 
                    entrees.qte, entrees.prix, entrees.commentaires, 
                    articles.id, articles.reference, articles.designation, articles.unite 
                    from entrees, articles WHERE entrees.id_ref = articles.id""")

    result = cur.fetchall()
    final = [
        {
            'id_ent': row[0], 'numero': row[1], 'bon': row[2], 'date': convertir_date_en_objet(row[3]),
            'id_ref': row[4], 'qte': row[5], 'prix': row[6], 'comm': row[7], 'ref': row[9], 'des': row[10],
            'unite': row[11], 'total': row[5] * row[6]
         }
        for row in result
    ]

    conn.commit()
    conn.close()
    return final


def all_sorties():
    conn = sql.connect(mybase)
    cur = conn.cursor()
    cur.execute("""select sorties.id, sorties.numero, sorties.bon, sorties.date, sorties.id_ref, 
                    sorties.qte, sorties.imputation, sorties.commentaire, 
                    articles.id, articles.reference, articles.designation, articles.unite 
                    from sorties, articles WHERE sorties.id_ref = articles.id""")

    result = cur.fetchall()
    final = [
        {
            'id_ent': row[0], 'numero': row[1], 'bon': row[2], 'date': convertir_date_en_objet(row[3]),
            'id_ref': row[4], 'qte': row[5], 'imputation': row[6], 'comm': row[7], 'ref': row[9], 'des': row[10],
            'unite': row[11],
        }
        for row in result
    ]

    conn.commit()
    conn.close()
    return final





