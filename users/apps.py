from django.apps import AppConfig
from configparser import ConfigParser

"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

This file is created to help the user include any application configuration for the app. Using this, you can configure some of the 
attributes of the application. From Application Configuration documentation: Application configuration objects store metadata for an application.
The use of the users signal is defined in the ready method will run during startup of every management command. Dispatching of signals is
used in the user model defined here.
"""

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals

