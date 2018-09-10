# -*- coding: utf-8 -*-


def includeme(config):
    config.add_route("index", "/")

    config.add_route("install", "/install")

    config.add_route("launch", "/launch")
    config.add_route("launch_form", "/launch/form")
    config.add_route("launch_sign", "/launch/sign")
