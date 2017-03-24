from django.test import TestCase
from cocktails.models import Cocktail
from django.core.urlresolvers import reverse
from cocktails.models import *

def add_cocktail(name, rating):
	c = Cocktail.objects.get_or_create(name=name)[0]
	c.rating = rating
	c.save()
	return c

# Create your tests here.
class CocktailModelTests(TestCase):
	
	def test_ensure_slug_works(self):
		c = Cocktail(name="Test Cocktail")
		c.save()
		self.assertEqual(c.slug, "test-cocktail")
		
	def test_ensure_name_notnull(self):
		try:
			c = Cocktail()
			c.save
			self.fail("This should have raised an exception")
		except:
			pass
			
class IndexViewTests(TestCase):
	
	def test_index_view_works(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		
	def test_index_view_with_cocktails(self):
		add_cocktail("Random Name", 5)
		
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Random Name")


class AboutViewTests(TestCase):
        def test_about_view_works(self):
                response = self.client.get(reverse('about'))
                self.assertEqual(response.status_code, 200)
