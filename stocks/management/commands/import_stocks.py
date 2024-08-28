from django.core.management.base import BaseCommand
from stocks.models import Stock
import csv

class Command(BaseCommand):
    help = 'Import stocks from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                Stock.objects.create(
                    ticker=row['ticker'],
                    company_name=row['company_name'],
                    exchange=row['exchange']
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported stocks from CSV'))