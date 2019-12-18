from django.test import TestCase

from rlcis.models import Reviewer

# Create your tests here.

class Test_Reviewer_Model(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Reviewer.objects.create(first_name='Robert', last_name='Lange', employee_id = 10)

    def test_first_name_label(self):
        reviewer = Reviewer.objects.get(id=1)
        field_label = reviewer._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')
        
    def test_first_name_max_length(self):
        reviewer = Reviewer.objects.get(id=1)
        max_length = reviewer._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 60)

    def test_last_name_label(self):
        reviewer = Reviewer.objects.get(id=1)
        field_label = reviewer._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')
        
    def test_last_name_max_length(self):
        reviewer = Reviewer.objects.get(id=1)
        max_length = reviewer._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 60)

    def test_employee_id(self):
        reviewer = Reviewer.objects.get(id=1)
        max_length = reviewer._meta.get_field('employee_id')
        self.assertTrue(10 <= 100 <= 1000)

    def test_object_name_is_last_name_comma_first_name(self):
       reviewer = Reviewer.objects.get(id=1)
       expected_object_name = f'{reviewer.last_name}, {reviewer.first_name}'
       self.assertNotEquals(expected_object_name, str(reviewer))
