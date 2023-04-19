from django.db import models


class Court(models.Model):
    courtID = models.IntegerField(primary_key=True)
    x = models.DecimalField(max_digits=9, decimal_places=6)
    y = models.DecimalField(max_digits=9, decimal_places=6)
    city = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    max_players = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.courtID:
            # generate a new unique courtID
            max_court_id = Court.objects.aggregate(models.Max('courtID'))['courtID__max'] or 0
            self.courtID = max_court_id + 1
        super().save(*args, **kwargs)
