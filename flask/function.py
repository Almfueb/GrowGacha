# functions.py

import random
from datetime import datetime
from models import db, History
def move_account_to_history(account, user_id):
    # Create a new history record with the necessary information
    history_entry = History(
        user_id=user_id,
        username=account.username,
        password=account.password,
        rarity=account.rarity,
        timestamp=datetime.utcnow()  # or the appropriate timestamp format
    )
    
    # Add and commit the history record
    db.session.add(history_entry)
    db.session.delete(account)  # Assuming you want to delete the account from the original table
    db.session.commit()

