import json
import os
from datetime import date
class Vehicule:
    def __init__(self, id, marque, modele, immatriculation, tarif_jour):
        self.id = id
        self.marque = marque
        self.modele = modele
        self.immatriculation = immatriculation
        self._tarif_jour = 0
        self._etat = "disponible"
        self.changer_tarif(tarif_jour)

    def to_dict(self):
        return {
            "id": self.id,
            "marque": self.marque,
            "modele": self.modele,
            "immatriculation": self.immatriculation,
            "tarif_jour": self._tarif_jour,
            "etat": self._etat,
        }

    @staticmethod
    def from_dict(d):
        if d["type"] == "voiture":
            v= Voiture(d["id"], d["marque"], d["modele"],
                       d["immatriculation"], d["tarif_jour"], d["nb_portes"])
        elif d["type"] == "moto":
            v= Moto(d["id"], d["marque"], d["modele"], d["immatriculation"],
                    d["tarif_jour"], d["cylindree"])
        else:
            raise ValueError("Type de vehicule invalide")
        v.changer_etat(d["etat"])
        return v

    def changer_tarif(self, valeur):
        if valeur <= 0:
            raise ValueError("Le tarif doit etre positif")
        self._tarif_jour = valeur

    def obtenir_tarif(self):
        return self._tarif_jour

    def obtenir_etat(self):
        return self._etat

    def changer_etat(self, nouvel_etat):
        nouvel_etat = nouvel_etat.lower()
        if nouvel_etat not in("disponible", "loue","maintenance"):
            raise ValueError("Etat invalide")
        self._etat = nouvel_etat

    def calculer_cout(self,nb_jours ):
        return self._tarif_jour * nb_jours


class Voiture(Vehicule):
    def __init__(self, id, marque, modele, immatriculation, tarif_jour, nb_portes):
        super().__init__(id, marque, modele, immatriculation, tarif_jour)
        self.nb_portes = nb_portes
    def calculer_cout(self,nb_jours ):
        base= super().calculer_cout(nb_jours)
        return base + 5 * nb_jours

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "voiture"
        data["nb_portes"] = self.nb_portes
        return data


class Moto(Vehicule):
    def __init__(self, id, marque, modele, immatriculation, tarif_jour, cylindree):
        super().__init__(id, marque, modele, immatriculation, tarif_jour)
        self.cylindree = cylindree
    def calculer_cout(self,nb_jours ):
        base = super().calculer_cout(nb_jours)
        if nb_jours > 3:
            base = base * 0.9
        return base

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "moto"
        data["cylindree"] = self.cylindree
        return data


class Client:
    def __init__(self, id, nom, telephone, numero_permis):
        if not nom.strip():
            raise ValueError("Nom vide")
        self.id = id
        self.nom = nom
        self.telephone = telephone
        self.numero_permis = numero_permis

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "telephone": self.telephone,
            "numero_permis": self.numero_permis,
        }
    @staticmethod
    def from_dict(d):
        return Client(d["id"], d["nom"], d["telephone"], d["numero_permis"])

class Maintenance:
    def __init__(self, id, vehicule_id, date_debut, date_fin):
        if date_fin < date_debut:
            raise ValueError("La date de fin precede la date de debut")
        self.id = id
        self.vehicule_id = vehicule_id
        self.date_debut = date_debut
        self.date_fin = date_fin

    def to_dict(self):
        return {
            "id": self.id,
            "vehicule_id": self.vehicule_id,
            "date_debut": self.date_debut.isoformat(),
            "date_fin" : self.date_fin.isoformat(),
        }

    @staticmethod
    def from_dict(d):
        return Maintenance(
            d["id"],
            d["vehicule_id"],
            date.fromisoformat(d["date_debut"]),
            date.fromisoformat(d["date_fin"]),
        )

class Reservation:
    STATUTS = ("confirmee", "en cours", "terminee", "annulee")
    def __init__(self, id, client_id, vehicule_id, date_debut, date_fin, montant):
        if date_fin < date_debut:
            raise ValueError("La date de fin precede la date de debut")
        self.id = id
        self.client_id = client_id
        self.vehicule_id = vehicule_id
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.montant = montant
        self._statut = "confirmee"
        self.montant_rembourse = 0
        self.date_retour=None
        self.frais_retard= 0
        self.montant_final= None

    def to_dict(self):
        if self.date_retour is None :
            retour = None
        else:
            retour = self.date_retour.isoformat()
        return{
            "id": self.id,
            "client_id": self.client_id,
            "vehicule_id": self.vehicule_id,
            "date_debut": self.date_debut.isoformat(),
            "date_fin": self.date_fin.isoformat(),
            "montant": self.montant,
            "statut": self._statut,
            "montant_rembourse": self.montant_rembourse,
            "date_retour": retour,
            "frais_retard": self.frais_retard,
            "montant_final": self.montant_final,
        }

    @staticmethod
    def from_dict(d):
        r = Reservation(d["id"], d["client_id"], d["vehicule_id"],
                        date.fromisoformat(d["date_debut"]), date.fromisoformat(d["date_fin"]),d["montant"])
        r.changer_statut(d["statut"])
        r.montant_rembourse = d["montant_rembourse"]
        if d["date_retour"] is not None:
            r.date_retour = date.fromisoformat(d["date_retour"])
        r.frais_retard = d["frais_retard"]
        r.montant_final = d["montant_final"]
        return r

    def changer_statut(self, nouveau_statut):
        if nouveau_statut not in self.STATUTS:
            raise ValueError("Statut invalide")
        self._statut = nouveau_statut

    def nb_jours(self):
        return (self.date_fin - self.date_debut).days

def tarif_du_vehicule(v):
    return v.obtenir_tarif()

class Agence:
    def __init__(self):
        self.vehicules = []
        self.clients = []
        self.reservations = []
        self.maintenances = []
        self.prochain_id_client = 1
        self.prochain_id_vehicule = 1
        self.prochain_id_reservation = 1
        self.prochain_id_maintenance = 1

    def to_dict(self):
        fiche_clients = []
        for c in self.clients:
            fiche_clients.append(c.to_dict())
        fiche_vehicules = []
        for v in self.vehicules:
            fiche_vehicules.append(v.to_dict())
        fiches_reservations = []
        for r in self.reservations:
            fiches_reservations.append(r.to_dict())
        fiches_maintenances = []
        for m in self.maintenances:
            fiches_maintenances.append(m.to_dict())
        return {
            "clients": fiche_clients,
            "vehicules": fiche_vehicules,
            "reservations": fiches_reservations,
            "maintenances": fiches_maintenances,
            "prochain_id_client": self.prochain_id_client,
            "prochain_id_vehicule": self.prochain_id_vehicule,
            "prochain_id_reservation": self.prochain_id_reservation,
            "prochain_id_maintenance": self.prochain_id_maintenance,

        }

    def sauvegarder(self, nom_fichier="agence.json"):
        with open(nom_fichier, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)

    def charger(self, nom_fichier="agence.json"):
        if not os.path.exists(nom_fichier):
            return False
        try:
            with open(nom_fichier, "r", encoding="utf-8") as f:
                d = json.load(f)
            clients = []
            for fiche in d["clients"]:
                clients.append(Client.from_dict(fiche))
            vehicules = []
            for fiche in d["vehicules"]:
                vehicules.append(Vehicule.from_dict(fiche))
            reservations = []
            for fiche in d["reservations"]:
                reservations.append(Reservation.from_dict(fiche))
            maintenances = []
            for fiche in d["maintenances"]:
                maintenances.append(Maintenance.from_dict(fiche))
            id_client = d["prochain_id_client"]
            id_vehicule = d["prochain_id_vehicule"]
            id_reservation = d["prochain_id_reservation"]
            id_maintenance = d["prochain_id_maintenance"]
        except (KeyError, TypeError, ValueError):
            raise ValueError("Fichier JSON invalide")

        self.clients = clients
        self.vehicules = vehicules
        self.reservations = reservations
        self.maintenances = maintenances
        self.prochain_id_client = id_client
        self.prochain_id_vehicule = id_vehicule
        self.prochain_id_reservation = id_reservation
        self.prochain_id_maintenance = id_maintenance
        return True

    def compter_par_statut(self):
        compte = {}
        for r in self.reservations:
            if r._statut in compte:
                compte[r._statut] += 1
            else:
                compte[r._statut] = 1
        return compte

    def calculer_revenus(self):
        total = 0
        for r in self.reservations:
            if r.montant_final is not None :
                total += r.montant_final
        return total

    def compter_locations_par_vehicule(self):
        compte = {}
        for r in self.reservations:
            if r._statut != "annulee":
                if r.vehicule_id in compte:
                    compte[r.vehicule_id] +=1
                else:
                    compte[r.vehicule_id] = 1
        return compte

    def vehicule_le_plus_loue(self):
        compte = self.compter_locations_par_vehicule()
        meilleur_id = None
        meilleur_total = 0
        for vehicule_id in compte :
            if compte[vehicule_id] > meilleur_total:
                meilleur_total = compte[vehicule_id]
                meilleur_id = vehicule_id
        return meilleur_id

    def ajouter_client(self, client):
        self.clients.append(client)

    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)

    def nouveau_id_client(self):
        id_donne = self.prochain_id_client
        self.prochain_id_client += 1
        return id_donne

    def nouveau_id_vehicule(self):
        id_vehicule = self.prochain_id_vehicule
        self.prochain_id_vehicule += 1
        return id_vehicule

    def nouveau_id_reservation(self):
        id_reservation = self.prochain_id_reservation
        self.prochain_id_reservation += 1
        return id_reservation

    def nouveau_id_maintenance(self):
        id_maintenance = self.prochain_id_maintenance
        self.prochain_id_maintenance += 1
        return id_maintenance

    def rechercher_par_marque(self, marque):
        resultat=[]
        for v in self.vehicules:
            if v.marque.lower() == marque.lower():
                resultat.append(v)
        return resultat

    def trier_par_tarif(self):
        return sorted(self.vehicules, key=tarif_du_vehicule)

    def trouver_vehicule(self, vehicule_id):
        for v in self.vehicules:
            if v.id == vehicule_id:
                return v
        return None

    def trouver_client(self, client_id):
        for c in self.clients:
            if c.id == client_id:
                return c
        return None

    def trouver_reservation(self, reservation_id):
        for r in self.reservations:
            if r.id == reservation_id:
                return r
        return None


    def est_disponible(self, vehicule_id, debut,fin):
        for r in self.reservations:
            if r.vehicule_id == vehicule_id and r._statut != "annulee" :
                if debut < r.date_fin and r.date_debut < fin:
                    return False
        for m in self.maintenances:
            if m.vehicule_id == vehicule_id :
                if debut < m.date_fin and m.date_debut < fin:
                    return False
        return True

    def reserver(self, client_id, vehicule_id, debut, fin):
        client = self.trouver_client(client_id)
        if client is None:
            raise ValueError("Client introuvable")
        vehicule = self.trouver_vehicule(vehicule_id)
        if vehicule is None:
            raise ValueError("Vehicule introuvable")
        if fin <= debut :
            raise ValueError("La location doit durer au moins 1 jour")
        if not self.est_disponible(vehicule_id, debut, fin):
            raise ValueError("Vehicule non disponible sur cette periode")

        nb_jours = (fin-debut).days
        montant = vehicule.calculer_cout(nb_jours)
        reservation = Reservation(self.nouveau_id_reservation(), client_id, vehicule_id, debut, fin, montant)
        self.reservations.append(reservation)
        return reservation

    def annuler(self, reservation_id, aujourdhui):
        reservation = self.trouver_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation introuvable")
        if reservation._statut != "confirmee":
            raise ValueError("Seule une reservation confirmee peut etre annulee")
        if (reservation.date_debut - aujourdhui).days >=2 :
            remboursement = reservation.montant
        else:
            remboursement = 0
        reservation.changer_statut("annulee")
        reservation.montant_rembourse = remboursement
        return remboursement

    def enregistrer_depart(self, reservation_id):
        reservation = self.trouver_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation introuvable")
        if reservation._statut != "confirmee":
            raise ValueError("Le depart n'est possible que pour une reservation confirmee")
        vehicule = self.trouver_vehicule(reservation.vehicule_id)
        if vehicule.obtenir_etat() != "disponible":
            raise ValueError("Le vehicule n'est pas disponible pour le depart")
        reservation.changer_statut("en cours")
        vehicule.changer_etat("loue")

    def enregistrer_retour(self, reservation_id, date_retour):
        reservation = self.trouver_reservation(reservation_id)
        if reservation is None:
            raise ValueError("Reservation introuvable")
        if reservation._statut != "en cours":
            raise ValueError("Seule une location en cours peut etre rendue")
        if date_retour < reservation.date_debut :
            raise ValueError("la date de retour precede la date de depart")

        vehicule= self.trouver_vehicule(reservation.vehicule_id)
        montant_final = reservation.montant
        frais_retard = 0
        if date_retour > reservation.date_fin:
            jours_retard = (date_retour - reservation.date_fin).days
            frais_retard = jours_retard *vehicule.obtenir_tarif()*2
            montant_final= reservation.montant + frais_retard
        elif date_retour < reservation.date_fin:
            jours_utilises = (date_retour - reservation.date_debut).days
            if jours_utilises < 1:
                jours_utilises = 1
            montant_final = vehicule.calculer_cout(jours_utilises)

        reservation.date_retour = date_retour
        reservation.frais_retard = frais_retard
        reservation.montant_final = montant_final
        reservation.changer_statut("terminee")
        vehicule.changer_etat("disponible")
        return montant_final

    def planifier_maintenance(self, vehicule_id, debut, fin):
        vehicule = self.trouver_vehicule(vehicule_id)
        if vehicule is None:
            raise ValueError("Vehicule introuvable")
        if fin <= debut:
            raise ValueError("la maintenance doit durer au moins 1 jour")
        if not self.est_disponible(vehicule_id, debut, fin):
            raise ValueError("Vehicule non disponible sur cette periode")
        maintenance = Maintenance(self.nouveau_id_maintenance(), vehicule_id, debut, fin)
        self.maintenances.append(maintenance)
        return maintenance

def saisir_client(agence):
    nom = input("Nom du client: ")
    if nom.strip() == "":
        print("Le nom ne peut pas etre vide")
        return
    telephone = input("Entrez votre numero de telephone: ")
    permis = input("Entrez votre numero de permis: ")
    client = Client(agence.nouveau_id_client(), nom, telephone, permis)
    agence.ajouter_client(client)
    print("Client ajoute , numero",client.id)

def saisir_vehicule(agence):
    type_v = input("type (1 = Voiture, 2= Moto) :")
    if type_v != "1" and type_v != "2":
        print("Type invalide")
        return
    marque = input("Entrez la Marque: ")
    modele = input("Entrez le modele: ")
    immat = input("Entrez l'immatriculation: ")
    try :
        tarif = float(input("Tarif par Jour: "))
        if type_v == "1":
            nb_portes = int(input("Nombre de portes: "))
            v = Voiture(agence.nouveau_id_vehicule(),marque, modele, immat, tarif, nb_portes)
        else:
            cylindree = int (input("Cylindre: "))
            v = Moto(agence.nouveau_id_vehicule(), marque, modele, immat, tarif, cylindree)
    except ValueError:
        print("Valeur invalide, vehicule non ajoute")
        return
    agence.ajouter_vehicule(v)
    print("Vehicule ajoute , numero",v.id)


def afficher_menu():
    print("=== Agence de location ===")
    print("1. Reservation par statut")
    print("2. Revenus")
    print("3. Locations par vehicules")
    print("4. vehicule le plus loue")
    print("5. Ajouter un client")
    print("6. Ajouter un vehicule")
    print("0. Quitter")

def menu_principal(agence):
    while True:
        afficher_menu()
        choix = input("Votre choix : ")
        if choix == "1":
            print(agence.compter_par_statut())
        elif choix == "2":
            print(agence.calculer_revenus())
        elif choix == "3":
            print(agence.compter_locations_par_vehicule())
        elif choix == "4":
            print(agence.vehicule_le_plus_loue())
        elif choix == "5":
            saisir_client(agence)
        elif choix == "6":
            saisir_vehicule(agence)
        elif choix == "0":
            print("Au revoir")
            break
        else:
            print("Choix invalide")




if __name__ == "__main__":
    agence = Agence()
    try:
        agence.charger()
    except ValueError as e:
        print("Erreur :", e)
        print("Le fichier agence.json est invalide. Corrigez-le ou renommez-le, puis relancez.")
    else:
        menu_principal(agence)



