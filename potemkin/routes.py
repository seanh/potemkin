# -*- coding: utf-8 -*-


def includeme(config):
    # The main page where you construct and execute LTI launches.
    config.add_route("launch", "/")

    # An OAuth 1.0 request-signing endpoint that's used to sign the LTI launch
    # forms.
    config.add_route("launch_sign", "/launch/sign")

    # The actual launch form that gets submitted to the LTI app.
    config.add_route("launch_form", "/launch/form")
