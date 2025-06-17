import json
import os
import csv
import io
from datetime import datetime
import ftplib

def handle(event, context):
    """
    File Transformer - triggered by NATS or manual invoke.
    Connects to FTP, processes a CSV file, and uploads the transformed result.
    """
    try:
        user_id = os.getenv("USER_ID", "US17")
        ftp_host = os.getenv("SFTP_HOST")
        ftp_user = os.getenv("SFTP_USER")
        ftp_pass = os.getenv("SFTP_PASS")

        if not ftp_host or not ftp_user or not ftp_pass:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "FTP credentials are missing in environment variables."})
            }

        try:
            payload = json.loads(event.body) if hasattr(event, 'body') else json.loads(event)
        except Exception:
            payload = {"source": "manual_trigger"}

        with ftplib.FTP() as ftp:
            ftp.connect(ftp_host, 21)
            ftp.login(ftp_user, ftp_pass)
            ftp.cwd("{}/data".format(user_id))

            csv_lines = []
            ftp.retrlines("RETR input.csv", callback=csv_lines.append)
            csv_text = "\n".join(csv_lines)

            reader = csv.DictReader(io.StringIO(csv_text))
            original_rows = list(reader)

            processed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_rows = []

            for row in original_rows:
                row["customer"] = row.get("customer", "").upper()
                row["product"] = row.get("product", "").lower()
                row["Processed-Date"] = processed_time
                row["processed_by"] = user_id
                updated_rows.append(row)

            output_stream = io.StringIO()
            if updated_rows:
                writer = csv.DictWriter(output_stream, fieldnames=updated_rows[0].keys())
                writer.writeheader()
                writer.writerows(updated_rows)

            ftp.cwd("/{}/depot".format(user_id))
            output_data = output_stream.getvalue().encode("utf-8")
            ftp.storbinary("STOR output.csv", io.BytesIO(output_data))

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Transformation completed.",
                "output_file": "{}/depot/output.csv".format(user_id),
                "rows": len(updated_rows),
                "timestamp": processed_time
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Unexpected error during processing.",
                "details": str(e)
            })
        }
