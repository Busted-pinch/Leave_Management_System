from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# Connect to MongoDB
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["leave_management"]
leave_collection = db["leave_applications"]

# ---------------------------
# Fix existing leave documents
# ---------------------------
leaves = list(leave_collection.find({}))
for lv in leaves:
    updated_fields = {}

    # Required string fields
    for field, default in [
        ("employee_id", "-"),
        ("employee_name", "-"),
        ("employee_email", "-"),
        ("employee_dept", "-"),
        ("title", "-"),
        ("description", "-"),
    ]:
        if field not in lv or lv[field] is None:
            updated_fields[field] = default

    # Dates
    for date_field in ["start_date", "end_date"]:
        if date_field not in lv or not isinstance(lv[date_field], datetime):
            # fallback to today if missing
            updated_fields[date_field] = datetime.utcnow()

    # Days
    if "days" not in lv or not isinstance(lv["days"], int):
        start = updated_fields.get("start_date", lv.get("start_date", datetime.utcnow()))
        end = updated_fields.get("end_date", lv.get("end_date", datetime.utcnow()))
        delta = (end - start).days + 1
        updated_fields["days"] = max(delta, 1)

    # Status
    if "status" not in lv or lv["status"] not in ["Pending", "Approved", "Rejected"]:
        updated_fields["status"] = "Pending"

    if updated_fields:
        leave_collection.update_one({"_id": lv["_id"]}, {"$set": updated_fields})
        print(f"Updated leave {_id}: {updated_fields}")

print("✅ All leave documents fixed for frontend compatibility.")
