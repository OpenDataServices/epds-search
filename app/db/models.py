from django.db import models


# This is the canonical data model, any changes here may need changes in:
# 1) [elastic] documents, signals
# 2) [db] load_scrape_data
# 3) [api] views, serializers
# 4) [ui] index
# 5) [main] settings.CSV_USER_DUMP_FIELDS


class Dataset(models.Model):
    datetime = models.DateTimeField(auto_now=True)


class PlaningApp(models.Model):
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, null=True, blank=True
    )
    area_name = models.TextField(null=True)
    description = models.TextField(null=True)
    location_x = models.FloatField(null=True)
    location_y = models.FloatField(null=True)
    near = models.TextField(null=True)
    decision = models.TextField(default="Unknown", null=True)
    app_type = models.TextField(null=True)
    date_received = models.DateField(null=True)
