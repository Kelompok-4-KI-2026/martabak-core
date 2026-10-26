from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DATABASE_URL

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as conn:
        try:
            from sqlalchemy import text
            if DATABASE_URL.startswith("sqlite"):
                res = conn.execute(text("PRAGMA table_info(users)"))
                cols = [row[1] for row in res.fetchall()]
            else:
                res = conn.execute(
                    text("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'users'")
                )
                cols = [row[0] for row in res.fetchall()]

            if cols and "full_name" not in cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN full_name VARCHAR(150)"))
            if cols and "outlet_name" not in cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN outlet_name VARCHAR(150)"))
            conn.commit()
        except Exception:
            pass
