from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, MDMAccount, ELITEAccount, ANCIENTAccount

# Configure your database URI
DATABASE_URI = 'sqlite:///instance/dataB.db'

# Create an engine and initialize the database connection
engine = create_engine(DATABASE_URI)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

def add_account(username, password, rarity):
    # Create a new CommonAccount instance
    new_account = ELITEAccount(username=username, password=password, rarity=rarity)

    # Add the new account to the session
    session.add(new_account)

    # Commit the transaction
    session.commit()
    print(f"Account with username '{username}' added successfully!")

if __name__ == '__main__':
    # Example usage
    add_account('uncommon1', 'uncommon1', 'epic')
    add_account('uncommon3', 'uncommon3', 'legend')
    add_account('uncommon4', 'uncommon4', 'mythic')

    # Close the session
    session.close()
