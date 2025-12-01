from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.auth import get_user_model

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear existing data
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index([('email', 1)], unique=True)

        # Teams
        teams = [
            {'name': 'Marvel', 'description': 'Team Marvel Superheroes'},
            {'name': 'DC', 'description': 'Team DC Superheroes'},
        ]
        db.teams.insert_many(teams)

        # Users
        users = [
            {'name': 'Tony Stark', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Steve Rogers', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Bruce Wayne', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Clark Kent', 'email': 'superman@dc.com', 'team': 'DC'},
        ]
        db.users.insert_many(users)

        # Activities
        activities = [
            {'user': 'Tony Stark', 'activity': 'Running', 'duration': 30},
            {'user': 'Steve Rogers', 'activity': 'Cycling', 'duration': 45},
            {'user': 'Bruce Wayne', 'activity': 'Swimming', 'duration': 60},
            {'user': 'Clark Kent', 'activity': 'Flying', 'duration': 120},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'user': 'Tony Stark', 'points': 100},
            {'user': 'Steve Rogers', 'points': 90},
            {'user': 'Bruce Wayne', 'points': 110},
            {'user': 'Clark Kent', 'points': 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Ironman Endurance', 'type': 'Cardio', 'duration': 60},
            {'name': 'Super Strength', 'type': 'Strength', 'duration': 45},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
