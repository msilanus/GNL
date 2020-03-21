import sys
import time
import datetime
import libGestionNotes
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gestionNotesNSIGUI import Ui_Dialog


class ApplicationIHM(QDialog):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.id_professeur_selectionne = ""
        self.nouveau_devoir = False
        self.start = True
        self.ui.pbEnregistrerNotes.setEnabled(False)
        self.ui.pbAjouterDevoir.setEnabled(False)
        self.ui.pbSupprimerDevoir.setEnabled(False)
        self.niveaux = ["Tous", "Terminale", "Première", "Seconde"]
        labels_classes = ["Classe", "Niveau", "Professeur principal"]
        self.ui.twClasses.setHorizontalHeaderLabels(labels_classes)
        self.ui.twClasses.setColumnHidden(3, True)
        labels_professeurs = ["NUMEN", "Nom", "Prénom"]
        self.ui.twProfesseurs.setHorizontalHeaderLabels(labels_professeurs)
        labels_matieres = ["Libellé", "Description"]
        self.ui.twMatieres.setHorizontalHeaderLabels(labels_matieres)
        labels_eleves = ["INE", "Nom", "Prénom", "Classe"]
        self.ui.twAdministrationEleves.setHorizontalHeaderLabels(labels_eleves)
        labels_professeurs_notes = ["Elève", "Classe", "Matière", "Devoir", "Date", "Note"]
        self.ui.twProfesseurAfficherNotes.setHorizontalHeaderLabels(labels_professeurs_notes)
        self.ui.twProfesseurAfficherNotes.columnResized(1, self.ui.twProfesseurAfficherNotes.columnWidth(1),
                                                        self.ui.twProfesseurAfficherNotes.columnWidth(1) * 2)
        config = {
            'user': 'Marco',
            'password': 'Marco',
            'host': '127.0.0.1',
            'database': 'bddNotes',
            'use_pure': True
        }
        self.un_niveau = str(self.ui.cbFiltreNiveau.currentText())
        self.bdd_notes = libGestionNotes.bdd(config)
        self.les_classes = libGestionNotes.classes(self.bdd_notes)
        self.les_eleves = libGestionNotes.eleves(self.bdd_notes)
        self.les_professeurs = libGestionNotes.professeurs(self.bdd_notes)
        self.les_matieres = libGestionNotes.matieres(self.bdd_notes)
        self.les_notes = libGestionNotes.notes(self.bdd_notes)

        self.liste_des_professeurs = self.les_professeurs.liste()
        self.liste_des_classes = self.les_classes.liste_annee(time.strftime("%Y"))
        self.liste_des_matieres = self.les_matieres.liste()
        self.liste_des_devoirs = self.les_notes.liste_devoirs()
        self.liste_des_notes = self.les_notes.liste_notes()

        self.maj_cb_profs(self.ui.cbProfPrincipal)
        self.maj_cb_profs(self.ui.cbIdentificationProfesseur)
        self.maj_cb_profs(self.ui.cbAssociationProfesseur)
        self.maj_cb_classes(self.ui.cbAdministrationClasse)
        self.maj_cb_classes(self.ui.cbSelectionClasseProfesseur)
        self.maj_cb_classes(self.ui.cbSelectionClasseEleve)
        self.maj_cb_devoirs(self.ui.cbSelectionDevoirSupprimer)
        self.maj_cb_devoirs(self.ui.cbDevoirSelectionDevoirEnregistrerNotes)

        self.affiche_annees()
        self.affiche_niveaux()
        self.affiche_matieres()
        self.affiche_professeurs()
        self.liste_des_eleves = self.les_eleves.liste_annee(time.strftime("%Y"))
        self.affiche_eleves()
        self.affiche_notes()

    def on_close(self):
        print()
        print("#### Fermeture du logiciel ####")
        print()
        print("Fin de la connexion à la bdd")
        self.bdd_notes.fermer()

    def maj_cb_classes(self, combo):
        combo.clear()
        combo.addItem("")
        for classe in self.liste_des_classes:
            combo.addItem(classe['nom'])

    def maj_cb_profs(self, combo):
        combo.clear()
        combo.addItem("")
        for prof in self.liste_des_professeurs:
            combo.addItem(prof['prenom'] + " " + prof['nom'])

    def maj_cb_matieres(self, combo):
        combo.clear()
        combo.addItem("")
        for matiere in self.liste_des_matieres:
            combo.addItem(matiere['libelle'])

    def maj_cb_devoirs(self, combo):
        combo.clear()
        combo.addItem("")
        for devoir in self.liste_des_devoirs:
            combo.addItem(devoir['devoir'])

    def maj_cb_dates(self, combo):
        combo.clear()
        combo.addItem("")
        for date in self.liste_des_devoirs:
            combo.addItem(str(date['date(date)']))

    def maj_cb_eleves(self, combo):
        combo.clear()
        combo.addItem("")
        for eleve in self.liste_des_eleves:
            combo.addItem(eleve['nom_eleve'] + " " + eleve['prenom_eleve'])


    ############################################################################################
    #
    #  Gestion des classes : Onglet administration - Groupbox Classes
    #   - Combobox filtre Années
    #   - Combobox filtre Niveaux
    #   - TableWidget Classes en fonction des filtres
    #   - Gestion événement on_change_annee() : sélection d'une année dans le filtre
    #   - Gestion événement on_change_niveau() : sélection d'un niveau dans le filtre
    #   - Gestions événements click sur les boutons Ajouter / Supprimer / Modifier une classe
    #   - Gestion événement on_administration_selection_classe() : sélection d'une classe
    #                                                              dans le tableau
    #
    ############################################################################################

    def affiche_annees(self):
        print()
        print("#### affiche_annee() : Récurération des années dans la bdd ####")
        print()
        liste_des_annees = self.les_classes.liste_annees()
        print(liste_des_annees)
        self.ui.cbFiltreAnnee.clear()
        self.ui.cbFiltreAnnee.addItem("")
        for annee in liste_des_annees:
            self.ui.cbFiltreAnnee.addItem(str(annee['annee']))
        self.ui.cbFiltreAnnee.setCurrentIndex(1)
        return 0

    def affiche_niveaux(self):
        print()
        print("#### affiche_niveaux() : Remplissage de la liste box niveaux ####")
        print()

        self.ui.cbFiltreNiveau.clear()
        self.ui.cbFiltreNiveau.addItems(self.niveaux)
        self.ui.cbNiveau.addItems(self.niveaux)
        return 0

    def remplissage_twClasses(self):
        i = 0
        for ligne in self.liste_des_classes:
            # i = liste_des_classes.index(ligne)
            self.ui.twClasses.insertRow(i)
            self.ui.twClasses.setItem(i, 0, QTableWidgetItem(ligne['nom']))
            self.ui.twClasses.setItem(i, 1, QTableWidgetItem(ligne['niveau']))
            if ligne['id_professeur'] is not None:
                prof_principal = self.les_classes.prof_principal("'" + ligne['id_professeur'] + "'")
                self.ui.twClasses.setItem(i, 2, QTableWidgetItem(
                    prof_principal[0]['prenom'] + " " + prof_principal[0]['nom']))
            self.ui.twClasses.setItem(i, 3, QTableWidgetItem(ligne['id_classe']))
            i += 1

    def affiche_classes(self):
        print()
        print("#### affiche_classes() : Récurération des classes dans la bdd ####")
        print()

        self.nettoie_table_view(self.ui.twClasses)

        if self.un_niveau == "Tous":
            self.liste_des_classes = self.les_classes.liste_annee(self.annee)
            print(self.liste_des_classes)
            self.remplissage_twClasses()
        else:
            print(self.un_niveau)
            self.liste_des_classes = self.les_classes.liste_annee_niveau(self.annee, "'" + self.un_niveau + "'")
            print(self.liste_des_classes)
            self.remplissage_twClasses()
        return 0

    def on_change_annee(self, annee):
        print()
        print(f"#### on_change_annee() : Affichage des classe pour l'année {annee} ####")
        print()
        if annee != "":
            self.annee = annee
            self.affiche_classes()
            self.liste_des_eleves = self.les_eleves.liste_annee(annee)
            self.affiche_eleves()
        else:
            self.liste_des_eleves = self.les_eleves.liste_non_affectes()
            self.affiche_eleves()
        return 0

    def on_change_niveau(self, niveau):
        print()
        print(f"#### on_change_niveau() : Affichage des classe pour le niveau {niveau} ####")
        print()
        if niveau != "":
            self.un_niveau = niveau
            self.affiche_classes()
        return 0

    def pbSupprimerClasse_clicked(self):
        print()
        print("#### on_pbSupprimerClasse_clicked() : Suppression d'une classe ####")
        print()
        try:
            item = self.ui.twClasses.currentItem()
            id_classe = self.liste_des_classes[item.row()]['id_classe']
            print(f"Classe à supprimer : {id_classe}")
            if self.les_classes.supprimer("'" + id_classe + "'") == -1:
                print("Impossible de supprimer")
                self.message_erreur("Impossible de supprimer", "Cette classe contient encore des élèves<br>"
                                                               "Supprimez ou réaffectez tous ces élèves<br> "
                                                               "avant de la supprimer")

            self.affiche_annees()
            self.affiche_niveaux()
        except:
            print("Rien à supprimer")
            self.message_erreur("Rien à supprimer", "Sélectionner la classe à supprimer")

        return 0

    def pbAjouterClasse_clicked(self):
        print()
        print("#### on_pbAjouterClasse_clicked() : Ajout d'une classe ####")
        print()
        try:
            id_classe = self.ui.leClasse.text() + "_" + time.strftime("%y")
            print(f"Classe à ajouter : {id_classe}")
            print(f"Nouveau nom : {self.ui.leClasse.text()}")
            print(f"Nouveau niveau : {self.ui.cbNiveau.currentText()}")
            a_ajouter = {"id_classe": id_classe, "nom": self.ui.leClasse.text(), "annee": time.strftime("%Y"),
                         "niveau": self.ui.cbNiveau.currentText(), "id_professeur": 'NULL'}
            if self.ui.cbProfPrincipal.currentIndex() != 0:
                nom = self.ui.cbProfPrincipal.currentText().split(' ')[1]
                prenom = self.ui.cbProfPrincipal.currentText().split(' ')[0]
                print(f"Nouveau professeur principal : {nom} {prenom}")
                pp = self.les_professeurs.id_professeur(nom, prenom)
                print(f"id_professeur : {pp}")
                a_ajouter["id_professeur"] = pp
            self.les_classes.ajouter(a_ajouter)
            self.affiche_annees()
        except:
            self.message_erreur("Rien à ajouter", "Remplissez le champ Nom")
        return 0

    def pbModifierClasse_clicked(self):
        print()
        print("#### on_pbModifierClasse_clicked() : Modification d'une classe ####")
        print()
        try:
            item = self.ui.twClasses.currentItem()
            id_classe = self.liste_des_classes[item.row()]['id_classe']
            print(f"Classe à modifier : {id_classe}")
            print(f"Nouveau nom : {self.ui.leClasse.text()}")
            print(f"Nouveau niveau : {self.ui.cbNiveau.currentText()}")
            maj = {"nom": self.ui.leClasse.text(), "niveau": self.ui.cbNiveau.currentText(), "id_professeur": 'NULL'}
            if self.ui.cbProfPrincipal.currentIndex() != 0:
                nom = self.ui.cbProfPrincipal.currentText().split(' ')[1]
                prenom = self.ui.cbProfPrincipal.currentText().split(' ')[0]
                print(f"Nouveau professeur principal : {nom} {prenom}")
                pp = self.les_professeurs.id_professeur(nom, prenom)
                maj["id_professeur"] = pp
                print(f"id_professeur : {pp}")

            self.les_classes.mettre_a_jour(maj, id_classe)
            self.affiche_classes()
        except:
            print("Rien à modifier")
            self.message_erreur("Rien à modifier", "Sélectionner la classe à modifier")

        return 0

    def on_administration_selection_classe(self, item):
        print()
        print(
            f"#### on_administration_selection_classe() : Sélection d'une cellule du tableau des classes : {item.text()} ####")
        print()
        self.ui.twClasses.setRangeSelected(QTableWidgetSelectionRange(item.row(), 0, item.row(), 2), True)
        id_classe = self.liste_des_classes[item.row()]['id_classe']
        classe = self.liste_des_classes[item.row()]['nom']
        pp = self.liste_des_classes[item.row()]['id_professeur']
        niveau = self.liste_des_classes[item.row()]['niveau']

        print(f"id_classe : {id_classe}")
        print(f"Classe : {classe}")
        print(f"prof principal : {pp}")
        print(f"Niveau : {niveau}")

        self.liste_des_eleves = self.les_eleves.liste_classe(id_classe)
        self.affiche_eleves()
        self.ui.leClasse.setText(classe)
        index = self.ui.cbNiveau.findText(niveau)
        self.ui.cbNiveau.setCurrentIndex(index)
        pp = self.ui.twClasses.item(item.row(), 2)
        if pp is not None:
            index = self.ui.cbProfPrincipal.findText(pp.text())
            self.ui.cbProfPrincipal.setCurrentIndex(index)
        else:
            self.ui.cbProfPrincipal.setCurrentIndex(0)

        return 0

    ############################################################################################
    #
    #  Gestion des matières : Onglet administration - Groupbox Matières
    #   - TableWidget Matières : affichage des matières présentes dans la bdd
    #   - Gestions événements click sur les boutons Ajouter / Supprimer / Modifier une matière
    #   - Gestion événement on_administration_selection_Matiere() : sélection d'une matiere
    #                                                              dans le tableau
    #
    ############################################################################################

    def affiche_matieres(self):
        print()
        print("#### affiche_matieres() : Récurération des matieres dans la bdd ####")
        print()

        self.nettoie_table_view(self.ui.twMatieres)

        self.liste_des_matieres = self.les_matieres.liste()
        print(self.liste_des_matieres)
        i = 0

        for ligne in self.liste_des_matieres:
            libelle = QTableWidgetItem(ligne['libelle'])
            description = QTableWidgetItem(ligne['description'])
            self.ui.twMatieres.insertRow(i)
            self.ui.twMatieres.setItem(i, 0, libelle)
            self.ui.twMatieres.setItem(i, 1, description)
            i += 1
        return 0

    def on_administration_selection_matiere(self, item):
        print()
        print(f"#### on_administration_selection_matiere() : "
              f"Sélection d'une cellule du tableau des matières : {item.text()} ####")
        print()
        self.ui.twMatieres.setRangeSelected(QTableWidgetSelectionRange(item.row(), 0, item.row(), 1), True)
        self.ui.leLibelleMatiere.setText(self.ui.twMatieres.item(item.row(), 0).text())
        self.ui.leDescriptionMatiere.setText(self.ui.twMatieres.item(item.row(), 1).text())

        return 0

    def pbAjouterMatiere_clicked(self):
        print()
        print("#### pbAjouterMatiere_clicked() : Ajouter une matière ####")
        print()
        libelle = self.ui.leLibelleMatiere.text()
        description = self.ui.leDescriptionMatiere.text()
        try:
            print(f"Matière à ajouter : {libelle}")
            print(f"Description : {description}")
            if libelle != "":
                a_ajouter = {"id_matiere": "NULL", "libelle": libelle, "description": description}
            self.les_matieres.ajouter(a_ajouter)
            self.affiche_matieres()
        except:
            print("Rien à ajouter")
            self.message_erreur("Rien à ajouter", "Remplissez le champ Libellé")
        return 0

    def pbSupprimerMatiere_clicked(self):
        print()
        print("#### pbSupprimerMatiere_clicked() : Suppression d'uune matière ####")
        print()
        try:
            item = self.ui.twMatieres.currentItem()
            id_matiere = self.liste_des_matieres[item.row()]['id_matiere']

            print(f"Matière à supprimer : {id_matiere}")
            self.les_matieres.supprimer("'" + str(id_matiere) + "'")
            self.affiche_matieres()
        except:
            print("Rien à supprimer")
            self.message_erreur("Rien à supprimer", "Sélectionner la matière à supprimer")
        return 0

    def pbModifierMatiere_clicked(self):
        print()
        print("#### pbModifierMatiere_clicked() : Modifier une matière ####")
        print()
        try:
            item = self.ui.twMatieres.currentItem()
            id_matiere = str(self.liste_des_matieres[item.row()]['id_matiere'])
            libelle = self.ui.leLibelleMatiere.text()
            description = self.ui.leDescriptionMatiere.text()
            print(f"Matiere à modifier : {id_matiere}")
            print(f"Nouveau libelle : {libelle}")
            print(f"Nouvelle description : {description}")
            maj = {"libelle": libelle, "description": description}
            self.les_matieres.mettre_a_jour(maj, id_matiere)
            self.affiche_matieres()
        except:
            print("Rien à modifier")
            self.message_erreur("Rien à modifier", "Sélectionner la matière à modifier")
        return 0

    ############################################################################################
    #
    #  Gestion des professeurs : Onglet administration - Groupbox Professeurs
    #   - TableWidget Professeurs : affichage des professeurs présents dans la bdd
    #   - Gestions événements click sur les boutons Ajouter / Supprimer / Modifier un professeur
    #   - Gestion événement on_administration_selection_professeur() : sélection d'un professeur
    #                                                              dans le tableau
    #
    ############################################################################################

    def affiche_professeurs(self):
        print()
        print("#### affiche_professeurs() : Récurération des professeurs dans la bdd ####")
        print()

        self.nettoie_table_view(self.ui.twProfesseurs)

        self.liste_des_professeurs = self.les_professeurs.liste()
        print(self.liste_des_professeurs)
        i = 0
        for ligne in self.liste_des_professeurs:
            # i = liste_des_classes.index(ligne)
            self.ui.twProfesseurs.insertRow(i)
            self.ui.twProfesseurs.setItem(i, 0, QTableWidgetItem(ligne['id_professeur']))
            self.ui.twProfesseurs.setItem(i, 1, QTableWidgetItem(ligne['nom']))
            self.ui.twProfesseurs.setItem(i, 2, QTableWidgetItem(ligne['prenom']))
            i += 1
        return 0

    def on_administration_selection_professeur(self, item):
        print()
        print(
            f"#### on_administration_selection_professeur() : Sélection d'une cellule du tableau des professeurs : {item.text()} ####")
        print()
        self.ui.twProfesseurs.setRangeSelected(QTableWidgetSelectionRange(item.row(), 0, item.row(), 2), True)
        self.ui.leIdProfesseur.setText(self.ui.twProfesseurs.item(item.row(), 0).text())
        self.ui.leNomProfesseur.setText(self.ui.twProfesseurs.item(item.row(), 1).text())
        self.ui.lePrenomProfesseur.setText(self.ui.twProfesseurs.item(item.row(), 2).text())
        return 0

    def pbAjouterProfesseur_clicked(self):
        print()
        print("#### pbAjouterProfesseur_clicked() : Ajouter un professeur ####")
        print()
        id_professeur = self.ui.leIdProfesseur.text()
        nom = self.ui.leNomProfesseur.text().replace(" ", "-").upper()
        prenom = self.ui.lePrenomProfesseur.text().replace(" ", "-")
        titre = "Rien à ajouter"
        information = "Remplissez le champ Nom"
        good_numen = True
        try:
            print(f"Nom : {id_professeur}")
            print(f"Nom : {nom}")
            print(f"Prénom : {prenom}")
            if len(id_professeur) != 13:
                titre = "NUMEN non conforme"
                information = "Le Numen doit comporter 13 caractères<br>Exemple : 01 E 95 01234ABC<br>" \
                              "<a href='https://fr.wikipedia.org/wiki/" \
                              "Num%C3%A9ro_d%27identification_%C3%A9ducation_nationale'>Définition du NUMEN</href> "
                good_numen = False
            if nom != "" and good_numen:
                a_ajouter = {"id_professeur": id_professeur, "nom": nom, "prenom": prenom}
            self.les_professeurs.ajouter(a_ajouter)
            self.affiche_professeurs()
        except:
            print("Rien à ajouter")
            self.message_erreur(titre, information)
        return 0

    def pbSupprimerProfesseur_clicked(self):
        print()
        print("#### pbSupprimerProfesseur_clicked() : Suppression d'un professeur ####")
        print()
        try:
            item = self.ui.twProfesseurs.currentItem()
            id_professeur = self.liste_des_professeurs[item.row()]['id_professeur']
            nom = self.liste_des_professeurs[item.row()]['nom']
            prenom = self.liste_des_professeurs[item.row()]['prenom']
            print(f"Professeur à supprimer : {id_professeur}")
            print(f"Nom : {nom}")
            print(f"Prénom : {prenom}")

            if self.les_professeurs.supprimer("'" + str(id_professeur) + "'") == -1:
                print("Impossible de supprimer")
                self.message_erreur("Impossible de supprimer",
                                    "Ce professeur est professeur principal<br> ou a saisi des notes !<br>"
                                    "Supprimer toutes références à ce professeur<br> "
                                    "avant de le supprimer")
            else:
                self.affiche_professeurs()
        except:
            print("Rien à supprimer")
            self.message_erreur("Rien à supprimer", "Sélectionner le professeur à supprimer")
        return 0

    def pbModifierProfesseur_clicked(self):
        print()
        print("#### pbModifierProfesseur_clicked() : Modifier un professeur ####")
        print()
        try:
            item = self.ui.twProfesseurs.currentItem()
            id_professeur = self.liste_des_professeurs[item.row()]['id_professeur']
            if id_professeur == self.ui.leIdProfesseur.text():
                nom = self.ui.leNomProfesseur.text().replace(" ", "-").upper()
                prenom = self.ui.lePrenomProfesseur.text().replace(" ", "-")
                print(f"Professeur à modifier : {id_professeur}")
                print(f"Nom : {nom}")
                print(f"Prénom : {prenom}")
                maj = {"nom": nom, "prenom": prenom}
                self.les_professeurs.mettre_a_jour(maj, id_professeur)
                self.affiche_professeurs()
                self.affiche_classes()
            else:
                print("IMPOSSIBLE ! Le NUMEN ne peut pas être modifié. Supprimez le professeur et recréez le.")
                self.message_erreur("IMPOSSIBLE !",
                                    "Le NUMEN ne peut pas être modifié.<br><b> Supprimez le professeur et recréez le.</b>")
        except:
            print("Rien à modifier")
            self.message_erreur("Rien à modifier", "Sélectionnez le professeur à modifier")
        return 0

    ############################################################################################
    #
    #  Gestion des Eleves : Onglet administration - Groupbox Elèves
    #   - TableWidget Elèves : affichage des élèves présents dans la bdd
    #   - Gestions événements click sur les boutons Ajouter / Supprimer / Modifier un élève
    #   - Gestion événement on_administration_selection_eleve() : sélection d'un élève
    #                                                             dans le tableau
    #
    ############################################################################################

    def affiche_eleves(self):
        print()
        print("#### affiche_Eleves() : Récurération des élèves dans la bdd ####")
        print()

        self.nettoie_table_view(self.ui.twAdministrationEleves)

        print(self.liste_des_eleves)
        i = 0
        for ligne in self.liste_des_eleves:
            # i = liste_des_classes.index(ligne)
            self.ui.twAdministrationEleves.insertRow(i)
            self.ui.twAdministrationEleves.setItem(i, 0, QTableWidgetItem(ligne['id_eleve']))
            self.ui.twAdministrationEleves.setItem(i, 1, QTableWidgetItem(ligne['nom_eleve']))
            self.ui.twAdministrationEleves.setItem(i, 2, QTableWidgetItem(ligne['prenom_eleve']))
            try:
                self.ui.twAdministrationEleves.setItem(i, 3, QTableWidgetItem(ligne['nom']))
            except:
                pass
            i += 1
        return 0

    def on_administration_selection_eleve(self, item):
        print()
        print(
            f"#### on_administration_selection_eleve() : Sélection d'une cellule du tableau des élèves : {item.text()} ####")
        print()
        self.ui.twAdministrationEleves.setRangeSelected(QTableWidgetSelectionRange(item.row(), 0, item.row(), 3), True)
        self.ui.leIdEleve.setText(self.ui.twAdministrationEleves.item(item.row(), 0).text())
        self.ui.leNomEleve.setText(self.ui.twAdministrationEleves.item(item.row(), 1).text())
        self.ui.lePrenomEleve.setText(self.ui.twAdministrationEleves.item(item.row(), 2).text())
        try:
            index = self.ui.cbAdministrationClasse.findText(self.ui.twAdministrationEleves.item(item.row(), 3).text())
            self.ui.cbAdministrationClasse.setCurrentIndex(index)
        except:
            self.ui.cbAdministrationClasse.setCurrentIndex(0)

        return 0

    def pbAjouterEleve_clicked(self):
        print()
        print("#### pbAjouterEleve_clicked() : Ajouter un élève ####")
        print()
        id_eleve = self.ui.leIdEleve.text()
        nom = self.ui.leNomEleve.text().replace(" ", "-").upper()
        prenom = self.ui.lePrenomEleve.text().replace(" ", "-")
        classe = self.ui.cbAdministrationClasse.currentText()
        titre = "Rien à ajouter"
        information = "Remplissez le champ Nom"
        good_ine = True
        try:
            print(f"INE : {id_eleve}")
            print(f"Nom : {nom}")
            print(f"Prénom : {prenom}")
            print(f"Classe : {classe}")
            if len(id_eleve) != 11:
                titre = "INE non conforme"
                information = "Le INE doit comporter 11 caractères<br>Exemple : 012345678AZ<br>" \
                              "<a href='http://etudiant.aujourdhui.fr/etudiant/info/" \
                              "parcoursup-ou-trouver-son-numero-ine.html'>Définition du INE</href> "
                good_ine = False
            if nom != "" and good_ine:
                a_ajouter = {"id_eleve": id_eleve, "nom_eleve": nom, "prenom_eleve": prenom, "id_classe": 'NULL'}

            if self.ui.cbAdministrationClasse.currentIndex() != 0:
                classe = classe + "_" + time.strftime("%y")
                a_ajouter["id_classe"] = classe

            self.les_eleves.ajouter(a_ajouter)
            if self.ui.cbAdministrationClasse.currentIndex() == 0:
                self.liste_des_eleves = self.les_eleves.liste_non_affectes()
            else:
                self.liste_des_eleves = self.les_eleves.liste_classe(classe)
            self.affiche_eleves()
        except:
            print("Rien à ajouter")
            self.message_erreur(titre, information)
        return 0

    def pbSupprimerEleve_clicked(self):
        print()
        print("#### pbSupprimerEleve_clicked() : Suppression d'un élève ####")
        print()
        try:
            item = self.ui.twAdministrationEleves.currentItem()
            id_eleve = self.liste_des_eleves[item.row()]['id_eleve']
            nom = self.liste_des_eleves[item.row()]['nom_eleve']
            prenom = self.liste_des_eleves[item.row()]['prenom_eleve']
            print(f"Eleve à supprimer : {id_eleve}")
            print(f"Nom : {nom}")
            print(f"Prénom : {prenom}")

            if self.les_eleves.supprimer("'" + str(id_eleve) + "'") == -1:
                print("Impossible de supprimer")
                self.message_erreur("Impossible de supprimer",
                                    "Cet élève a encore des notes.<br>"
                                    "<b>Supprimer toutes références à cet élève "
                                    "avant de le supprimer</b>")
            else:
                if self.ui.cbFiltreAnnee.setCurrentIndex(0):
                    self.liste_des_eleves = self.les_eleves.liste_non_affectes()
                else:
                    self.liste_des_eleves = self.les_eleves.liste_annee(time.strftime("%Y"))
                self.affiche_eleves()
        except:
            print("Rien à supprimer")
            self.message_erreur("Rien à supprimer", "Sélectionner l'élève à supprimer")
        return 0

    def pbModifierEleve_clicked(self):
        print()
        print("#### pbModifierEleve_clicked() : Modifier un élève ####")
        print()
        try:
            item = self.ui.twAdministrationEleves.currentItem()
            id_eleve = self.liste_des_eleves[item.row()]['id_eleve']
            if id_eleve == self.ui.leIdEleve.text():
                nom = self.ui.leNomEleve.text().replace(" ", "-").upper()
                prenom = self.ui.lePrenomEleve.text().replace(" ", "-")
                classe = self.ui.cbAdministrationClasse.currentText()
                print(f"Elève à modifier : {id_eleve}")
                print(f"Nom : {nom}")
                print(f"Prénom : {prenom}")
                print(f"Classe : {classe}")
                maj = {"nom_eleve": nom, "prenom_eleve": prenom, "id_classe": 'NULL'}
                if self.ui.cbAdministrationClasse.currentIndex() != 0:
                    classe = classe + "_" + time.strftime("%y")
                    maj["id_classe"] = classe
                self.les_eleves.mettre_a_jour(maj, id_eleve)
                if self.ui.cbAdministrationClasse.currentIndex() == 0:
                    self.liste_des_eleves = self.les_eleves.liste_non_affectes()
                else:
                    self.liste_des_eleves = self.les_eleves.liste_classe(classe)
                self.affiche_eleves()
            else:
                print("IMPOSSIBLE ! Le INE ne peut pas être modifié. Supprimez l'élève et recréez le.")
                self.message_erreur("IMPOSSIBLE !",
                                    "Le INE ne peut pas être modifié.<br><b> Supprimez l'élève et recréez le.</b>")
        except:
            print("Rien à modifier")
            self.message_erreur("Rien à modifier", "Sélectionnez l'élève à modifier")

    def message_erreur(self, titre, information):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(information)
        msg.setWindowTitle(titre)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    ############################################################################################
    #
    #  Affichage des notes : Onglet Professeur - Groupbox Notes
    #   - TableWidget Notes : affichage des notes des élèves présents dans la bdd pour
    #                         professeur sélectionné
    #   - Gestions événements click sur les boutons Ajouter / Supprimer / Modifier une note
    #   - Gestion événement on_professeur_selection_note() : sélection d'une note dans le tableau
    #                       on_professeur_identification(QString) : Sélection professeur
    #
    ############################################################################################

    def affiche_notes(self):
        print()
        print(f"#### affiche_notes() : Affichage des notes du professeurs {self.id_professeur_selectionne} ####")
        print()

        self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)

        print(self.liste_des_notes)
        i = 0
        for ligne in self.liste_des_notes:
            # i = liste_des_notes.index(ligne)
            self.ui.twProfesseurAfficherNotes.insertRow(i)
            self.ui.twProfesseurAfficherNotes.setItem(i, 0, QTableWidgetItem(ligne['nom'] + " " + ligne['prenom']))
            self.ui.twProfesseurAfficherNotes.setItem(i, 1, QTableWidgetItem(ligne['classe']))
            self.ui.twProfesseurAfficherNotes.setItem(i, 2, QTableWidgetItem(ligne['libelle']))
            self.ui.twProfesseurAfficherNotes.setItem(i, 3, QTableWidgetItem(ligne['devoir']))
            self.ui.twProfesseurAfficherNotes.setItem(i, 4, QTableWidgetItem(str(ligne['date'])))
            self.ui.twProfesseurAfficherNotes.setItem(i, 5, QTableWidgetItem(str(ligne['note'])))
            i += 1
        self.ui.twProfesseurAfficherNotes.horizontalHeader().setSectionResizeMode(0)
        return 0

    def affiche_liste_eleves_sans_notes(self):
        print()
        print(
            "#### affiche_liste_eleves_sans_notes() : Affichage la liste des élèves pour entrer les notes d'un nouveau devoir ####")
        print()

        self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)

        print(self.liste_des_eleves)
        if len(self.liste_des_eleves) > 0:
            i = 0
            for ligne in self.liste_des_eleves:
                self.ui.twProfesseurAfficherNotes.insertRow(i)
                self.ui.twProfesseurAfficherNotes.setItem(i, 0, QTableWidgetItem(
                    ligne['nom_eleve'] + " " + ligne['prenom_eleve']))
                self.ui.twProfesseurAfficherNotes.setItem(i, 1, QTableWidgetItem(
                    self.ui.cbSelectionClasseProfesseur.currentText()))
                self.ui.twProfesseurAfficherNotes.setItem(i, 2, QTableWidgetItem(
                    self.ui.cbSelectionMatiereProfesseur.currentText()))
                self.ui.twProfesseurAfficherNotes.setItem(i, 3, QTableWidgetItem(
                    self.ui.cbDevoirSelectionDevoirEnregistrerNotes.currentText()))
                self.ui.twProfesseurAfficherNotes.setItem(i, 4, QTableWidgetItem(
                    str(datetime.datetime.now().isoformat(' ', 'seconds'))))
                self.ui.twProfesseurAfficherNotes.setItem(i, 5, QTableWidgetItem('None'))
                i += 1
            # self.ui.twProfesseurAfficherNotes.horizontalHeader().setSectionResizeMode(0)
            self.ui.pbEnregistrerNotes.setEnabled(True)

        return 0

    def nettoie_table_view(self, tw):
        # for i in range(tw.rowCount()):
        #     tw.removeRow(i)
        # tw.clearContents()
        tw.setRowCount(0)

    def on_professeur_identification(self, professeur):
        print()
        print("#### on_professeur_identification() : Professeur identification ####")
        print(f" - professeur sélectionné : {professeur}")

        if professeur != "":
            i = self.ui.cbIdentificationProfesseur.currentIndex() - 1
            self.id_professeur_selectionne = self.liste_des_professeurs[i]['id_professeur']
            print(f" - id_professeur : {self.id_professeur_selectionne}")
            print()

            self.liste_des_matieres = self.les_professeurs.liste_matieres(self.id_professeur_selectionne)
            if len(self.liste_des_matieres) == 0:
                print("Ce professeur n'enseigne aucune matière")
                self.ui.cbSelectionClasseProfesseur.setEnabled(False)
                self.ui.cbSelectionMatiereProfesseur.setEnabled(False)
                self.message_erreur("ATTENTION !",
                                    "Ce professeur n'enseigne aucune matière.<br><br><b>Veuillez l'associé à au moins une matière<b>")
                self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)

                return -1

            self.liste_des_notes = self.les_notes.liste_notes_professeur(self.id_professeur_selectionne)
            if len(self.liste_des_notes) > 0:
                self.affiche_notes()
            else:
                self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)

            self.ui.cbSelectionClasseProfesseur.setEnabled(True)
            self.ui.cbSelectionMatiereProfesseur.setEnabled(True)
            self.ui.cbSelectionClasseProfesseur.setCurrentIndex(0)
            self.ui.cbSelectionMatiereProfesseur.setCurrentIndex(0)
            self.ui.cbDevoirSelectionDevoirEnregistrerNotes.setEnabled(False)
            self.ui.pbAjouterDevoir.setEnabled(False)
            self.ui.pbSupprimerDevoir.setEnabled(False)
            self.ui.pbEnregistrerNotes.setEnabled(False)

            self.maj_cb_matieres(self.ui.cbSelectionMatiereProfesseur)

            self.liste_des_devoirs = self.les_notes.liste_devoirs_professeur(self.id_professeur_selectionne)
            self.maj_cb_devoirs(self.ui.cbSelectionDevoirSupprimer)
            self.maj_cb_devoirs(self.ui.cbDevoirSelectionDevoirEnregistrerNotes)
        else:
            self.ui.cbSelectionClasseProfesseur.setEnabled(False)
            self.ui.cbSelectionMatiereProfesseur.setEnabled(False)
            self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)

        return 0

    def on_ajouter_devoir_changed(self, devoir):
        print()
        print("#### on_ajouter_devoir_changed() : Devoir à ajouter ####")
        print(f" - Devoir sélectionné : {devoir}")
        print()
        if devoir != "":
            self.ui.pbAjouterDevoir.setEnabled(True)
        else:
            self.ui.pbAjouterDevoir.setEnabled(False)
        return 0

    def on_selection_devoir_changed(self, devoir):
        print()
        print("#### on_selection_devoir_changed() : Devoir à ajouter ####")
        print(f" - Devoir sélectionné : {self.ui.cbDevoirSelectionDevoirEnregistrerNotes.currentText()}")
        print(f' - Nouveau devoir : {self.nouveau_devoir}')
        print()
        if not self.nouveau_devoir:
            self.ui.pbAjouterDevoir.setEnabled(True)
            self.ui.pbAjouterDevoir.setEnabled(True)
            self.liste_des_notes = self.les_notes.liste_notes_professeur(self.id_professeur_selectionne,
                                                                         self.id_classe_selectionnee,
                                                                         self.ui.cbSelectionMatiereProfesseur.currentText(),
                                                                         self.ui.cbDevoirSelectionDevoirEnregistrerNotes.currentText())
            self.affiche_notes()
        else:
            self.affiche_liste_eleves_sans_notes()

        self.ui.pbAjouterDevoir.setEnabled(False)

        return 0

    def selection_classe_matiere(self, classe="", matiere=""):
        print()
        print("#### Gestion des notes :  ####")
        print(f" - classe  sélectionnée : {classe}")
        print(f" - matière sélectionnée : {matiere}")
        print()
        if classe != "":
            id_classe = self.id_classe_selectionnee
        else:
            id_classe = ""

        if matiere != "":
            id_matiere = self.id_matiere_selectionnee
        else:
            id_matiere = ""
        self.liste_des_devoirs = self.les_notes.liste_devoirs_professeur(self.id_professeur_selectionne, id_classe,
                                                                         id_matiere)
        self.maj_cb_devoirs(self.ui.cbSelectionDevoirSupprimer)
        self.maj_cb_devoirs(self.ui.cbDevoirSelectionDevoirEnregistrerNotes)

        self.liste_des_notes = self.les_notes.liste_notes_professeur(self.id_professeur_selectionne, id_classe, matiere)
        self.affiche_notes()

        if classe != "" and matiere != "":
            self.ui.leNouveauDevoir.setEnabled(True)
            self.ui.cbSelectionDevoirSupprimer.setEnabled(True)
            self.ui.pbEnregistrerNotes.setEnabled(True)
            self.ui.cbDevoirSelectionDevoirEnregistrerNotes.setEnabled(True)
        else:
            self.ui.leNouveauDevoir.setEnabled(False)
            self.ui.cbSelectionDevoirSupprimer.setEnabled(False)
            self.ui.pbEnregistrerNotes.setEnabled(False)
            self.ui.cbDevoirSelectionDevoirEnregistrerNotes.setEnabled(False)

        return 0

    def on_identification_classe_changed(self, classe):
        print()
        print("#### on_identification_classe_changed() : Choix d'une classe dans la gestion des notes ####")
        print(f" - classe sélectionnée : {classe}")
        self.id_classe_selectionnee = ""
        if classe != "":
            i = self.ui.cbSelectionClasseProfesseur.currentIndex() - 1
            self.id_classe_selectionnee = self.liste_des_classes[i]['id_classe']
            if i < 0: self.id_classe_selectionnee = ""
            print(f" - id_classe : {self.id_classe_selectionnee}")
            print()

            self.liste_des_eleves = self.les_eleves.liste_classe(self.id_classe_selectionnee)
            print(f" - nombre d'élèves trouvés : {len(self.liste_des_eleves)}")
            if len(self.liste_des_eleves) < 1:
                if not self.start:
                    self.message_erreur("ATTENTION !",
                                        "Cette classe est vide.<br><br>"
                                        "<b>Ajouter des élèves avant de leur donner des notes !</b>")
                    self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)
                    self.ui.pbEnregistrerNotes.setEnabled(False)
                    self.start = True
                    return -1

            matiere = self.ui.cbSelectionMatiereProfesseur.currentText()
            self.selection_classe_matiere(classe, matiere)
            self.start = False

        return 0

    def on_identification_matiere_changed(self, matiere):
        print()
        print("#### on_identification_matiere_changed() : Sélection d'une matière dans la gestion des notes ####")
        print(f" - matière sélectionnée : {matiere}")
        i = self.ui.cbSelectionMatiereProfesseur.currentIndex() - 1
        if i < 0: i = 0
        print(self.liste_des_matieres)
        print()
        self.id_matiere_selectionnee = self.liste_des_matieres[i]['id_matiere']
        print(f" - id_matiere : {self.id_matiere_selectionnee}")
        print(self.liste_des_matieres)

        classe = self.ui.cbSelectionClasseProfesseur.currentText()
        self.selection_classe_matiere(classe, matiere)

        return 0

    def on_supprimer_devoir_changed(self, devoir):
        print()
        print("#### on_supprimer_devoir_changed() : Devoir à supprimer sélectionné ####")
        print(f' - Devoir sélectionné : {devoir}')
        print()

        if devoir != "":
            self.ui.pbSupprimerDevoir.setEnabled(True)
            self.liste_des_notes = self.les_notes.liste_notes_professeur(self.id_professeur_selectionne,
                                                                         self.id_classe_selectionnee,
                                                                         self.ui.cbSelectionMatiereProfesseur.currentText(),
                                                                         self.ui.cbSelectionDevoirSupprimer.currentText())
            self.affiche_notes()
        else:
            self.ui.pbSupprimerDevoir.setEnabled(False)

        return 0

    def pbAjouterDevoir_clicked(self):
        print()
        print("#### pbAjouterDevoir_clicked() : Bouton Ajouter devoir cliqué ####")
        print()
        if self.ui.leNouveauDevoir.text() != "":
            self.nouveau_devoir = True
            a_ajouter = {'devoir': self.ui.leNouveauDevoir.text()}
            self.liste_des_devoirs.append(a_ajouter)
            print(f"Liste des devoirs disponibless : {self.liste_des_devoirs}")
            self.maj_cb_devoirs(self.ui.cbSelectionDevoirSupprimer)
            self.maj_cb_devoirs(self.ui.cbDevoirSelectionDevoirEnregistrerNotes)
            self.ui.cbDevoirSelectionDevoirEnregistrerNotes.setCurrentText(self.ui.leNouveauDevoir.text())

            return 0
        self.message_erreur("Création impossible !", "Votre nouveau devoir n'a pas de nom.<br><br>"
                                                     "<b>Vous devez donner un nom à votre devoir.</b>")
        return -1

    def pbSupprimerDevoir(self):
        print()
        print("#### pbSupprimerDevoir() : Bouton Supprimer devoir cliqué ####")
        print(f" - Devoir sélectionné : {self.ui.cbSelectionDevoirSupprimer.currentText()} ")
        print()

        conditions = {"a_obtenu.id_professeur": "'" + self.id_professeur_selectionne + "'",
                      "_op1": "AND",
                      "a_obtenu.id_matiere": "'" + str(self.id_matiere_selectionnee) + "'",
                      "_op2": "AND",
                      "Eleve.id_classe": "'" + self.id_classe_selectionnee + "'",
                      "_op3": "AND",
                      "devoir": "'" + self.ui.cbSelectionDevoirSupprimer.currentText() + "'"
                      }
        nb_supprimer = self.les_notes.supprimer(conditions)
        self.message_erreur("Devoir supprimer", str(nb_supprimer) + " notes ont été supprimées !")
        self.liste_des_notes = self.les_notes.liste_notes_professeur(self.id_professeur_selectionne,
                                                                     self.id_classe_selectionnee,
                                                                     str(self.id_matiere_selectionnee))
        self.affiche_notes()
        return 0

    def pbEnregistrerNotes_clicked(self):
        print()
        print("#### pbEnregistrerNotes_clicked() : Bouton Enregistrer notes cliqué ####")
        print()
        self.nouveau_devoir = False
        if self.ui.cbDevoirSelectionDevoirEnregistrerNotes.currentText() == "":
            self.message_erreur("ERREUR !", "<b>Sélectionnez un devoir pour <br>ajouter ou modifier des notes")
            return -1
        ajout = 0
        modifie =0
        for i in range(self.ui.twProfesseurAfficherNotes.rowCount()):
            if self.ui.twProfesseurAfficherNotes.item(i, 0) is not None:
                id_eleve = self.liste_des_eleves[i]['id_eleve']
                id_professeur = self.id_professeur_selectionne
                id_matiere = str(self.id_matiere_selectionnee)
                try:
                    note_str = self.ui.twProfesseurAfficherNotes.item(i, 5).text()
                    note_str = note_str.replace(",", ".")
                    note = float(note_str)
                    if note < 0 or note > 20:
                        self.message_erreur("Note non conforme",
                                            "Les notes doivent être comprisent entre 0 et 20 !")
                        return -1
                    note = str(note)
                except:
                    note = 'NULL'
                date = self.ui.twProfesseurAfficherNotes.item(i, 4).text()
                devoir = self.ui.cbDevoirSelectionDevoirEnregistrerNotes.currentText()

                a_ajouter = {"id_eleve": id_eleve,
                             "id_professeur": id_professeur,
                             "id_matiere": id_matiere,
                             "note": note,
                             "date": date,
                             "devoir": devoir}
                ok = self.les_notes.ajouter(a_ajouter)
                if ok==1:
                    ajout += ok
                    print(f"Ajout : {id_eleve} - "
                          f"{self.liste_des_eleves[i]['nom_eleve']} - "
                          f"{self.liste_des_eleves[i]['prenom_eleve']} - "
                          f"{self.id_classe_selectionnee} - "
                          f"id_matiere : {id_matiere} : "
                          f"{note}")
                else:
                    a_modifier = {"note": note}
                    conditions = {"id_professeur":id_professeur,
                                  "_op0": "AND",
                                  "id_eleve": id_eleve,
                                  "_op1": "AND",
                                  "id_matiere": id_matiere,
                                  "_op2": "AND",
                                  "devoir" : devoir,
                                  "_op3": "AND",
                                  "date": date}
                    ok = self.les_notes.mettre_a_jour(a_modifier,conditions)
                    if ok == 1:
                        modifie += ok
                        print(f"Ajout : {id_eleve} - "
                              f"{self.liste_des_eleves[i]['nom_eleve']} - "
                              f"{self.liste_des_eleves[i]['prenom_eleve']} - "
                              f"{self.id_classe_selectionnee} - "
                              f"id_matiere : {id_matiere} : "
                              f"{note} - "
                              f"{str(datetime.datetime.now().isoformat(' ', 'seconds'))}")

        print(f'Enregistrement de {ajout} notes')
        if ajout>0:
            self.message_erreur("Enregistrement", str(ajout) + " notes ont été enregistrées")
        if modifie>0:
            self.message_erreur("Mise à jour", str(modifie) + " notes ont été modifiées")

        self.liste_des_notes = self.les_notes.liste_notes_professeur(id_professeur,
                                                                     self.id_classe_selectionnee,
                                                                     self.ui.cbSelectionMatiereProfesseur.currentText(),
                                                                     devoir)
        self.affiche_notes()
        return 0

    ############################################################################################
    #
    #  Association professeurs/matières : Onglet Association - Groupbox gbEnseigne
    #
    #   Définition des enseignements assurés par les professeurs
    #   - Gestions événements click sur le bouton Enregistrer Met à jour la table Enseigne
    #   - Gestion événement on_association_identification(QString) : Sélection professeur
    #           - créer les cases à cocher des matières
    #           - lit la base pour cocher les cases si le professeur enseigne la matière
    #
    ############################################################################################

    def on_association_identification_changed(self, professeur):
        print()
        print(
            "#### on_association_identification_changed() : Sélection d'un professeur pour association avec les matières ####")
        print(f'  - professeur sélectionné : {professeur}')

        if professeur != "":
            i = self.ui.cbAssociationProfesseur.currentIndex()-1

            self.id_professeur_selectionne = self.liste_des_professeurs[i]['id_professeur']
            print(f" - id_professeur : {self.id_professeur_selectionne}")
            self.ui.lblNUMEN.setText(self.id_professeur_selectionne)

            print(f" - liste des matières : {self.liste_des_matieres}")
            self.clearLayout(self.ui.verticalLayout_21)

            hbox_pbEnregistrer = QHBoxLayout()
            hbox_pbEnregistrer.setObjectName("hbox_pbEnregistrer")
            SpacerItem_gauche = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            hbox_pbEnregistrer.addItem(SpacerItem_gauche)
            pbEnregistrerAssociations = QPushButton(self.ui.gbEnseigne)
            sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(pbEnregistrerAssociations.sizePolicy().hasHeightForWidth())
            pbEnregistrerAssociations.setSizePolicy(sizePolicy)
            pbEnregistrerAssociations.setMinimumSize(QSize(0, 0))
            pbEnregistrerAssociations.setObjectName("pbEnregistrerAssociations")
            hbox_pbEnregistrer.addWidget(pbEnregistrerAssociations)
            spacerItem1_droite = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            hbox_pbEnregistrer.addItem(spacerItem1_droite)
            hbox_pbEnregistrer.setStretch(0, 1)
            hbox_pbEnregistrer.setStretch(1, 3)
            hbox_pbEnregistrer.setStretch(2, 1)
            pbEnregistrerAssociations.setText("Enregistrer")

            pbEnregistrerAssociations.clicked.connect(self.pbEnregistrerAssociations)

            self.ui.verticalLayout_21.addLayout(hbox_pbEnregistrer)
            frame_pbEnregistrer = QFrame(self.ui.gbEnseigne)
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            frame_pbEnregistrer.setFont(font)
            frame_pbEnregistrer.setFrameShape(QFrame.StyledPanel)
            frame_pbEnregistrer.setFrameShadow(QFrame.Raised)
            frame_pbEnregistrer.setObjectName("frame_pbEnregistrer")
            vbox_all_frame = QVBoxLayout(frame_pbEnregistrer)
            vbox_all_frame.setObjectName("vbox_all_frame")
            hbox_select_all_description = QHBoxLayout()
            hbox_select_all_description.setObjectName("hbox_select_all_description")
            ckbToutSelectionner = QCheckBox(frame_pbEnregistrer)
            ckbToutSelectionner.setObjectName("ckbToutSelectionner")
            hbox_select_all_description.addWidget(ckbToutSelectionner)
            lblDescription = QLabel(frame_pbEnregistrer)
            lblDescription.setObjectName("lblDescription")
            hbox_select_all_description.addWidget(lblDescription)
            hbox_select_all_description.setStretch(0, 1)
            hbox_select_all_description.setStretch(1, 2)
            vbox_all_frame.addLayout(hbox_select_all_description)
            self.ui.verticalLayout_21.addWidget(frame_pbEnregistrer)
            ckbToutSelectionner.setText("Tout Sélectionner/Désélectionner")
            lblDescription.setText("Description")
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.lightGray)
            frame_pbEnregistrer.setAutoFillBackground(True)
            frame_pbEnregistrer.setPalette(p)

            ckbToutSelectionner.stateChanged.connect(self.ckbToutSelectionner_changed)

            self.liste_des_matieres_du_prof_selectionne = self.les_professeurs.liste_matieres(
                self.id_professeur_selectionne)
            print(f" - enseigne : {self.liste_des_matieres_du_prof_selectionne}")
            self.liste_ckbMatieres = []

            for i in range(len(self.liste_des_matieres)):
                matiere = {}
                matiere['id_matiere'] = self.liste_des_matieres[i]['id_matiere']
                matiere['libelle'] = self.liste_des_matieres[i]['libelle']

                hbox = QHBoxLayout()

                frame = QFrame(self.ui.gbEnseigne)
                frame.setFrameShape(QFrame.StyledPanel)
                frame.setFrameShadow(QFrame.Raised)

                vbox = QVBoxLayout(frame)

                checkbox = QCheckBox(frame)
                checkbox.setText(matiere['libelle'])
                if matiere in self.liste_des_matieres_du_prof_selectionne:
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
                checkbox.setVisible(True)
                name = "ckb_" + str(matiere['id_matiere'])
                checkbox.setObjectName(name)
                hbox.addWidget(checkbox)

                label_description = QLabel(frame)
                label_description.setText(self.liste_des_matieres[i]['description'])
                name = "lbl_" + str(matiere['id_matiere'])
                label_description.setObjectName(name)
                hbox.addWidget(label_description)

                hbox.setStretch(0, 1)
                hbox.setStretch(1, 2)

                vbox.addLayout(hbox)
                self.ui.verticalLayout_21.addWidget(frame)
                # self.ui.vbox_all_frame.addStretch()
                self.liste_ckbMatieres.append(checkbox)

                print(matiere, self.liste_des_matieres_du_prof_selectionne, " : ",
                      matiere in self.liste_des_matieres_du_prof_selectionne)
        else:
            self.ui.lblNUMEN.clear()

        return 0

    def ckbToutSelectionner_changed(self, state):
        print()
        print("#### ckbToutSelectionner_changed() : Tout sélectionner/désélectionner ####")
        print(f"  - Etat : {state}")
        print()

        for checkbox in self.liste_ckbMatieres:
            checkbox.setChecked(state)

        return 0

    def pbEnregistrerAssociations(self):
        print()
        print("#### pbEnregistrerAssociations() : Enregistrement des associaiton ####")
        print(f'  - professeur sélectionné : {self.id_professeur_selectionne}')
        print(f'  - matières sélectionnées : ')
        ajouter = 0
        supprimer = 0
        for i in range(len(self.liste_des_matieres)):
            if self.liste_ckbMatieres[i].isChecked():
                print(f"   - checkbox   : {self.liste_ckbMatieres[i].text()}")
                print(f"   - id_matiere : {self.liste_des_matieres[i]['id_matiere']}")
                print(f"   - libelle    : {self.liste_des_matieres[i]['libelle']}")
                if self.les_professeurs.ajouter_enseignement(self.id_professeur_selectionne,
                                                             self.liste_des_matieres[i]['id_matiere']) == 1:
                    ajouter += 1
                    print(f"   - {self.liste_des_matieres[i]['id_matiere']} a été ajouter à la table enseignement")
            else:
                if self.les_professeurs.supprimer_enseignement(self.id_professeur_selectionne,
                                                               self.liste_des_matieres[i]['id_matiere']) == 1:
                    supprimer += 1
                    print(f"   - {self.liste_des_matieres[i]['id_matiere']} a été supprimer de la table enseignement")

        print(f"{ajouter} enseignements ajoutés")
        print(f"{supprimer} enseignements supprimés")

        self.message_erreur("Information", str(ajouter) + " enseignements ajoutés<br>" +
                            str(supprimer) + " enseignements supprimés")

        return 0

    def clearLayout(self, layout):
        print()
        print("#### clearLayout() : Suppression de tous les widget du layout qui contient le choix des matières ####")
        print()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                print("widget" + str(item))
                item.widget().close()
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QSpacerItem):
                print("spacer " + str(item))
                # no need to do extra stuff
            else:
                print("layout " + str(item))
                self.clearLayout(item.layout())

            # remove the item from layout
            layout.removeItem(item)

        return 0

    ############################################################################################
    #
    #  Affichage des notes de l'élève : Onglet Elève - Groupbox gbNotesEleve
    #
    #   Affichage des notes de toutes les matières ou d'une seule matière
    #   - Gestion événement on_eleve_classe(QString) : Sélection d'une classe
    #   - Gestion événement on_eleve_identification(QString) : Sélection élève dans une classe
    #   - Gestion événement on_eleve_matiere(QString) : Sélection matiere dans une classe
    #
    ############################################################################################



    def on_eleve_classe(self, classe):
        print()
        print("#### on_eleve_classe() : Choix de la classe dans la vue élève ####")
        print(f" - Classe sélectionnée : {classe}")
        print()

        self.nettoie_table_view(self.ui.twEleveAfficherNotes)

        if classe != "":
            self.ui.cbIdentificationEleve.setEnabled(True)
            i = self.ui.cbSelectionClasseEleve.currentIndex() - 1
            self.id_classe_selectionnee = self.liste_des_classes[i]['id_classe']
            if i < 0: self.id_classe_selectionnee = ""
            print(f" - id_classe : {self.id_classe_selectionnee}")
            print()
            self.liste_des_eleves = self.les_eleves.liste_classe(self.id_classe_selectionnee)
            self.maj_cb_eleves(self.ui.cbIdentificationEleve)

        else:
            self.ui.cbIdentificationEleve.setCurrentIndex(0)
            self.ui.cbIdentificationEleve.setEnabled(False)
            self.ui.cbSelectionMatiereEleve.setCurrentIndex(0)
            self.ui.cbSelectionMatiereEleve.setEnabled(False)

        return 0

    def on_eleve_identification(self, eleve):
        print()
        print("#### on_eleve_identication() : Choix de l'élève dans la vue élève ####")
        print(f" - Elève sélectionné : {eleve}")
        print()

        if eleve != "":
            self.ui.cbSelectionMatiereEleve.setEnabled(True)
            i = self.ui.cbIdentificationEleve.currentIndex() - 1
            self.id_eleve_selectionnee = self.liste_des_eleves[i]['id_eleve']
            if i < 0: self.id_eleve_selectionnee = ""
            print(f" - id_eleve : {self.id_eleve_selectionnee}")
            print()
            self.liste_des_matieres = self.les_matieres.liste_classe(self.id_classe_selectionnee)
            self.maj_cb_matieres(self.ui.cbSelectionMatiereEleve)

            self.affiche_notes_eleve()
        else:
            self.ui.cbSelectionMatiereEleve.setCurrentIndex(0)
            self.ui.cbSelectionMatiereEleve.setEnabled(False)
            self.nettoie_table_view(self.ui.twEleveAfficherNotes)

        return 0

    def affiche_notes_eleve(self):
        self.nettoie_table_view(self.ui.twEleveAfficherNotes)
        labels = ["Matière", "Plus basse", "Moyenne classe", "Plus haute", "Moyenne élève"]
        self.ui.twEleveAfficherNotes.setHorizontalHeaderLabels(labels)
        i = 0
        for matiere in self.liste_des_matieres:
            moyenne_eleve = self.les_eleves.moyenne(self.id_eleve_selectionnee, matiere['id_matiere'])
            stat_matiere = self.les_matieres.statitiques(self.id_classe_selectionnee, matiere['id_matiere'])
            print(f"Moyenne : {moyenne_eleve['moyenne']}  Stat : {stat_matiere}")
            self.ui.twEleveAfficherNotes.insertRow(i)

            libelle = QTableWidgetItem(matiere['libelle'])
            min_classe = QTableWidgetItem(str(stat_matiere['min']))
            min_classe.setTextAlignment(Qt.AlignCenter)
            if stat_matiere['moyenne'] is None: moy_classe = QTableWidgetItem(" - ")
            else : moy_classe = QTableWidgetItem(str(round(stat_matiere['moyenne'], 2)))
            moy_classe.setTextAlignment(Qt.AlignCenter)
            max_classe = QTableWidgetItem(str(stat_matiere['max']))
            max_classe.setTextAlignment(Qt.AlignCenter)
            if moyenne_eleve['moyenne'] is None: moy_eleve = QTableWidgetItem(" - ")
            else : moy_eleve = QTableWidgetItem(str(round(moyenne_eleve['moyenne'], 2)))
            moy_eleve.setTextAlignment(Qt.AlignCenter)

            self.ui.twEleveAfficherNotes.setItem(i, 0, libelle)
            self.ui.twEleveAfficherNotes.setItem(i, 1, min_classe)
            self.ui.twEleveAfficherNotes.setItem(i, 2, moy_classe)
            self.ui.twEleveAfficherNotes.setItem(i, 3, max_classe)
            self.ui.twEleveAfficherNotes.setItem(i, 4, moy_eleve)
            i += 1

    def on_eleve_matiere(self, matiere):
        print()
        print("#### on_eleve_matiere() : Choix de la matière dans la vue élève ####")
        print(f" - Matière sélectionné : {matiere}")

        if matiere != "":
            i = self.ui.cbSelectionMatiereEleve.currentIndex() - 1

            id_matiere_selectionnee = self.liste_des_matieres[i]['id_matiere']
            if i < 0: self.id_matiere_selectionnee = ""
            print(f" - id_matiere : {id_matiere_selectionnee}")
            print()

            self.nettoie_table_view(self.ui.twEleveAfficherNotes)
            labels = ["Devoir", "Note la plus basse", "Moyenne classe", "Note la plus haute", "Note de l'élève"]
            self.ui.twEleveAfficherNotes.setHorizontalHeaderLabels(labels)

            les_devoirs = self.les_notes.devoirs_eleve(self.id_eleve_selectionnee, id_matiere_selectionnee)
            print(f"Devoirs : {les_devoirs}")

            i=0
            for devoir in les_devoirs:
                print(devoir['devoir'])
                stat_devoir = self.les_matieres.statitiques(self.id_classe_selectionnee, id_matiere_selectionnee, devoir['devoir'])
                print(f"Stat : {stat_devoir}")
                nom_devoir = QTableWidgetItem(devoir['devoir'])
                min_classe = QTableWidgetItem(str(stat_devoir['min']))
                min_classe.setTextAlignment(Qt.AlignCenter)
                if stat_devoir['moyenne'] is None : moy_classe = QTableWidgetItem(" - ")
                else: moy_classe = QTableWidgetItem(str(round(stat_devoir['moyenne'],2)))
                moy_classe.setTextAlignment(Qt.AlignCenter)
                max_classe = QTableWidgetItem(str(stat_devoir['max']))
                max_classe.setTextAlignment(Qt.AlignCenter)
                note_eleve = QTableWidgetItem(str(devoir['note']))
                note_eleve.setTextAlignment(Qt.AlignCenter)

                self.ui.twEleveAfficherNotes.insertRow(i)

                self.ui.twEleveAfficherNotes.setItem(i, 0, nom_devoir)
                self.ui.twEleveAfficherNotes.setItem(i, 1, min_classe)
                self.ui.twEleveAfficherNotes.setItem(i, 2, moy_classe)
                self.ui.twEleveAfficherNotes.setItem(i, 3, max_classe)
                self.ui.twEleveAfficherNotes.setItem(i, 4, note_eleve)
                i += 1
        else:
            self.affiche_notes_eleve()
        return 0

    def on_change_tab(self,tab):
        print()
        print("#### on_change_tab() : Changement d'onglet ####")
        print(f" - Onglet sélectionné : {tab}")

        self.liste_des_professeurs = self.les_professeurs.liste()
        self.liste_des_classes = self.les_classes.liste_annee(time.strftime("%Y"))
        self.liste_des_matieres = self.les_matieres.liste()
        self.liste_des_devoirs = self.les_notes.liste_devoirs()
        self.liste_des_notes = self.les_notes.liste_notes()

        self.maj_cb_profs(self.ui.cbProfPrincipal)
        self.maj_cb_profs(self.ui.cbIdentificationProfesseur)
        self.maj_cb_profs(self.ui.cbAssociationProfesseur)
        self.maj_cb_classes(self.ui.cbAdministrationClasse)
        self.maj_cb_classes(self.ui.cbSelectionClasseProfesseur)
        self.maj_cb_classes(self.ui.cbSelectionClasseEleve)
        self.maj_cb_devoirs(self.ui.cbSelectionDevoirSupprimer)
        self.maj_cb_devoirs(self.ui.cbDevoirSelectionDevoirEnregistrerNotes)

        if tab == 1:
            self.ui.cbIdentificationProfesseur.setCurrentIndex(0)
            self.ui.cbSelectionClasseProfesseur.setCurrentIndex(0)
            self.ui.cbSelectionMatiereProfesseur.setCurrentIndex(0)
            self.ui.leNouveauDevoir.clear()
            self.nettoie_table_view(self.ui.twProfesseurAfficherNotes)
            self.ui.pbEnregistrerNotes.setEnabled(False)


        if tab == 2:
            self.ui.cbAssociationProfesseur.setCurrentIndex(0)
            self.clearLayout(self.ui.verticalLayout_21)

        if tab == 3:
            self.on_eleve_classe(self.ui.cbIdentificationEleve.currentText())

def main():
    app = QApplication(sys.argv)
    application = ApplicationIHM()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
