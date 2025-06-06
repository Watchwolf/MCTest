from django.db import models
import csv
import numpy as np
import urllib.request
import json

class Copropriete(models.Model):
    DATASET: list['Copropriete']
    
    source_url: str = models.CharField(max_length=200, null=False)
    api_id: str = models.CharField(max_length=100, null=False)
    charge: float = models.FloatField(default=None, null=True)
    departement: str = models.CharField(max_length=10, null=False)
    ville: str = models.CharField(max_length=20, null=False)
    code_postal: int = models.CharField(null=False)
    
    def get_api_url(self):
        """
        Retourne l'addresse WEB de l'API json de la copropriété
        """
        return 'https://www.bienici.com/realEstateAd.json?id=' % self.api_id

    def build_api_id(self):
        """
        Extrait l'identifiant de la copropriété à partir de l'url source complète
        """
        ##On considère que l'id est le dernier paramètre de l'url
        tab: list[str] = self.source_url.split('/')
        tab = tab[-1].split('=')
        self.api_id = tab[-1]

    def save(self):
        if not self.api_id:
            self.build_api_id()

        ##On n'a pas de BdD
        #return super(Copropriete, self).save()
    
    def add_to_dataset(url: str):
        """
        Ajouter une copropriété au dataset depuis son url bienici.com
        """
        copropriete: Copropriete = Copropriete()
        copropriete.source_url = url
        copropriete.build_api_id()

        dataJSON = None
        with urllib.request.urlopen('https://www.bienici.com/realEstateAd.json?id=%s' % copropriete.api_id) as response:
            if response.status == 200:
                content = response.read().decode('utf-8')
                try:
                    dataJSON = json.loads(content)
                except json.JSONDecodeError as e:
                    raise Exception(f"La réponse n'est pas un JSON valide pour l'URL: {url}. Erreur: {e}")
            else:
                raise Exception(f"Erreur HTTP: Statut {response.status} pour l'URL {url}")
        
        copropriete.code_postal = dataJSON['postalCode']
        copropriete.departement = copropriete.code_postal[:2] if copropriete.code_postal else ''
        copropriete.ville = dataJSON['city']
        copropriete.charge = dataJSON['annualCondominiumFees']
        copropriete.save()

        Copropriete.DATASET.append(copropriete)

    def init_dataset(dataSetPath: str, maxLines: int = None) -> list['Copropriete']:
        """
        À appeler pour charger les données de test depuis le fichier csv
        """
        coproprietes: list[Copropriete] = []

        with open(dataSetPath, mode='r', encoding='utf-8') as file_csv:
            ##TODO: gérer les doulons et les lignes invalides
            lines = csv.reader(file_csv)
            
            for line in lines:
                copropriete: Copropriete = Copropriete()
                copropriete.source_url = line[1]
                copropriete.departement = line[3]
                copropriete.code_postal = line[4]
                copropriete.ville = line[5]

                try:
                    copropriete.charge = float(line[14].replace(',', '.'))
                except ValueError as e:
                    copropriete.charge = None
                
                copropriete.save()

                coproprietes.append(copropriete)

                if maxLines and len(coproprietes) >= maxLines:
                    break

        return coproprietes
    
    def stats(filter: str):
        """
        Retourne les statistiques de la copropriété : moyenne, quantile 10 et quantile 90
        """
        dataset: list['Copropriete'] = [i.charge for i in Copropriete.DATASET if i.charge and (i.departement == filter or i.code_postal == filter or i.ville == filter)]

        avg = np.mean(dataset) if len(dataset) >= 1 else None
        q10 = np.quantile(dataset, 0.10) if len(dataset) >= 2 else None
        q90 = np.quantile(dataset, 0.90) if len(dataset) >= 2 else None
        
        return {'avg': avg, 'q10': q10, 'q90': q90}
