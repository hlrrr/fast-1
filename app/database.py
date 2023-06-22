# Import the SQLAlchemy parts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config   import settings

engine = create_engine(
    settings.database_url,
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)
Base = declarative_base()

# database session for prod
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLALCHEMY_DATABASE_URL = f"postgresql://lima:1q2w3e4r5t@211.117.18.86:15432/test"
## db connection
# while True:
#     try:
#         conn=psycopg2.connect(
#             host='211.117.18.86',
#             port='15432',
#             user='lima',
#             password='1q2w3e4r5t',
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print(f"Db conn: Done")
#         break

#     except Exception as error:  
#         print("DB conn: Failed")
#         print("Error: ", error)
#         time.sleep(3)

# # move to "test" directory
# engine_test = create_engine(
#     settings_test.database_url_test,
#     # connect_args={"check_same_thread": False}
# )
# SessionLocal_test = sessionmaker(autocommit=False,
#                                  autoflush=False,
#                                  bind=engine_test)
# # database session for prod
# def get_db_test():
#     db = SessionLocal_test()
#     try:
#         yield db
#     finally:
#         db.close()