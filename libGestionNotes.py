import mysql.connector
import sys


class bdd:
    def __init__(self,config : dict):
        """
        Constructeur de la classe bdd
            parametre : config : dictionnaire des parametres de connexion
            exemple : config = {
                                'user': 'username',
                                'password': 'pass',
                                'host': '127.0.0.1',
                                'database': 'myDatabase',
                                'raise_on_warnings': True
                               }
        """
        try:
            self.connect = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Nom d'utilisateur ou mot de passe incorrect !")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("La base de donnée spécifiée n'existe pas !")
            else:
                print(err)
            sys.exit()

        else:
            print("Base de donnée connectée...")
            self.cursor = self.connect.cursor()

    def fermer(self):
        """
            Fermeture de la connexion au serveur MySQL
        """
        self.cursor.close()
        self.connect.close()


    def execute(self, query):
        """
        Méthode à usage interne de la classe (membre privé)
        :param query: requète à exécuter
        :return: le nombre de ligne(s) affectée(s) dans la table si tout c'est bien passé
                 sinon, affiche le code d'erreur MySQL et retourne -1
        """
        try:
            self.cursor.execute(query)
            self.connect.commit()
            count = self.cursor.rowcount
            return count
        except mysql.connector.Error as err:
            print(err)
            return -1


    def ajouter(self,table : str, a_ajouter : dict):
        """
        Ajouter des données dans une table
        :param table: Nom de la table à affecter
        :param a_ajouter: Dictionnaire des valeurs à ajouter
                          exemple : {"colonne1":"valeur1", "colonne2":"valeur2"}
        :return: le nombre de ligne(s) affectée(s) dans la table si tout c'est bien passé
                 sinon, affiche le code d'erreur MySQL et retourne -1
                             if value == 'NULL':
                query += "`" + key + "`=" + value
            else :
                query += "`"+key+"`="+"'"+value+"'"
            if nb_key>1:
                query += ", "
                nb_key-=1
        """
        query = "INSERT INTO "+table+" ("
        nb_key = len(a_ajouter)
        for key in a_ajouter:
            #print(nb_key)
            query += "`"+key+"`"
            if nb_key>1:
                query += ","
                nb_key-=1
            else:
                query += ") VALUES ("
        nb_key = len(a_ajouter)
        for value in a_ajouter.values():
            #print(value)
            if value == 'NULL':
                query += value
            else:
                query += "'"+value+"'"
            if nb_key>1:
                query += ","
                nb_key-=1
            else:
                query += ");"
        print(query)
        return self.execute(query)

    def supprimer(self, table: str, conditions: dict):
        """
        Supprimer des données présente dans une table
        :param table: Nom de la table à affecter
        :param conditions: Dictionnaire des conditions pour générer la clause WHERE
                exemple : {"colonne1":"valeur1"}
                exemple : {"colonne1":"valeur1", "_op":"AND", "colonne2":"valeur2"}
                Entre chaque condition, doit apparaitre un opérateur logique
                clé : "_op", valeur : "AND", "OR", "NOT", ...
        :return: le nombre de ligne(s) affectée(s) dans la table si tout c'est bien passé
                 sinon, affiche le code d'erreur MySQL et retourne -1
        """
        #print(conditions)

        query = "DELETE FROM  " + table + " WHERE "
        #print(query)
        for key, value in conditions.items():
            #print(key, value)
            if "_op" in key:
                query += " " + value + " "
            else:
                query += key + "=" + value

        query += ";"
        print(query)
        exec_query = self.execute(query)
        #print("exec_query : ", exec_query)
        return exec_query

    def supprimer_multitables(self, tables: list, conditions: dict):
        """
        Supprimer des données présentes dans une table avec conditions sur plusieurs tables
        :param table: Nom des la tables à utiliser, la première est celle à affecter
        :param conditions: Dictionnaire des conditions pour générer la clause WHERE
                exemple : {"colonne1":"valeur1"}
                exemple : {"colonne1":"valeur1", "_op":"AND", "colonne2":"valeur2"}
                Entre chaque condition, doit apparaitre un opérateur logique
                clé : "_op", valeur : "AND", "OR", "NOT", ...
        :return: le nombre de ligne(s) affectée(s) dans la table si tout c'est bien passé
                 sinon, affiche le code d'erreur MySQL et retourne -1
        """
        #print(conditions)

        query = "DELETE "
        query += tables[0]
        query += " FROM "

        nb_tables = len(tables)
        for table in tables:
            # print(table)
            query += "`" + table + "`"
            if nb_tables > 1:
                query += ", "
                nb_tables -= 1

        # print(query)
        query += " WHERE "

        for key, value in conditions.items():
            #print(key, value)
            if "_op" in key:
                query += " " + value + " "
            else:
                query +=  key + "=" + value
        print(query)
        exec_query = self.execute(query)
        #print("exec_query : ", exec_query)
        return exec_query


    def mettre_a_jour(self,table : str, a_modifier : dict, conditions : dict):
        """
        Modifier des données déja présentes dans une table
        :param table: Nom de la table à affecter
        :param a_modifier: Dictionnaire des valeurs à modifier
                exemple : {"colonne1":"valeur1", "colonne2":"valeur2"}
        :param conditions: Dictionnaire des conditions pour générer la clause WHERE
                exemple : {"colonne1":"valeur1"}
                exemple : {"colonne1":"valeur1", "_op":"AND", "colonne2":"valeur2"}
                Entre chaque condition, doit apparaitre un opérateur logique
                clé : "_op", valeur : "AND", "OR", "NOT", ...
        :return: le nombre de ligne(s) affectée(s) dans la table si tout c'est bien passé
                 sinon, affiche le code d'erreur MySQL et retourne -1
        """
        query = "UPDATE "+table+" SET "
        nb_key = len(a_modifier)
        for key, value in a_modifier.items():
            #print(nb_key)
            if value == 'NULL':
                query += "`" + key + "`=" + value
            else :
                query += "`"+key+"`="+"'"+value+"'"
            if nb_key>1:
                query += ", "
                nb_key-=1
            else:
                query += " WHERE "

        for key, value in conditions.items():
            #print(key,value)
            if "_op" in key:
                query += " "+ value + " "
            else:
                query += "`"+key+"`='"+value+"'"

        query += ";"
        print(query)
        exec_query = self.execute(query)
        #print("exec_query : ", exec_query)
        return exec_query

    def afficher(self, tables : list, colonnes : list, filtre : dict={}):
        """
        Afficher des valeurs des colonnes d'une ou plusieurs tables en fonction du filtre choisi
        :param tables: Liste des tables concernées. ex : ["table1", "table2"]
        :param colonnes: Liste des colonnes à afficher. ex : ["col1", "col2", "col3"]
        :param filtre: Dictionnaire des conditions pour générer la clause WHERE
                exemple : {"colonne1":"valeur1"}
                exemple : {"colonne1":"valeur1", "_op":"AND", "colonne2":"valeur2"}
                Entre chaque condition, doit apparaitre un opérateur logique
                clé : "_opx", valeur : "AND", "OR", "NOT", ...
                si plusieurs opérateurs logiques sont nécessaires : x = 1,2,... (_op1, _op2, ...)
        :return: Une liste de dictionnaires des colonnes et valeurs à afficher
        """

        #print(tables, colonnes)
        query = "SELECT "

        nb_colonnes = len(colonnes)
        for colonne in colonnes:
            #print(colonne)
            #query += "`" + colonne + "`"
            query += colonne
            if nb_colonnes > 1:
                query += ", "
                nb_colonnes -= 1

        query += " FROM "

        nb_tables = len(tables)
        for table in tables:
            #print(table)
            query += "`" + table + "`"
            if nb_tables > 1:
                query += ", "
                nb_tables -= 1

        if len(filtre)>0:

            if not (len(filtre)==1 and ('_op0' in filtre and "ORDER BY" in filtre['_op0'])):
                query += " WHERE "
            #else:
                #print(filtre['_op0'])

            for key, value in filtre.items():
                #print(key, value)
                if "_op" in key:
                    query += " " + value + " "
                else:
                    if value.lower()== "null":
                        query += key + " is NULL "
                    else:
                        query += key + "=" +  value

        query += ";"
        print(query)

        # Execution de la requète
        self.cursor.execute(query)
        # Récupération des noms de colonnes depuis MySQL
        mysq_colonnes = self.cursor.description
        #print(mysq_colonnes)
        # mysq_colonnes est une liste de tuples dont le premier élément de chaque tuple correspond à une colonne de la table
        # Préparation de la liste des résultats
        result = []
        # pour chaque ligne retournée par MySQL
        for enregistements in self.cursor.fetchall():
            # préparation du dictionnaire des résultats pour une ligne
            #print(enregistements)
            tmp = {}
            # index contient le numéro de colonne
            # enregistrement contient la valeur de l'enregitrement dans la colonne courante pour la ligne courante
            for (index, enregistrement) in enumerate(enregistements):
                #print(index, enregistrement)
                tmp[mysq_colonnes[index][0]] = enregistrement
            result.append(tmp)
        return result

class eleves:
    def __init__(self, bdd_notes):
        self.bdd = bdd_notes

    def liste(self, table = ["Eleve"], colonnes = ["id_eleve", "nom_eleve", "prenom_eleve", "id_classe"], filtre = {}):
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_classe(self, id_classe):
        table = ["Eleve", "Classe"]
        filtre = {"Classe.id_classe": "Eleve.id_classe", "_op1": "AND", "Eleve.id_classe": "'"+id_classe+"'",
                  "_op0": "ORDER BY Eleve.nom_eleve ASC"}
        colonnes = ["Eleve.id_eleve", "Eleve.nom_eleve", "Eleve.prenom_eleve", "Eleve.id_classe", "Classe.nom"]
        return self.liste(table, colonnes, filtre)

    def liste_annee(self, annee):
        #SELECT Eleve.id_eleve, Eleve.nom, Eleve.prenom, Classe.id_classe, Classe.nom FROM `Eleve`, Classe WHERE Eleve.id_classe=Classe.id_classe AND Classe.annee=2019 ORDER BY Eleve.nom ASC
        table = ["Eleve", "Classe"]
        filtre = {"Eleve.id_classe": "Classe.id_classe", "_op1": "AND", "Classe.annee": annee, "_op0": "ORDER BY Eleve.nom_eleve ASC" }
        colonnes = ["Eleve.id_eleve", "Eleve.nom_eleve", "Eleve.prenom_eleve", "Eleve.id_classe", "Classe.nom"]
        return self.liste(table, colonnes, filtre)

    def liste_non_affectes(self):
        table = ["Eleve"]
        filtre = {"Eleve.id_classe": "NULL", "_op0": "ORDER BY Eleve.nom_eleve ASC"}
        colonnes = ["Eleve.id_eleve", "Eleve.nom_eleve", "Eleve.prenom_eleve"]
        return self.liste(table, colonnes, filtre)

    def moyenne(self, id_eleve : str, id_matiere : str):
        table = ["a_obtenu", "Eleve"]
        colonnes = ["a_obtenu.id_eleve",  "nom_eleve", "prenom_eleve", "AVG(note) as moyenne"]
        filtre = {"a_obtenu.`id_eleve`": "Eleve.id_eleve",
                  "_op0": "AND",
                  "id_matiere": "'" + str(id_matiere) + "'",
                  "_op1": "AND",
                  "a_obtenu.id_eleve": "'" + id_eleve + "'"}
        return self.bdd.afficher(table, colonnes, filtre)[0]

    def supprimer(self, id_eleve : str):
        table = "Eleve"
        condition = {"id_eleve": id_eleve}
        return self.bdd.supprimer(table, condition)

    def mettre_a_jour(self, a_modifier: dict, id_eleve: str):
        table = "Eleve"
        condition = {"id_eleve": id_eleve}
        return self.bdd.mettre_a_jour(table, a_modifier, condition)

    def ajouter(self, a_ajouter):
        table = "Eleve"
        return self.bdd.ajouter(table, a_ajouter)


class professeurs:
    def __init__(self, bdd_notes):
        self.bdd = bdd_notes

    def liste(self, table = ["Professeur"], colonnes = ["Professeur.id_professeur", "Professeur.nom", "Professeur.prenom"], filtre = {"_op0": " ORDER BY `Professeur`.`nom` ASC"} ):
        return self.bdd.afficher(table,colonnes,filtre)


    def liste_matieres(self, id_professeur):
        table = ["enseigne", "Matiere"]
        colonnes = ["Matiere.id_matiere", "Matiere.libelle"]
        filtre = {"Matiere.id_matiere":"enseigne.id_matiere", "_op1": "AND", "enseigne.id_professeur":"'"+id_professeur+"'"}
        return self.liste(table, colonnes, filtre)

    def id_professeur(self, nom : str, prenom : str):
        table = ["Professeur"]
        colonnes = ["Professeur.id_professeur"]
        filtre = {"nom": "'"+nom+"'", "_op1": "AND", "prenom": "'"+prenom+"'"}
        pp = self.liste(table, colonnes, filtre)
        print(pp)
        return pp[0]['id_professeur']

    def supprimer(self, id_professeur):
        table = "Professeur"
        condition = {"id_professeur": id_professeur}
        return self.bdd.supprimer(table, condition)

    def mettre_a_jour(self, a_modifier: dict, id_professeur: str):
        table = "Professeur"
        condition = {"id_professeur": id_professeur}
        return self.bdd.mettre_a_jour(table, a_modifier, condition)

    def ajouter(self, a_ajouter):
        table = "Professeur"
        return self.bdd.ajouter(table, a_ajouter)

    def ajouter_enseignement(self,id_professeur, id_matiere):
        table = "enseigne"
        a_ajouter = {'id_professeur': id_professeur, 'id_matiere': str(id_matiere)}
        return self.bdd.ajouter(table, a_ajouter)

    def supprimer_enseignement(self, id_professeur, id_matiere):
        table = "enseigne"
        condition = {"id_professeur": "'"+id_professeur+"'", "_op": "AND", "id_matiere": "'"+str(id_matiere)+"'" }
        return self.bdd.supprimer(table, condition)


class matieres:
    def __init__(self, bdd_notes):
        self.bdd = bdd_notes

    def liste(self, table = ["Matiere"], colonnes = ["Matiere.id_matiere", "Matiere.libelle", "Matiere.description"], filtre = {"_op0": " ORDER BY `Matiere`.`libelle` ASC"}):
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_classe(self, id_classe):

        table = ["a_obtenu", "Eleve", "Matiere" ]
        colonnes = ["DISTINCT a_obtenu.`id_matiere`", "libelle"]
        filtre = {"a_obtenu.id_eleve": "Eleve.id_eleve",
                  "_op0": "AND",
                  "a_obtenu.id_matiere": "Matiere.id_matiere",
                  "_op1": "AND",
                  "Eleve.id_classe": "'" + id_classe + "'",
                  "_op2": " ORDER BY `libelle` ASC"}
        return self.bdd.afficher(table, colonnes, filtre)

    def statitiques(self, id_classe : str, id_matiere : str, devoir=""):
        table = ["a_obtenu", "Eleve"]
        colonnes = ["COUNT(note) as nombre_notes", "AVG(note) as moyenne", "MAX(note) as max", "MIN(note) as min"]
        filtre = {"a_obtenu.`id_eleve`": "Eleve.id_eleve",
                  "_op0": "AND",
                  "Eleve.id_classe": "'" + id_classe + "'",
                  "_op1": "AND",
                  "id_matiere": "'" + str(id_matiere) + "'"}
        if devoir != "":
            filtre["_op2"] = "AND"
            filtre["devoir"] = "'" + devoir + "'"
        return self.bdd.afficher(table, colonnes, filtre)[0]

    def supprimer(self, id_matiere : str):
        table = "Matiere"
        condition = {"id_matiere": id_matiere}
        return self.bdd.supprimer(table, condition)

    def mettre_a_jour(self, a_modifier: dict, id_matiere: str):
        table = "Matiere"
        condition = {"id_matiere": id_matiere}
        return self.bdd.mettre_a_jour(table, a_modifier, condition)

    def ajouter(self, a_ajouter):
        table = "Matiere"
        return self.bdd.ajouter(table, a_ajouter)

class classes:

    def __init__(self, bdd_notes):
        self.bdd = bdd_notes

    def liste(self, table = ["Classe"], colonnes = ["Classe.id_classe", "Classe.nom", "Classe.niveau", "Classe.annee", "Classe.id_professeur"], filtre = {"_op0": " ORDER BY `Classe`.`id_classe` ASC"}):
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_niveau(self, niveau : str):
        table = ["Classe"]
        colonnes = ["Classe.id_classe", "Classe.niveau", "Classe.annee", "Classe.id_professeur"]
        filtre = {"Classe.niveau": niveau, "_op1": " ORDER BY `Classe`.`id_classe` ASC"}
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_annee(self, annee):
        table = ["Classe"]
        colonnes = ["Classe.id_classe", "Classe.nom", "Classe.niveau", "Classe.annee", "Classe.id_professeur"]
        filtre = {"Classe.annee": annee, "_op1": " ORDER BY `Classe`.`id_classe` ASC"}
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_annee_niveau(self, annee,niveau):
        table = ["Classe"]
        colonnes = ["Classe.id_classe", "Classe.nom", "Classe.niveau", "Classe.annee", "Classe.id_professeur"]
        filtre = {"Classe.annee": annee, "_op1": "AND" ,"Classe.niveau": niveau, "_op2": " ORDER BY `Classe`.`id_classe` ASC"}
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_annees(self):
        table = ["Classe"]
        colonnes = ["DISTINCT Classe.annee"]
        filtre = {"_op0": " ORDER BY `Classe`.`annee` DESC"}
        return self.bdd.afficher(table, colonnes, filtre)

    def supprimer(self, id_classe):
        table = "Classe"
        condition = {"id_classe": id_classe}
        return self.bdd.supprimer(table, condition)

    def prof_principal(self, id_professeur):
        table = ["Professeur"]
        colonnes = ["id_professeur", "nom", "prenom"]
        filtre = {"id_professeur": id_professeur}
        return self.bdd.afficher(table, colonnes, filtre)

    def mettre_a_jour(self, a_modifier: dict, id_classe: str):
        table = "Classe"
        condition = {"id_classe": id_classe}
        return self.bdd.mettre_a_jour(table, a_modifier, condition)

    def ajouter(self, a_ajouter):
        table = "Classe"
        return self.bdd.ajouter(table, a_ajouter)

    def classe(self, id_classe):
        table = ["Classe"]
        colonnes = ["nom"]
        filtre = {"id_classe": "'"+id_classe+"'"}
        return self.liste(table, colonnes, filtre)[0]['nom']

class notes:
    def __init__(self, bdd_notes):
        self.bdd = bdd_notes

    def liste(self, table = ["a_obtenu"], colonnes = ["id_eleve", "id_professeur", "note", "date", "devoir"], filtre = {"_op0": " ORDER BY `id_eleve` ASC"}):
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_devoirs(self, table = ["a_obtenu"], colonnes = ["DISTINCT devoir, date(date)"], filtre = {"_op0": " ORDER BY `date` ASC"}):
        return self.liste(table, colonnes, filtre)

    def liste_devoirs_professeur(self, professeur, classe = "", matiere =""):
        table = ["a_obtenu", "Eleve"]
        colonnes = ["DISTINCT devoir"]
        filtre = {"a_obtenu.id_professeur":"'"+professeur+"'",
                  "_op1": "AND",
                  "a_obtenu.id_eleve":  "Eleve.id_eleve"}
        if classe != "":
            filtre["_op2"] = "AND"
            filtre["Eleve.id_classe"] = "'" + classe + "'"

        if matiere != "":
            filtre["_op3"] = "AND"
            filtre["a_obtenu.id_matiere"] = "'" + str(matiere) + "'"
        filtre["_op4"] =  " ORDER BY `devoir` ASC"
        return self.liste(table, colonnes, filtre)

    def liste_notes(self):
        table = ['Classe', 'Eleve', 'a_obtenu', 'Matiere']
        colonnes = ['Eleve.nom_eleve as nom',
                    'Eleve.prenom_eleve as prenom',
                    'a_obtenu.devoir as devoir',
                    'a_obtenu.note as note',
                    'a_obtenu.date as date',
                    ' Matiere.libelle as libelle',
                    'Classe.id_classe as classe']
        filtre = {"Eleve.id_eleve":"a_obtenu.id_eleve",
                  "_op1":"AND",
                  "a_obtenu.id_matiere":"Matiere.id_matiere",
                  "_op2":"AND",  "Eleve.id_classe":"Classe.id_classe"}
        return self.bdd.afficher(table, colonnes, filtre)

    def liste_notes_professeur(self, professeur, classe="", matiere="", devoir=""):
        table = ['Classe', 'Eleve', 'a_obtenu', 'Matiere']
        colonnes = ['Eleve.id_eleve as id_eleve',
                    'Eleve.nom_eleve as nom',
                    'Eleve.prenom_eleve as prenom',
                    'a_obtenu.devoir as devoir',
                    'a_obtenu.note as note',
                    'a_obtenu.date as date',
                    ' Matiere.libelle as libelle',
                    'Classe.id_classe as classe']
        filtre = {"Eleve.id_eleve":"a_obtenu.id_eleve",
                  "_op1":"AND",  "a_obtenu.id_matiere":"Matiere.id_matiere",
                  "_op2":"AND",  "Classe.id_classe":"Eleve.id_classe",
                  "_op3": "AND", "Classe.annee":"YEAR(NOW())",
                  "_op4":"AND",  "a_obtenu.id_professeur":"'"+professeur+"'"}
        if classe != "":
            filtre["_op5"] = "AND"
            filtre["Eleve.id_classe"] = "'"+classe+"'"

        if matiere != "":
            filtre["_op6"] = "AND"
            filtre["libelle"] = "'"+matiere+"'"

        if devoir != "":
            filtre["_op7"] = "AND"
            filtre["devoir"] = "'"+devoir+"'"

        filtre["_op0"] = "ORDER BY nom, prenom ASC"

        return self.bdd.afficher(table, colonnes, filtre)

    def devoirs_eleve(self, id_eleve, id_matiere=""):
        table = ['Classe', 'Eleve', 'a_obtenu', 'Matiere']
        colonnes = ['Eleve.nom_eleve as nom',
                    'Eleve.prenom_eleve as prenom',
                    'a_obtenu.devoir as devoir',
                    'a_obtenu.note as note',
                    ' Matiere.libelle as libelle',
                    'Classe.id_classe as classe']
        filtre = {"Eleve.id_eleve": "a_obtenu.id_eleve",
                  "_op1": "AND", "a_obtenu.id_matiere": "Matiere.id_matiere",
                  "_op2": "AND", "Classe.id_classe": "Eleve.id_classe",
                  "_op3": "AND", "a_obtenu.id_eleve": "'" + id_eleve + "'"}
        if id_matiere != "":
            filtre["_op4"]="AND"
            filtre["Matiere.id_matiere"]= "'" + str(id_matiere)  + "'"
        return self.bdd.afficher(table, colonnes, filtre)

    def ajouter(self, a_ajouter):
        table = "a_obtenu"
        return self.bdd.ajouter(table, a_ajouter)

    def supprimer(self, conditions):
        tables = ["a_obtenu", "Eleve"]
        conditions["_op0"] = "AND"
        conditions['a_obtenu.id_eleve'] = "Eleve.id_eleve"
        return self.bdd.supprimer_multitables(tables, conditions)

    def mettre_a_jour(self, a_modifier: dict, conditions : dict):
        table = "a_obtenu"
        return self.bdd.mettre_a_jour(table, a_modifier, conditions)

'''
if __name__ == '__main__':

    config = {
        'user': 'Marco',
        'password': 'Marco',
        'host': '127.0.0.1',
        'database': 'bddNotes',
        'use_pure': True
    }
    bdd_notes = bdd(config)

    #eleve_a_ajouter = {"id_eleve":"7546039557S","nom":"Lopez","prenom":"Abdul" }
    classe_a_ajouter = {"id_classe" : "TG2",
                        "niveau" : "Seconde",
                        "annee" : "2019",
                        "id_professeur" : "1314482981R"
                        }
    classe_a_modifier = {"niveau" : "Terminale"}
    condition = {"id_classe" : "TG2", "_op" : "AND", "annee" : "2019"}

    #print(bdd_notes.ajouter("Eleve", eleve_a_ajouter))
    # if bdd_notes.ajouter("Classe", classe_a_ajouter):
    #     print("Classe ajoutée")
    # else:
    #     print("Erreur lors de l'ajout de la classe")

    # count = bdd_notes.mettre_a_jour("Classe", classe_a_modifier, condition)
    # if count>-1:
    #     print(f"Table Classe modifiée : {count} ligne(s) affectée(s)")
    # else:
    #     print("Erreur lors de la modification de la classe")

    table = ["Eleve"]
    colonnes = ["id_eleve", "nom", "prenom"]
    #filtre = {"id_eleve":"1307661172D"}
    filtre = {}

    print(bdd_notes.afficher(table,colonnes,filtre))

    print("########################################")

    une_personne = personne("Laplouz", "Gaston")
    print(une_personne.get_nom(),une_personne.get_prenom())
    une_personne.set_nom("Lazare")
    une_personne.set_prenom("Garcin")
    print(une_personne.get_nom(),une_personne.get_prenom())

    un_eleve = eleve("Lazare", "Garcin", "1ZE34564334")
    print(un_eleve.get_prenom(),un_eleve.get_nom(), un_eleve.get_id())

    print("########################################")

    les_eleves = eleves(bdd_notes)
    print(les_eleves.liste())

    print("########################################")

    print(les_eleves.liste_classe("'1G2'"))

    print("########################################")

    les_profs = professeurs(bdd_notes)
    print(les_profs.liste())

    print("########################################")

    print(les_profs.liste_matiere("'SI'"))

    print("########################################")

    les_matieres = matieres(bdd_notes)
    print(les_matieres.liste())

    print("########################################")

    les_classes = classes(bdd_notes)
    print(les_classes.liste())

    bdd_notes.fermer()
'''



