import json
from datetime import datetime

def handle(event, context):
    """
    Déclenché par CRON, cette fonction publie un message sur le topic NATS 'orders.import'.
    Le message contient la date du jour pour simuler une nouvelle commande.
    """
    now = datetime.now().isoformat()
    
    message = {
        "event_time": now,
        "message": "Déclenchement quotidien de l'importation des commandes."
    }
    
    # Le message est automatiquement publié sur le 'write_topic' défini dans stack.yml
    print(f"Publication du message sur 'orders.import': {json.dumps(message)}")
    
    return {
        "statusCode": 200,
        "body": json.dumps(message)
    }