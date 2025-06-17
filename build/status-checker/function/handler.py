import os
import json
from ftplib import FTP

def handle(event, context):
    """
    Fonction HTTP qui retourne le nombre de fichiers dans /US17/depot (FTP)
    """
    ftp_host = os.getenv("SFTP_HOST")
    ftp_user = os.getenv("SFTP_USER")
    ftp_pass = os.getenv("SFTP_PASS")
    user_id = os.getenv("USER_ID", "US17")

    depot_path = f"{user_id}/depot"

    try:
        ftp = FTP()
        ftp.connect(ftp_host, 21)
        ftp.login(ftp_user, ftp_pass)
        ftp.cwd(depot_path)

        files = [f for f in ftp.nlst() if f not in ('.', '..')]
        files = ftp.nlst()
        file_count = len(files)

        ftp.quit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "depot_path": depot_path,
                "file_count": file_count,
                "files": files
            })
        }

    except Exception as e:
        error_message = f"Erreur lors de la vérification: {str(e)}"
        print(error_message)

        return {
            "statusCode": 500,
            "body": json.dumps({"error": error_message})
        }
