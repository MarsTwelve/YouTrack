from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
import os

from src.Database.models import Base


class Database:

    def __init__(self):
        """
        Connects to the MySQL database, in case the database does not exist, it creates a database and then connects.

        [WARNING] --> This might have inconsistencies when running in different computers with different versions of
        MySQL, further testing is required
        """
        self.engine = create_engine("mysql+pymysql://root:password@localhost/vehicle_tracker_V1", echo=True)
        if not database_exists(self.engine.url):
            create_database(self.engine.url)

        Base.metadata.create_all(self.engine)

    def get_session(self):
        session = Session(self.engine)
        return session
