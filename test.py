# пример теста — сохранить в test_sa.py и запустить
from google.oauth2 import service_account
import gspread

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = service_account.Credentials.from_service_account_file("price-from-base-39198cff139d.json", scopes=SCOPES)
# если нужен impersonate:
# creds = creds.with_subject("user@yourdomain.com")

gc = gspread.authorize(creds)
sh = gc.open_by_key("1fni43Tj5fuqPWh8Ftd7LQ_L9i7mmIlW9OLhb68FBge8")
print("OK — title:", sh.title)