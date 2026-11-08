from datetime import date
class Vehicule:
    def __init__(self, id, marque, modele, immatriculation, tarif_jour):
        self.id = id
        self.marque = marque
        self.modele = modele
        self.immatriculation = immatriculation
        self.tarif_jour = 0
        self.etat = "disponible"
        self.changer_tarif(tarif_jour)

    def changer_tarif(self, valeur):
        if valeur <= 0:
            raise ValueError("Le tarif doit etre positif")
        self._tarif_jour = valeur

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

    def changer_statut(self, nouveau_statut):
        if nouveau_statut not in self.STATUTS:
            raise ValueError("Statut invalide")
        self._statut = nouveau_statut

    def nb_jours(self):
        return (self.date_fin - self.date_debut).days


v= Vehicule(1, "Toyota", "corolla", "AA-1234", 50)
print(v.etat)
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