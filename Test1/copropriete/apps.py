from django.apps import AppConfig


class CoproprieteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'copropriete'

    def ready(self):
        from .models import Copropriete

        print('Début chargement du dataset')
        Copropriete.DATASET = Copropriete.init_dataset('/srv_perso/apps/dataset_annonces.csv', None)
        print('Fin chargement du dataset')
