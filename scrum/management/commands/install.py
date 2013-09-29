from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.core.management import call_command
from django.core.validators import validate_email 

import re

class Command(BaseCommand):

    def commandError(self, message):
        raise CommandError("ERROR: %s\n" % message)
        exit()

    def error(self, message):
        raise Exception("ERROR: %s\n" % message)
        exit()


    #Install the environment, first arg: username, second arg: email
    def handle(self, *args, **options):
        MANAGER_GROUP = 'Manager'
        CLIENT_GROUP = 'Client'
        TEAM_GROUP = 'Team'

        if len(args) != 2:
            self.commandError('Please provide 2 parameters: username email')

        username = args[0]
        email = args[1]

        #Try to validate email
        try:
            validate_email(email)
        except ValidationError as e:
            raise e

        print '######################################'
        print '#       WELCOME TO AGILE BOARD       #'
        print '######################################\n\n'
        
        #Check if the username already exists
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass
        else:
            self.error('The username ' + username + ' already exists!')
            
        print 'A manager account will be created with the username : ' + username
        print 'please enter your password below'    

        #Create the superuser
        try:
            call_command('createsuperuser', username=username, email=email)
            user = User.objects.get(username=username)
        except Exception:
            self.error('*** An error occured! ****')

        #Create 3 groups if they not exist
        try:
            Group.objects.get(name=CLIENT_GROUP)
        except ObjectDoesNotExist:
            Group.objects.create(name=CLIENT_GROUP)
            
        try:
            Group.objects.get(name=TEAM_GROUP)
        except ObjectDoesNotExist:
            Group.objects.create(name=TEAM_GROUP)
            
        try:
            manager_group = Group.objects.get(name=MANAGER_GROUP)
        except ObjectDoesNotExist:
            manager_group = Group.objects.create(name=MANAGER_GROUP)
        
        user.groups.add(manager_group)
        
        print '*** Installation complete! ***'