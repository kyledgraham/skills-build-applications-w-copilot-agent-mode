from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data using drop_collection for Djongo compatibility
        from django.db import connection
        db = connection.cursor().db_conn.client[connection.settings_dict['NAME']]
        db['leaderboard'].drop()
        db['activities'].drop()
        db['workouts'].drop()
        db['users'].drop()
        db['teams'].drop()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User(name='Batman', email='batman@dc.com', team=dc),
        ]
        for user in users:
            user.save()

        # Create Workouts
        workouts = [
            Workout(name='Super Strength', description='Strength training for heroes', suggested_for='Marvel'),
            Workout(name='Stealth Moves', description='Stealth and agility drills', suggested_for='DC'),
        ]
        for workout in workouts:
            workout.save()

        # Create Activities
        activities = [
            Activity(user=users[0], type='Web Swinging', duration=30, date=timezone.now().date()),
            Activity(user=users[1], type='Suit Up', duration=45, date=timezone.now().date()),
            Activity(user=users[2], type='Lasso Practice', duration=40, date=timezone.now().date()),
            Activity(user=users[3], type='Detective Work', duration=50, date=timezone.now().date()),
        ]
        for activity in activities:
            activity.save()

        # Create Leaderboard
        leaderboard_entries = [
            Leaderboard(user=users[0], score=100),
            Leaderboard(user=users[1], score=90),
            Leaderboard(user=users[2], score=95),
            Leaderboard(user=users[3], score=85),
        ]
        for entry in leaderboard_entries:
            entry.save()

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
