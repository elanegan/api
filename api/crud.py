import api.schemas as schemas
import api.models as models

from sqlalchemy.orm import Session


def get_tournament_by_name(db: Session, name: str):
    return (
        db.query(models.Tournament)
            .filter(models.Tournament.name == name)
            .first()
    )


def get_tournament_by_id(db: Session, tournament_id: str):
    return (
        db.query(models.Tournament)
            .filter(models.Tournament.id == tournament_id)
            .first()
    )


def create_tournament(db: Session, tournament: schemas.Tournament):
    db_tournament = models.Tournament(
        region=tournament.region,
        name=tournament.name,
        time=tournament.time,
        prize=tournament.prize
    )
    # todo check how optional works in situation like below
    if tournament.description:
        db_tournament.description = tournament.description
    if tournament.region:
        db_tournament.region = tournament.region
    else:
        db_tournament.region = 'international'
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def get_tournaments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tournament).offset(skip).limit(limit).all()


def add_tournament_user(db: Session, tournament_id: int):
    pass

def create_user(db: Session, user: schemas.User):
    hashed_password = user.password + 'TODO: hash'
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        username=user.username,
        date_of_birth=user.date_of_birth
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

