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

class Voiture(Vehicule):
    def __init__(self, id, marque, modele, immatriculation, tarif_jour, nb_portes):
        super().__init__(id, marque, modele, immatriculation, tarif_jour)
        self.nb_portes = nb_portes

class Moto(Vehicule):
    def __init__(self, id, marque, modele, immatriculation, tarif_jour, cylindree):
        super().__init__(id, marque, modele, immatriculation, tarif_jour)
        self.cylindree = cylindree



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