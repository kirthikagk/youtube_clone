from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from videos.models import Video, Comment, Like, UserProfile
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with sample data'
    
    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create sample users
        users = []
        for i in range(5):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'User',
                    'last_name': f'{i+1}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                UserProfile.objects.create(
                    user=user,
                    bio=f'This is {username}\'s bio'
                )
            users.append(user)
        
        # Create sample videos
        video_data = [
            {
                'title': 'Introduction to Python Programming',
                'description': 'Learn the basics of Python programming in this comprehensive tutorial.',
                'tags': ['python', 'programming', 'tutorial'],
                'views': random.randint(100, 10000)
            },
            {
                'title': 'Web Development with Django',
                'description': 'Build modern web applications using Django framework.',
                'tags': ['django', 'web development', 'python'],
                'views': random.randint(100, 10000)
            },
            {
                'title': 'Machine Learning Basics',
                'description': 'Understanding the fundamentals of machine learning.',
                'tags': ['machine learning', 'AI', 'data science'],
                'views': random.randint(100, 10000)
            },
            {
                'title': 'JavaScript ES6 Features',
                'description': 'Explore modern JavaScript features introduced in ES6.',
                'tags': ['javascript', 'ES6', 'web development'],
                'views': random.randint(100, 10000)
            },
            {
                'title': 'Building REST APIs',
                'description': 'Learn how to build RESTful APIs from scratch.',
                'tags': ['API', 'REST', 'backend'],
                'views': random.randint(100, 10000)
            },
        ]
        
        videos = []
        for i, data in enumerate(video_data):
            video, created = Video.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'user': users[i % len(users)],
                    'tags': data['tags'],
                    'views': data['views'],
                    'upload_date': timezone.now() - timedelta(days=random.randint(1, 30))
                }
            )
            videos.append(video)
        
        # Create sample comments
        comment_texts = [
            'Great video! Very helpful.',
            'Thanks for the tutorial!',
            'Can you make more videos like this?',
            'Excellent explanation!',
            'This helped me a lot, thank you!',
        ]
        
        for video in videos:
            for _ in range(random.randint(2, 5)):
                Comment.objects.get_or_create(
                    video=video,
                    user=random.choice(users),
                    content=random.choice(comment_texts),
                    defaults={
                        'created_at': timezone.now() - timedelta(hours=random.randint(1, 48))
                    }
                )
        
        # Create sample likes/dislikes
        for video in videos:
            for user in random.sample(users, random.randint(1, len(users))):
                Like.objects.get_or_create(
                    video=video,
                    user=user,
                    defaults={
                        'is_like': random.choice([True, True, True, False])  # More likes than dislikes
                    }
                )
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
