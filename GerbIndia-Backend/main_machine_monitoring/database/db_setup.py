from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from main_machine_monitoring.pydantic_schema.request_schema import IpPhase, settings

ip_phase = settings
ipadd = ip_phase.ip_address

print(ipadd)
# Create the settings instance with the obtained IP address
settings = IpPhase()


# print(settings.ip_address)

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:siri2251105@{settings.ip_address}/gerb"

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()



# Dependency
def get_db():
    db = SessionLocal()
    print(SQLALCHEMY_DATABASE_URL)
    print(db)
    try:
        yield db
    finally:
        db.close()

# docker run -e IP_ADDRESS=10.82.126.73 --name demo_gerb_container -p 8000:8000 demo/gerb:1.0
#docker tag tiei_main_initial:real_data_fix3 smt18m005/tiei-repo:real_data_fix3

