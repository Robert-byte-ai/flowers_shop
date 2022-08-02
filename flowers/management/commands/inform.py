from django.core.management.base import BaseCommand
import json

from flowers.models import Purchase


class Command(BaseCommand):

    def handle(self, *args, **options):
        purchases = Purchase.objects.select_related('ad__seller__user', 'customer__user').all()
        result = {
            i.ad.seller.user.username:
                {'customers': list({j.customer.user.username for j in purchases if j.ad.seller == i.ad.seller}),
                 'ads_sum': sum(u.ad.price*u.amount for u in purchases if u.ad.seller == i.ad.seller)}
            for i in purchases
        }
        return json.dumps(result)
