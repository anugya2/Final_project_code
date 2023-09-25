# "All code below written by the student."

# Description of file: Contains unit tests for all api endpoints.

from django.test import TestCase
from .serializers import *
import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from .model_factories import *
from .serializers import *

# 6 tests for our apis
# 6 test for our serialisers

# custom function to avoid repitition;
def deleteObj(self):
    User.objects.all().delete()
    AppUser.objects.all().delete()
    Category.objects.all().delete()
    AppUser.objects.all().delete()
    Tool.objects.all().delete()
    BorrowRequests.objects.all().delete()

class ToolDetailsTest(APITestCase):

    tool1 = None
    tool2 = None
    good_url = ''
    bad_url = ''
    delete_url = ''

    def setUp(self):
        self.tool1 = ToolFactory.create(tool_name="scythe")
        self.tool2  = ToolFactory.create(tool_name="cutter")
        self.tool3  = ToolFactory.create(tool_name="slicer")        
        self.good_url = reverse('tool_details_api', kwargs={'tool_name': "scythe"})
        self.bad_url = "/api/toolData/H/"
        self.delete_url = reverse('tool_details_api', kwargs={'tool_name': "slicer"})

    def tearDown(self):
        deleteObj(self)

    def test_toolDetailReturnsSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200) # 404 is incorrect/ error, 200 is correct/success
        data = json.loads(response.content)
        self.assertTrue('tool_category' in data)
        self.assertEqual(data['tool_description'],"Gently used.")

    def test_toolDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)    

class UserDataTest(APITestCase): 
    user1 = None
    user2 = None
    good_url = ''
    bad_url = ''
    delete_url = ''

    def setUp(self):
        self.user1 = AppUserFactory.create(user=UserFactory.create(username ="Dolly"))
        self.user2  = AppUserFactory.create(user=UserFactory.create(username ="Molly"))
        self.user3  = AppUserFactory.create(user=UserFactory.create(username ="Sally"))                
        self.good_url = reverse('user_details_api', kwargs={'pk':  1})
        self.bad_url = "api/userData/H/"
        self.delete_url = reverse('user_details_api', kwargs={'pk': 2})

    def tearDown(self):
        deleteObj(self)

    # Checks if expected data is returned
    def test_userDetailReturnsSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200) # 404 is incorrect/ error, 200 is correct/success
        data = json.loads(response.content)
        self.assertTrue('status' in data)
        self.assertEqual(data['organisation'], "Hobby association society")

    # Expected failure used as a control
    def test_userDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

class BorrowRequestTest(APITestCase): 
    req1 = None
    req2 = None
    good_url = ''
    bad_url = ''
    delete_url = ''

    def setUp(self):
        self.req1 = BorrowRequestsFactory.create(tool_id=ToolFactory.create(tool_name ="saw"))
        self.req2  = BorrowRequestsFactory.create(tool_id=ToolFactory.create(tool_name ="cutter"))
        self.req3  = BorrowRequestsFactory.create(tool_id=ToolFactory.create(tool_name ="needles"))                
        self.good_url = reverse('borrowRequestsData_api', kwargs={'request_id':  1})
        self.bad_url = "api/borrowRequestsData/H/"
        self.delete_url = reverse('borrowRequestsData_api', kwargs={'request_id': 2})

    def tearDown(self):
        deleteObj(self)

    # Checks if expected data is returned
    def test_requestDetailReturnsSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200) # 404 is incorrect/ error, 200 is correct/success
        data = json.loads(response.content)
        self.assertTrue('borrower' in data)
        self.assertEqual(data['acceptance_status'], False)

    # Expected failure used as a control
    def test_requestDetailReturnFailOnBadPk(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

class UserDataSerializerTest(APITestCase):
    # Initialising User instance and user data serialiaser
    user = None
    userserializer = None
    def setUp(self):
        self.user = AppUserFactory.create()
        self.userserializer = AppUserSerializer(instance=self.user )

    # Emptying test database
    def tearDown(self):
        deleteObj(self)

    # Data attributes as expected
    def test_userDataSerilaiser(self): 
        data = self.userserializer.data
        self.assertEqual(set(data.keys()), set(['user', 'organisation', 'status', 'user_address', 'photo']))

    # Data values as expected
    def test_userDataSerilaiseruserIDIsHasCorrectData(self):
        data = self.userserializer.data
        self.assertEqual(type(data['organisation']), str) 




class ToolSerialiserTest(APITestCase):
    tool1 = None
    toolserializer = None

    def setUp(self):
        self.tool1 = ToolFactory.create(tool_name="saw")
        self.toolserializer  = ToolSerializer(instance=self.tool1 )

    def tearDown(self):
        deleteObj(self)

    def test_toolSerilaiser(self): 
        data = self.toolserializer.data
        self.assertEqual(set(data.keys()), set(['tool_id', 'tool_category', 'tool_name', 'tool_description',
                                        'tool_photo', 'tool_location', 'tool_owner']))

    def test_toolSerilaisertoolIDIsHasCorrectData(self):
        data = self.toolserializer.data
        self.assertEqual(data['tool_name'], "saw") 

class BorrowRequestSerialiserTest(APITestCase):
    req1 = None
    reqserializer = None

    def setUp(self):
        self.req1 = BorrowRequestsFactory.create(tool_id=ToolFactory.create(tool_name ="saw"))
        self.reqserializer  = BorrowRequestsSerializer(instance=self.req1)

    def tearDown(self):
        deleteObj(self)

    def test_requestSerilaiser(self): 
        data = self.reqserializer.data
        self.assertEqual(set(data.keys()), set(['request_id', 'tool_id', 'borrower', 'acceptance_status']))

    def test_requestSerilaisertoolIDIsHasCorrectData(self):
        data = self.reqserializer.data
        self.assertEqual(data['acceptance_status'], False)   


