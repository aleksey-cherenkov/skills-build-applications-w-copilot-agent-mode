from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        # Delete dependent objects first
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        # Clear team members before deleting teams and delete safely
        for team in Team.objects.all():
            try:
                team.members.clear()
                team.save()
            except Exception:
                pass
        for team in Team.objects.all():
            if team.id is not None:
                team.delete()
        for user in User.objects.all():
            if user.id is not None:
                user.delete()

        # Create users (superheroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]
        marvel_users = [User.objects.create(**hero) for hero in marvel_heroes]
        dc_users = [User.objects.create(**hero) for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Marvel')
        dc_team = Team.objects.create(name='DC')
        # Assign members by direct assignment to avoid djongo set() issues
        marvel_team.members = marvel_users
        marvel_team.save()
        dc_team.members = dc_users
        dc_team.save()

        # Create activities
        Activity.objects.create(user=marvel_users[0], activity_type='Running', duration=30, calories_burned=300, date=timezone.now())
        Activity.objects.create(user=dc_users[0], activity_type='Cycling', duration=45, calories_burned=450, date=timezone.now())

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity for heroes', difficulty='Hard', suggested_for='Superheroes')
        Workout.objects.create(name='Power Yoga', description='Flexibility and strength', difficulty='Medium', suggested_for='All')

        # Create leaderboard
        Leaderboard.objects.create(team=marvel_team, points=100)
        Leaderboard.objects.create(team=dc_team, points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
