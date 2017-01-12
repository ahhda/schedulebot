from django.core.management.base import BaseCommand, CommandError
from fb_schedulebot.models import *
from fb_schedulebot.views import *

import csv

def return_list_from_file(filename):
    file1 = open(filename)
    csvdata = csv.reader(file1)
    messages = []
    for row in csvdata:
        messages.append(row[0])
    return messages

class Command(BaseCommand):
    help = 'Checks and Sends daily message to users'

    def handle(self, *args, **options):
        trial_messages = return_list_from_file('messages_trial.csv')
        main_messages = return_list_from_file('messages_main.csv')
        users = fb_user.objects.all()
        for item in users:
            try:
                print "Sending message to ", item.first_name
                current_day = item.current_day
                if item.first_message == 0:
                    continue
                if current_day >= len(trial_messages):
                    if item.label == 1:
                        send_message_generic(item.fb_id, main_messages[current_day-len(trial_messages)])
                        current_day += 1
                        itemcopy = item
                        itemcopy.current_day = current_day
                        itemcopy.save()
                    continue
                if item.first_message == 1 and current_day == 0:
                    itemcopy = item
                    itemcopy.first_message = 2
                    itemcopy.save()
                    continue
                send_message_generic(item.fb_id, trial_messages[current_day])
                current_day += 1
                itemcopy = item
                itemcopy.current_day = current_day
                itemcopy.save()
            except Exception as e:
                print e
                raise CommandError('Users Errors')

        self.stdout.write('Successfully sent messages "%s"' % "to users")