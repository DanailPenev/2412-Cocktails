from django.test import TestCase
from cocktails.models import Cocktail

# Create your tests here.
class CocktailModelTests(TestCase):
	
	def test_ensure_slug_works(self):
		c = Cocktail(name="Test Cocktail")
		c.save()
		self.assertEqual((c.slug=="test-cocktail"), True)
		
	def test_ensure_name_notnull(self):
		try:
			c = Cocktail()
			c.save
			self.fail("This should have raised an exception")
		except:
			pass
			
class InstructionModelTests(TestCase):

	def test_instruction_is_deleted_if_cocktail_is_deleted(self):
		c = Cocktail(name="Test")
		c.save()
		pass