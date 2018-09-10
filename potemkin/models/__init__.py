"""Boilerplate stuff for initializing SQLAlchemy."""
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import configure_mappers
import zope.sqlalchemy

from potemkin.models.base import Base
from potemkin.models.application_instance import ApplicationInstance


configure_mappers()


def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession


def includeme(config):
    settings = config.get_settings()
    settings["tm.manager_hook"] = "pyramid_tm.explicit_manager"

    config.include("pyramid_tm")
    config.include("pyramid_retry")

    engine = engine_from_config(settings, "sqlalchemy.")

    Base.metadata.create_all(engine)

    session_factory = sessionmaker()
    session_factory.configure(bind=engine)
    config.registry["dbsession_factory"] = session_factory

    def dbsession(session_factory, transaction_manager):
        dbsession = session_factory()
        zope.sqlalchemy.register(dbsession, transaction_manager=transaction_manager)

    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        "db",
        reify=True
    )
