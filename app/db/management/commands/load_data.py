import dataset
from django.core.management.base import BaseCommand

import db.models as db
from db.management.spinner import Spinner


class Command(BaseCommand):
    help = "Loads data that has been downloaded and processed by the scraper"

    def add_arguments(self, parser):
        parser.add_argument(
            "db-uri",
            nargs=1,
            help="The uri of the database containing scraped data",
        )

    def fetch_data(self):
        scrape_db = dataset.connect(self.options["db-uri"][0])

        pkf_fields = " pkf.area_name, pkf.description, pkf.location_x, pkf.location_y, pkf.decision, pkf.app_type, pkf.date_received "

        db_result = scrape_db.query(
            f"""
            (SELECT {pkf_fields}, 'RSPB Reserve' as near
            FROM planit p
            JOIN planit_load pl on p.load_id = pl.id
            JOIN planit_key_fields pkf on pkf.id = p.id
            JOIN near_rspb_reserves nr on nr.id = p.id
            )

            UNION

            (SELECT {pkf_fields}, 'IBA'
            FROM planit p
            JOIN planit_load pl on p.load_id = pl.id
            JOIN planit_key_fields pkf on pkf.id = p.id
            JOIN near_ibas nr on nr.id = p.id
            )
            """
        )

        db_dataset = db.Dataset.objects.create()

        batch = []

        for result in db_result:
            result_with_dataset = {"id": None, "dataset": db_dataset}
            result_with_dataset.update(result)
            batch.append(db.PlaningApp(**result_with_dataset))

        db.PlaningApp.objects.bulk_create(batch)

        return len(batch)

    def handle(self, *args, **options):
        self.options = options

        spinner = Spinner()
        spinner.start()

        added = self.fetch_data()

        spinner.stop()
        print(f"\nData loaded: {added}\n", file=self.stdout)
