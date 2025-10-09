from app.db.mongodb import db

def get_next_employee_number():
    counter = db.counters.find_one_and_update(
        {"_id": "employee_number"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    # Format as EMP001, EMP002, etc.
    return f"EMP{counter['seq']:03d}"

def get_next_manager_number():
    counter = db.counters.find_one_and_update(
        {"_id": "manager_number"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    # Format as MAN001, MAN002, etc.
    return f"MAN{counter['seq']:03d}"


