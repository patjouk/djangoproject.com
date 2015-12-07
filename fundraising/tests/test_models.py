import os
from datetime import date

from django.conf import settings
from django.test import TestCase
from PIL import Image

from ..models import DjangoHero


class TestDjangoHero(TestCase):
    def setUp(self):
        kwargs = {
            'approved': True,
            'is_visible': True,
        }
        self.h1 = DjangoHero.objects.create(**kwargs)
        d1 = self.h1.donation_set.create()
        d1.payment_set.create(amount='5', stripe_charge_id='a1')
        self.h2 = DjangoHero.objects.create(**kwargs)
        d2 = self.h2.donation_set.create()
        d2.payment_set.create(amount='15', stripe_charge_id='a2')
        self.h3 = DjangoHero.objects.create(**kwargs)
        d3 = self.h3.donation_set.create()
        d3.payment_set.create(amount='10', stripe_charge_id='a3')
        self.today = date.today()

    def test_thumbnail(self):
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, 'fundraising/logos/'))
        except OSError:  # directory may already exist
            pass
        image_path = os.path.join(settings.MEDIA_ROOT, 'fundraising/logos/test_logo.jpg')
        image = Image.new('L', (500, 500))
        image.save(image_path)
        self.h1.logo = image_path
        self.h1.save()
        thumbnail = self.h1.thumbnail
        self.assertEqual(thumbnail.x, 170)
        self.assertEqual(thumbnail.y, 170)
        os.remove(image_path)
        self.assertTrue(
            os.path.exists(
                thumbnail.url.replace(settings.MEDIA_URL, '{}/'.format(settings.MEDIA_ROOT))
            )
        )

    def test_thumbnail_no_logo(self):
        self.assertIsNone(self.h2.thumbnail)

    def test_name_with_fallback(self):
        hero = DjangoHero()
        self.assertEqual(hero.name_with_fallback, 'Anonymous Hero')
        hero.name = 'Batistek'
        self.assertEqual(hero.name_with_fallback, 'Batistek')