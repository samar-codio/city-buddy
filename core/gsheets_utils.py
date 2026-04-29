import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from django.conf import settings

def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_path = os.path.join(settings.BASE_DIR, 'service_account.json')
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    return client

def push_order_to_sheet(order):
    try:
        client = get_gsheet_client()
        sheet = client.open("CityBuddyData").worksheet("Order")
        # Prepare the row data
        row = [
            str(order.id),
            order.user.email,
            order.name,
            order.phone_number,      
            order.alt_phone_number,  
            order.get_service_display() if order.service else "N/A",
            order.room_no,
            order.status,
            order.created_at.strftime("%Y-%m-%d %H:%M")
        ]
        sheet.append_row(row)
    except Exception as e:
        print(f"❌ Google Sheets Sync Error: {e}")

def get_price_list_from_sheet():
    try:
        client = get_gsheet_client()
        sheet = client.open("CityBuddyData").worksheet("PriceList")

        # Returns a list of dictionaries (if headers exist)
        return sheet.get_all_records()
    except Exception as e:
        print(f"❌ Price List Fetch Error: {e}")
        return []