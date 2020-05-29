from sqlalchemy import func


def count(session, obj):
    return session.query(func.count(obj)).scalar()

def add(session, obj):
    session.add(obj)
    session.commit()

def delete(session, obj):
    session.delete(obj)
    session.commit()

def commit(session):
    session.commit()