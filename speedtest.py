import requests
import time

def download_upload_speed():
    try:
        # URL du fichier à télécharger
        url = "http://bouygues.testdebit.info/100M.iso"

        # Chemin du fichier de destination pour le téléchargement
        filename = "/tmp/100m.iso"

        # Téléchargement du fichier
        start_time = time.time()
        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        download_time = time.time() - start_time

        # URL de destination pour le téléversement
        upload_url = "http://bouygues.testdebit.info/ul/"

        # Taille des chunks pour le téléversement
        chunk_size = 1024*1024

        # Ouverture du fichier pour le téléversement
        with open(filename, 'rb') as f:
            # Calcul de la taille totale du fichier
            file_size = len(f.read())

            # Retour au début du fichier
            f.seek(0)

            # Paramètres pour le téléversement
            files = {'file': ('100m.iso', f)}
            start_time = time.time()
            r = requests.post(upload_url, files=files)

        # Calcul de la durée du téléversement
        upload_time = time.time() - start_time

        # Calcul de la vitesse de téléchargement et de téléversement en Mbps
        download_speed = round(file_size / download_time / 1024 / 1024 * 8, 2)
        upload_speed = round(file_size / upload_time / 1024 / 1024 * 8, 2)

        # Affichage des résultats
        print(f"Vitesse de téléchargement : {download_speed:.2f} Mbps")
        print(f"Vitesse de téléversement : {upload_speed:.2f} Mbps")

        # Suppression du fichier de 100 Mo
        import os
        os.remove(filename)

        return download_speed, upload_speed

    except:
        print("Erreur")
        return "error", "error"
