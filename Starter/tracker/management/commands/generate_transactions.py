import random
from faker import Faker
from django.core.management.base import BaseCommand
from tracker.models import User, Category, Transaction


class Command(BaseCommand):
    help = "Generate random transactions for testing purposes"

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()
        categories = Category.objects.all()
        if not categories.exists():
            categories = [
                "Bills",
                "Food",
                "Clothes",
                "Medical",
                "Housing",
                "Salary",
                "Social",
                "Entertainment",
                "Transport",
                "Vacation",
                "Other",
            ]
            for category_name in categories:
                Category.objects.get_or_create(name=category_name)
            
            categories = Category.objects.all()


        if not users.exists():
            self.stdout.write(self.style.ERROR("Please create some users first."))
            return

        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES
                 ]
        for _ in range(100):  # Generate 100 random transactions
            user = random.choice(users)
            category = random.choice(categories)
            transaction_type = random.choice(types)
            amount = round(random.uniform(1.00, 2500.00), 2)
            date = fake.date_between(start_date="-1y", end_date="today")

            Transaction.objects.create(
                user=user,
                category=category,
                type=transaction_type,
                ammount=amount,
                date=date,
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully generated random transactions.")
        )
