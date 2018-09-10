# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def app(global_config, **settings):
    """Return the Pyramid WSGI application."""
    config = Configurator(settings=settings)
    config.include("pyramid_jinja2")

    config.include(".models")
    config.include(".routes")

    config.add_static_view("static", "static")

    config.set_session_factory(SignedCookieSessionFactory('itsaseekreet'))

    config.scan()

    return config.make_wsgi_app()
