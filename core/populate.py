import os
import random
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "planner.settings")

from django import setup
setup()

from django.contrib.auth.models import User
from django.utils import timezone

from core.models import Tag, Item

DEBUG = False
DEFAULT_EMAIL = "abc@xyz.com"
DEFAULT_PASSWORD = "password"
USER_COUNT = 5
TAGS_PER_USER = 5
SEED = 12345  # Seed used for generating item datetimes and tag assignments.
ITEMS_PER_USER = 30
MAX_TAGS_PER_ITEM = 3
MAX_ITEM_DATE_DELTA_FROM_NOW = 10
MAX_ITEM_DURATION_HOURS = 4

def clear():
    Item.objects.all().delete()
    Tag.objects.all().delete()
    User.objects.all().delete()
    print("Database cleared.")

def populate():
    populate_users(USER_COUNT)
    print("Users populated.")
    populate_tags(TAGS_PER_USER)
    print("Tags populated.")
    populate_items(SEED, ITEMS_PER_USER)
    print("Items populated.")
    print("Database populated.")

def populate_users(user_count):
    for i in range(user_count):
        username = f"user{i}"
        user = User.objects.create_user(
            username=username,
            email=DEFAULT_EMAIL,
            password=DEFAULT_PASSWORD
        )
        if DEBUG: print(f"User {user} created.")

def populate_tags(tags_per_user):
    users = User.objects.all()

    if not users:
        raise Exception("Tags can only be populated if users exist.")

    for user in users:
        for i in range(tags_per_user):
            tag_name = f"tag{i}"
            random_colour = random.choice(list(Tag.Colour.values))
            tag = Tag.objects.create(
                user=user,
                name=tag_name,
                colour=random_colour
            )
            if DEBUG: print(f"Tag {tag} created for user {user}.")

def populate_items(seed, items_per_user):
    random.seed(seed)

    users = User.objects.all()

    if not users:
        raise Exception("Items can only be populated if users exist.")

    for user in users:
        user_tags = list(Tag.objects.filter(user=user))

        for i in range(items_per_user):
            name = f"item{i}"
            random_is_complete = random.choice([True, False])
            random_start = timezone.now() + timedelta(days=random.randint(-MAX_ITEM_DATE_DELTA_FROM_NOW, MAX_ITEM_DATE_DELTA_FROM_NOW))
            random_end = random_start + timedelta(hours=random.randint(0, MAX_ITEM_DURATION_HOURS))
            item = Item(
                user=user,
                name=name,
                is_complete=random_is_complete,
                start_datetime=random_start,
                end_datetime=random_end
            )
            item.full_clean()
            item.save()
            if DEBUG: print(f"Item {item} created for user {user}.")

            tag_count = min(MAX_TAGS_PER_ITEM, len(user_tags))
            random_tag_sample = random.sample(
                user_tags,
                k=random.randint(0, tag_count)
            )
            item.tags.set(random_tag_sample)
            if DEBUG: print(f"{tag_count} tags assigned to item {item}.")

if __name__ == "__main__":
    clear()
    populate()
