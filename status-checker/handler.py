import json
import os
import paramiko

def handle(event, context):
    """
    Fonction HTTP qui retourne le nombre de fichiers dans /USX/depot
    """
    try:
        user_id = os.getenv('USER_ID', 'US17')
        
        # Configuration SFTP
        sftp_host = os.getenv('SFTP_HOST')
        sftp_user = os.getenv('SFTP_USER')
        sftp_pass = os.getenv('SFTP_PASS')
        
        if not all([sftp_host, sftp_user, sftp_pass]):
            return json.dumps({
                "error": "SFTP configuration missing",
                "user_id": user_id
            })
        
        # Connexion SFTP
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(sftp_host, username=sftp_user, password=sftp_pass)
        sftp = ssh.open_sftp()
        
        # Comptage des fichiers dans /USX/depot
        depot_path = f"/{user_id}/depot"
        try:
            files = sftp.listdir(depot_path)
            file_count = len([f for f in files if not f.startswith('.')])
        except FileNotFoundError:
            file_count = 0
            files = []
        
        # Fermeture des connexions
        sftp.close()
        ssh.close()
        
        # Réponse JSON
        response = {
            "user_id": user_id,
            "depot_path": depot_path,
            "file_count": file_count,
            "files": files,
            "status": "success"
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        error_response = {
            "error": str(e),
            "user_id": os.getenv('USER_ID', 'US17'),
            "status": "error"
        }
        return json.dumps(error_response, indent=2)