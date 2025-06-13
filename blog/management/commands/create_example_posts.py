from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import BlogPost
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates example blog posts'

    def handle(self, *args, **kwargs):
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Created superuser "admin"'))

        admin = User.objects.get(username='admin')

        # Example blog posts
        example_posts = [
            {
                'title': 'My First Violin Lesson! 🎻',
                'content': '''Hey everyone! Today was my first violin lesson and it was AMAZING! 🎵 

I was so nervous at first, but my teacher is super nice and patient. We started with the basics - how to hold the violin and bow correctly. It felt a bit awkward at first, but I'm getting the hang of it!

The best part was when we played our first note together. It wasn't perfect (far from it actually 😅), but it was so exciting to make music! 

I can't wait for my next lesson! Does anyone else play the violin? Let me know your tips for beginners! 💕'''
            },
            {
                'title': 'Swimming Competition Success! 🏊‍♀️',
                'content': '''OMG guys! I just had my first swimming competition and it was INCREDIBLE! 

I was so nervous before the race, but once I got in the water, it was like everything else disappeared. I focused on my breathing and technique, just like my coach taught me.

And guess what? I came in second place! 🥈 I'm so proud of myself! The girl who won was amazing, and I'm actually happy I got to race against her - it pushed me to swim faster than ever before.

Next competition is in two weeks, and I'm already training hard! Wish me luck! 💪'''
            },
            {
                'title': 'New Art Project: Watercolor Cats! 🎨',
                'content': '''I've been obsessed with watercolors lately, and I decided to combine my two favorite things: painting and cats! 

I started with my own cat, Whiskers, as a model. It took me three tries to get it right, but I'm really happy with how it turned out! The way the colors blend in watercolor is just magical.

I'm thinking of making a whole series of cat portraits. Maybe I'll even start taking commissions from my friends! 

Do you guys like to paint? What's your favorite medium? Let me know in the comments! 💖'''
            }
        ]

        # Create the posts
        for post_data in example_posts:
            if not BlogPost.objects.filter(title=post_data['title']).exists():
                BlogPost.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    author=admin,
                    created_at=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(f'Created post: {post_data["title"]}')) 