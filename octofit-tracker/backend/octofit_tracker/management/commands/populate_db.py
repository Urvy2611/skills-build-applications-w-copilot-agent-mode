from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **kwargs):
        # Skipping deletion due to Djongo ObjectId bug. Ensure collections are dropped manually if needed.

        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel superheroes team')
        dc = Team.objects.create(name='DC', description='DC superheroes team')

        # Create users
        users = [
            User(email='tony@stark.com', username='IronMan', team=marvel, is_superhero=True),
            User(email='steve@rogers.com', username='CaptainAmerica', team=marvel, is_superhero=True),
            User(email='bruce@wayne.com', username='Batman', team=dc, is_superhero=True),
            User(email='clark@kent.com', username='Superman', team=dc, is_superhero=True),
        ]
        for user in users:
            user.save()

        # Create activities
        Activity.objects.create(user=users[0], activity_type='Running', duration_minutes=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Cycling', duration_minutes=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type='Swimming', duration_minutes=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Yoga', duration_minutes=20, date=timezone.now().date())

        # Create workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for superheroes')
        w2 = Workout.objects.create(name='Flight Training', description='Flight workout for superheroes')
        w1.suggested_for.set([users[0], users[2]])
        w2.suggested_for.set([users[1], users[3]])

        # Create leaderboards
        Leaderboard.objects.create(team=marvel, total_points=100, rank=1)
        Leaderboard.objects.create(team=dc, total_points=90, rank=2)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
