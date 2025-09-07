from faker import Faker

faq = Faker()

async def create_short_link(l: int = 5):
    return "".join(faq.random_choices(length=l))