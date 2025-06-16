import json
import os
import csv
from datetime import datetime
from pathlib import Path

def handle(event, context):
    """

    """
    try:
        if event:
            try:
                message = json.loads(event)
                user_id = message.get('user_id', os.getenv('USER_ID', 'US1'))
            except:
                user_id = os.getenv('USER_ID', 'US1')
        else:
            user_id = os.getenv('USER_ID', 'US1')

        input_file = "function/Data/input.csv"
        depot_path = "function/Depot"
        data_path = os.path.dirname(input_file)

        if not os.path.exists(input_file):
            return json.dumps({
                "status": "error",
                "message": f"File {input_file} not found",
                "user_id": user_id,
                "data_path": data_path,
                "files_in_data": os.listdir(data_path) if os.path.exists(data_path) else []
            }, indent=2)
                
        transformed_rows = []
        process_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(input_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                
                if 'customers' in row:
                    row['customers'] = row['customers'].upper()
                if 'product' in row:
                    row['product'] = row['product'].lower()
                
                row['Processed-Date'] = process_datetime
                row['process_by'] = user_id
                
                transformed_rows.append(row)
        
        if not transformed_rows:
            return json.dumps({
                "status": "error",
                "message": "No data found in CSV file",
                "user_id": user_id
            }, indent=2)
        
        output_file = "function/Depot/output.csv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = transformed_rows[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transformed_rows)
        
        result = {
            "status": "success",
            "message": f"File transformed successfully. Processed {len(transformed_rows)} records",
            "user_id": user_id,
            "processed_at": process_datetime,
            "input_file": str(input_file),
            "output_file": str(output_file),
            "records_processed": len(transformed_rows),
            "columns_added": ["Processed-Date", "process_by"]
        }
        
        print(f"File transformation completed for {user_id}: {len(transformed_rows)} records")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        error_result = {
            "status": "error",
            "error": str(e),
            "user_id": os.getenv('USER_ID', 'US1'),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Error in file-transformer: {str(e)}")
        return json.dumps(error_result, indent=2)