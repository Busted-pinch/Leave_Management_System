from app.db.mongodb import db  # your MongoDB client

def get_next_employee_number():
    counter = db.counters.find_one_and_update(
        {"_id": "employee_number"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]
