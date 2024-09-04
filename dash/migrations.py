# from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from datetime import datetime

# # Define the database connection string
# DATABASE_URL = "postgresql://postgres:azbycx567@docker/frauddetection"

# # Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Create a base class for the models
# Base = declarative_base()

# # Define the Transaction model
# class Transaction(Base):
#     __tablename__ = 'transactions'

#     id = Column(Integer, primary_key=True)
#     key = Column(String(255), nullable=False)
#     index = Column(Integer, nullable=False)
#     phonenumber = Column(String(20), nullable=False)
#     time = Column(TIMESTAMP, default=datetime.utcnow)
#     v1 = Column(String(255))
#     v2 = Column(String(255))
#     v3 = Column(String(255))
#     v4 = Column(String(255))
#     v5 = Column(String(255))
#     v6 = Column(String(255))
#     v7 = Column(String(255))
#     v8 = Column(String(255))
#     v9 = Column(String(255))
#     v10 = Column(String(255))
#     v11 = Column(String(255))
#     v12 = Column(String(255))
#     v13 = Column(String(255))
#     v14 = Column(String(255))
#     v15 = Column(String(255))
#     v16 = Column(String(255))
#     v17 = Column(String(255))
#     v18 = Column(String(255))
#     v19 = Column(String(255))
#     v20 = Column(String(255))
#     v21 = Column(String(255))
#     v22 = Column(String(255))
#     v23 = Column(String(255))
#     v24 = Column(String(255))
#     v25 = Column(String(255))
#     v26 = Column(String(255))
#     v27 = Column(String(255))
#     v28 = Column(String(255))
#     amount = Column(Integer, default=0)
#     time_produced = Column(TIMESTAMP, default=datetime.utcnow)
#     time_processed = Column(TIMESTAMP, default=datetime.utcnow)
#     latency = Column(Integer, default=0)
#     prediction = Column(Integer, default=0)
#     reply = Column(String(255))
#     is_fraud = Column(Boolean, default=False)

#     feedbacks = relationship("Feedback", back_populates="transaction")

#     def save(self, session):
#         """Saves the transaction record to the database."""
#         session.add(self)
#         session.commit()

# # Define the Feedback model
# class Feedback(Base):
#     __tablename__ = 'feedbacks'

#     id = Column(Integer, primary_key=True)
#     transaction_id = Column(Integer, ForeignKey('transactions.id'), nullable=False)
#     feedback_type = Column(String(20), nullable=False)
#     feedback_response = Column(String(20), nullable=False)
#     processed_by = Column(String(50))
#     feedback_timestamp = Column(TIMESTAMP, default=datetime.utcnow)

#     transaction = relationship("Transaction", back_populates="feedbacks")

#     def save(self, session):
#         """Saves the feedback record to the database."""
#         session.add(self)
#         session.commit()

# # Create a sessionmaker
# Session = sessionmaker(bind=engine)

# def create_tables():
#     """Creates the necessary tables in the database."""
#     Base.metadata.create_all(engine)

# def drop_tables():
#     """Drops the tables in the database (use with caution)."""
#     Base.metadata.drop_all(engine)

# if __name__ == "__main__":
#     # Uncomment the next line to drop existing tables (use with caution)
#     # drop_tables()

#     create_tables()  # Create the tables
