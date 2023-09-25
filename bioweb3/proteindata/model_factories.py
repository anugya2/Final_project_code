# I wrote this code

import factory
from .models import *
import factory.faker #Creates random username and email ids
from django_countries.fields import CountryField
from django_countries import countries

class AddressFactory(factory.django.DjangoModelFactory):   
    house_no = "S22"
    street = "Orangevane"
    city = "Columbia"
    country = dict(countries)["NZ"]
    class Meta:
        model = Address
# Create Django users for testing
class UserFactory(factory.django.DjangoModelFactory):    
    username = factory.Faker("name")
    email = factory.Faker("email")
    password ="dehw"
    class Meta:
        model = User

# Create App users for testing
class AppUserFactory(factory.django.DjangoModelFactory):    
    user = factory.SubFactory(UserFactory)
    organisation = "Hobby association society"
    status = "Getting sun on the beach. Enjoying life"
    user_address = factory.SubFactory(AddressFactory)
    photo = "http://127.0.0.1:8080/images/images/test.jpg"
    class Meta:
        model = AppUser

# Create Frienships for testing
class CategoryFactory(factory.django.DjangoModelFactory):
    # Do not initialise frienship_is as it is autoField.
    category_name = factory.Faker("name")
    category_description = "soil and mud and texture"    
    class Meta:
        model = Category

# Create image instances for testing


class ToolFactory(factory.django.DjangoModelFactory):     
    tool_category = factory.SubFactory(CategoryFactory)
    tool_name = "Wood planner"
    tool_description = "Gently used."
    tool_photo = "static/images/tools.png"
    tool_location = factory.SubFactory(AddressFactory)
    tool_owner = factory.SubFactory(AppUserFactory)
    class Meta:
        model = Tool

class BorrowRequestsFactory(factory.django.DjangoModelFactory):     
    tool_id = factory.SubFactory(ToolFactory)
    borrower = factory.SubFactory(AppUserFactory)
    acceptance_status = False
    class Meta:
        model = BorrowRequests

# end of code I wrote
   









