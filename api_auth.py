#!/usr/bin/env python
# Module to retrieve bot info via prompt or configuration file
import praw
import getpass as gp
import os
import ConfigParser

# Get bot info via user input or configuration file if it exists
def get_info():
    # Initialize ConfigParser and load configuration if it exists
    config = ConfigParser.ConfigParser()
    CONFIG_FILE_NAME = "config.ini"
    # Check if the config file exists
    file_exists = os.path.isfile(CONFIG_FILE_NAME)
    print "Config file exists =>", file_exists

    # If it doesn't exist, create it
    if not file_exists:
        print "Config file created =>",os.path.isfile(CONFIG_FILE_NAME)
        config_file = open('config.ini', "w+")
        config.add_section('BOT_VALUES')
    else:
        config_file = open('config.ini', "r")
    config.readfp(config_file)

    # Prompt user for secure entry of password
    print "Enter bot account's password (this will NOT be stored)"
    password = gp.getpass().strip()

    # Gather bot info
    if file_exists:
        # Load from configuration
        username = config.get('BOT_VALUES', 'username')
        app_id = config.get('BOT_VALUES', 'app_id')
        header = config.get("BOT_VALUES", 'header')
        app_secret = config.get('BOT_VALUES', 'app_secret')
    else:
        # Prompt user for bot info
        username = raw_input("Enter username: ").strip()
        app_id = raw_input("Enter app id: ").strip()
        header = raw_input("Enter a header of form <platform>:<app ID>:<version string> (by /u/<reddit username>):\n").strip()
        app_secret = raw_input("Enter app secret: ").strip()
        # Write configuration
        config.set('BOT_VALUES', 'username', username)
        config.set('BOT_VALUES', 'app_id', app_id)
        config.set("BOT_VALUES", 'header', header)
        config.set('BOT_VALUES', 'app_secret', app_secret)
        config.write(config_file)

    # Aggregate data and send to Reddit's authentication server (OAuth2)
    app = {'id': app_id, 'secret': app_secret, 'username': username, 'password': password}
    r = praw.Reddit(header)
    r.set_oauth_app_info(client_id=app['id'],client_secret=app['secret'],redirect_uri='http://127.0.0.1:65010/authorize_callback')

    # Write out and close configuration file
    config_file.close()
    return r
