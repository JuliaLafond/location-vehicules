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

class Moto(Vehicule):
    def __init__(self, id, marque, modele, immatriculation, tarif_jour, cylindree):
        super().__init__(id, marque, modele, immatriculation, tarif_jour)
        self.cylindree = cylindree
    def calculer_cout(self,nb_jours ):
        base = super().calculer_cout(nb_jours)
        if nb_jours > 3:
            base = base * 0.9
        return base

class Client:
    def __init__(self, id, nom, telephone, numero_permis):
        if not nom.strip():
            raise ValueError("Nom vide")
        self.id = id
        self.nom = nom
        self.telephone = telephone
        self.numero_permis = numero_permis

class Maintenance:
    def __init__(self, id, vehicule_id, date_debut, date_fin):
        if date_fin < date_debut:
            raise ValueError("La date de fin precede la date de debut")
        self.id = id
        self.vehicule_id = vehicule_id
        self.date_debut = date_debut
        self.date_fin = date_fin

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





v= Vehicule(1, "Toyota", "corolla", "AA-1234", 50)
print(v.obtenir_etat())
print(v.marque)
try:
    v.changer_tarif(-5)
except ValueError as e:
    print("refuse :", e)
v.changer_etat("Loue")
print(v._etat)
try:
    v.changer_etat("banane")
except ValueError as e:
    print("refuse :", e)

c=Voiture(2, "Honda", "Civic", 'BB-5678', 60, 4)
print(c.marque)
c.changer_etat("Loue")

m=Moto(3, "Yamaha", "R15", "CC-916", 25, 155)
print(m.cylindree)
print(c.calculer_cout(2))
print(m.calculer_cout(5))

cl=Client(1,"Michelande","3246-1809","HT123478")
print(cl.nom)
try:
    Client(2,'',"1134-5676","HT5678")
except ValueError as e:
    print("refuse :", e)

m1=Maintenance(1,2,date(2026,11,10),date(2026,11,12))
print(m1.date_debut)
try:
    Maintenance(2,2,date(2026,11,12),date(2026,11,10))
except ValueError as e:
    print("refuse :", e)

r=Reservation(1,1,2,date(2026,11,11),date(2026,11,13), 130)
print(r.client_id)
print(r.vehicule_id)

try:
    Reservation(2,1,2,date(2026,11,13),date(2026,11,11),130)
except ValueError as e:
    print("refuse :", e)

r=Reservation(1,1,2,date(2026,11,11),date(2026,11,13),130)
r.changer_statut("en cours")
print(r._statut)

try:
    r.changer_statut("bambou")
except ValueError as e:
    print('refuse :', e)

c = Voiture(2, "Honda", "Civic", "BB-5678", 60, 4)
r = Reservation(1, 1, 2, date(2026, 11, 11), date(2026, 11, 13), 0)
print(r.nb_jours())
r.montant = c.calculer_cout(r.nb_jours())
print(r.montant)

ag = Agence()
ag.ajouter_client(Client(1, "Marie Joseph", "2345-5676", "HT1233"))
print(len(ag.clients))
print(ag.clients[0].nom)
ag.ajouter_vehicule(Voiture(1, "Honda", "Civic", "BB-5678", 60, 4))
print(len(ag.vehicules))
print(ag.vehicules[0].marque)

# agence=Agence()
# print(agence.nouveau_id_client())
# print(agence.nouveau_id_client())
# print(agence.nouveau_id_client())
#
# ag2=Agence()
# print(ag2.nouveau_id_vehicule())
# print(ag2.nouveau_id_vehicule())
# print(ag2.nouveau_id_vehicule())
ag3 = Agence()
ag3.ajouter_client(Client(ag3.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag3.ajouter_client(Client(ag3.nouveau_id_client(), "Mar Joseph", "2345-5676", "HT1233"))
print(ag3.clients[0].id)
print(ag3.clients[1].id)

ag4 = Agence()
ag4.ajouter_vehicule(Voiture(ag4.nouveau_id_vehicule(),"HONDA", "Civic", "BB-5678", 60, 4))
ag4.ajouter_vehicule(Moto(ag4.nouveau_id_vehicule(), "Honda", "CB500", "MM-2222", 40, 500))
ag4.ajouter_vehicule(Voiture(ag4.nouveau_id_vehicule(), "Toyota", "Corolla", "BB-3333", 55, 4))

print(len(ag4.rechercher_par_marque("Honda")))
print(len(ag4.rechercher_par_marque("Toyota")))
print(len(ag4.rechercher_par_marque("BMW")))

for v in ag4.trier_par_tarif():
    print(v.modele, v.obtenir_tarif())

ag5 = Agence()
ag5.ajouter_vehicule(Voiture(ag5.nouveau_id_vehicule(), "Honda", "civic", "BB-5678", 60, 4))
ag5.reservations.append(Reservation(1, 1, 1, date(2026, 11, 11), date(2026, 11, 13), 130))
print(ag5.est_disponible(1, date(2026, 11, 11), date(2026, 11, 14)))
print(ag5.est_disponible(1, date(2026, 11, 13), date(2026, 11, 15)))

ag6 = Agence()
print(ag6.nouveau_id_reservation())
print(ag6.nouveau_id_reservation())
print(ag6.nouveau_id_maintenance())

ag7 = Agence()
ag7.ajouter_client(Client(ag7.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag7.ajouter_vehicule(Voiture(ag7.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))

r1 = ag7.reserver(1,1,date(2026,11, 20), date(2026, 11, 23))
print(r1.montant)

try:
    ag7.reserver(1,1,date(2026,11, 22), date(2026, 11, 23))
except ValueError as e:
    print('refuse :', e)
print(len(ag7.reservations))

ag8 = Agence()
ag8.ajouter_client(Client(ag8.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag8.ajouter_vehicule(Voiture(ag8.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))
ag8.reserver(1,1,date(2026,11, 20), date(2026, 11, 23))
ag8.reserver(1,1,date(2026, 12, 1), date(2026, 12, 3))
print(ag8.trouver_reservation(1).montant)
print(ag8.trouver_reservation(98))

print(ag8.annuler(1, date(2026, 11, 12)))
print(ag8.annuler(2, date(2026, 11, 30)))

try:
    ag8.annuler(1, date(2026, 11, 12))
except ValueError as e:
    print('refuse :', e)

print(ag8.est_disponible(1, date(2026, 11, 20), date(2026, 11, 23)))

ag9= Agence()
ag9.ajouter_client(Client(ag9.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag9.ajouter_vehicule(Voiture(ag9.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))
ag9.reserver(1,1,date(2026, 11, 20), date(2026, 11, 23))

ag9.enregistrer_depart(1)
print(ag9.trouver_reservation(1)._statut)
print(ag9.trouver_vehicule(1).obtenir_etat())

try:
    ag9.enregistrer_depart(1)
except ValueError as e:
    print('refuse :', e)

ag10 = Agence()
ag10.ajouter_client(Client(ag10.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag10.ajouter_vehicule(Voiture(ag10.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))
ag10.reserver(1,1, date(2026, 11, 20), date(2026, 11, 23))
ag10.enregistrer_depart(1)

print(ag10.enregistrer_retour(1, date(2026, 11, 23)))
print(ag10.trouver_reservation(1)._statut)
print(ag10.trouver_vehicule(1).obtenir_etat())
print(ag10.trouver_reservation(1).date_retour)
print(ag10.trouver_reservation(1).montant_final)

try:
    ag10.enregistrer_retour(1, date(2026, 11, 23))
except ValueError as e:
    print("refuse :",e)

ag11 = Agence()
ag11.ajouter_client(Client(ag11.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag11.ajouter_vehicule(Voiture(ag11.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))
ag11.reserver(1,1, date(2026, 11, 20), date(2026, 11, 23))
ag11.enregistrer_depart(1)

print(ag11.enregistrer_retour(1, date(2026, 11, 25)))
print(ag11.trouver_reservation(1).frais_retard)

ag12 = Agence()
ag12.ajouter_client(Client(ag12.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag12.ajouter_vehicule(Voiture(ag12.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))
ag12.reserver(1,1, date(2026, 11, 20), date(2026, 11, 23))
ag12.enregistrer_depart(1)

print(ag12.enregistrer_retour(1, date(2026, 11, 21)))
print(ag12.trouver_reservation(1).frais_retard)

ag12.reserver(1,1, date(2026, 12, 1), date(2026, 12, 3))
ag12.enregistrer_depart(2)
try:
    ag12.enregistrer_retour(2, date(2026, 11, 30))
except ValueError as e:
    print("refuse :", e)

ag13 = Agence()
ag13.ajouter_client(Client(ag13.nouveau_id_client(), "Marie Joseph", "2345-5676", "HT1233"))
ag13.ajouter_vehicule(Voiture(ag13.nouveau_id_vehicule(), "Honda", "Civic", "BB-5678", 60, 4))
ag13.reserver(1,1, date(2026, 11, 20), date(2026, 11, 23))

try:
    ag13.planifier_maintenance(1, date(2026, 11, 21), date(2026, 11, 22))
except ValueError as e:
    print("refuse :", e)

ag13.planifier_maintenance(1, date(2026, 11, 25), date(2026, 11, 27))
print(len(ag13.maintenances))

try:
    ag13.reserver(1, 1, date(2026, 11, 26), date(2026, 11, 28))
except ValueError as e:
    print("refuse :", e)

