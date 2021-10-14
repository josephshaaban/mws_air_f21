from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = ""
    url_list = [
        'https://www.who.int/news-room/q-a-detail/coronavirus-disease-covid-19-'
        'food-safety-and-nutrition',
        'https://www.who.int/ar/news-room/q-a-detail/food-safety-and-nutrition',
    ]

    def handle(self, *args, **options):
        for url in self.url_list:
            self.stdout.write(f'Scraping from: {url}')
            self.stdout.write('fading data into database tables..')
