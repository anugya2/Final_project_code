# "All code below written by the student."

# Description of file: Stores all django view classes. For now we have only view for the page that is 
# used to add protein and a main page spa class.

#Importing all used models:
from django.shortcuts import render
from typing import Any, Dict
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from .forms import *
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required



def index(request):
    if request.user.is_authenticated:
        djangouser = request.user # get django user 
        user = AppUser.objects.get(user = djangouser) # get Appuser data corresponding to our django user
        pk= user.pk    #primary key of AppUser instance
        return render(request, 'proteindata/index.html', {'pk': pk })                 
    else:        
        return render(request, 'proteindata/index.html') 

def register(request):        
    registered = False #Initilise this variable as false
    # After registration form is filled and posted
    if request.method == 'POST':        
        user_form = UserForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST, request.FILES)
        address_form = AddressForm(request.POST, request.FILES)
        # Validation of form
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            add = address_form.save()
            add.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_address = add
            
            # if 'organisation' in user_form.cleaned_data:
            #     profile.organisation = request.DATA['organisation']
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors, address_form.errors)
    else:        
        user_form = UserForm()
        profile_form = UserProfileForm()
        address_form = AddressForm()
    return render(request, 'proteindata/register.html',
                  {'user_form': user_form,
                    'profile_form': profile_form,
                    'address_form':address_form,
                    'registered': registered ,})

# View for Login functionality
def user_login(request):
    master_genes = AppUser.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("../")
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'proteindata/login.html', {'master_genes': master_genes})

@login_required  
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')

@login_required  
def home(request):
    djangouser = request.user
    user = AppUser.objects.get(user = djangouser)
    name = djangouser.username
    organisation = user.organisation
    status= user.status
    photo = user.photo
    pk = user.pk 
    photoForm = PhotoForm()
    toolForm = ToolForm()
    categoryForm = CategoryForm()
    addressForm = AddressForm()
    toolList = Tool.objects.all()
    userToolList = Tool.objects.filter(tool_owner = user)
    
    # user specific tools/ ONly for pickup not initiated
    
    tool_request_tuple_list = []
    for tool in userToolList: 
        br_list = BorrowRequests.objects.filter(tool_id= tool)       
        for borrowRequests in br_list: 
            if  borrowRequests.acceptance_status == False:       
                tool_request_tuple_list.append([tool,borrowRequests])    
    
    # For accepted borrow request/ chat with borrower to arrange pickup.
    accepted_tool_borrowRequest_list = []
    for tool in userToolList: 
        br_list = BorrowRequests.objects.filter(tool_id= tool)       
        for borrowRequests in br_list: 
            if  borrowRequests.acceptance_status == True:    
                accepted_tool_borrowRequest_list.append([tool,borrowRequests]) 

    # outgoing_request_list = BorrowRequests.objects.filter(tool_id= tool)
    accepted_outgoing_request_list = BorrowRequests.objects.filter(borrower= user,acceptance_status = True)
    pending_outgoing_request_list = BorrowRequests.objects.filter(borrower= user,acceptance_status= False )

    # render page with relevant data
    return render(request, 'proteindata/home.html', {  'user_name': name,
                                                'user_organisation':organisation,
                                                'user_status':status,
                                                'user_photo':photo,
                                                "pk": pk,
                                                "photoForm":photoForm,
                                                "toolForm":toolForm,
                                                "categoryForm":categoryForm,
                                                "addressForm": addressForm,
                                                "toolList":toolList,
                                                "userToolList":userToolList,
                                                "tool_request_tuple_list" : tool_request_tuple_list,
                                                "accepted_tool_borrowRequest_list": accepted_tool_borrowRequest_list,
                                                "accepted_outgoing_request_list": accepted_outgoing_request_list,
                                                "pending_outgoing_request_list" : pending_outgoing_request_list,
                                                
                                               })

def update_status(request):
    #Get AppUser data based on Django User
    user = AppUser.objects.get(user = request.user)
    if request.method == 'POST':        
        status = request.POST['status'] #Posted status content
        user.status = status
        user.save()  # Saving record in the data model      
        return HttpResponseRedirect("../home/")
    
def update_organisation(request):   
    user = AppUser.objects.get(user = request.user)
    if request.method == 'POST':        
        organisation = request.POST['organisation'] 
        user.organisation= organisation
        user.save()    
        return HttpResponseRedirect("../home/")
def update_address(request):   
    user = AppUser.objects.get(user = request.user)
    if request.method == 'POST':        
        home_no = request.POST['home_no'] 
        street = request.POST['street'] 
        city = request.POST['home_no'] 
        country = user.address.country
        row= Address.objects.create(home_no = home_no,
                                    street = street,
                                    city = city,
                                    country = country,
                                    )
        row.save()
        user.address= row
        user.save()    
        return HttpResponseRedirect("../home/")
def update_photo(request): 
    user = AppUser.objects.get(user = request.user)
    if request.method == 'POST':        
        photoForm = PhotoForm(request.POST, request.FILES)
        if photoForm.is_valid():
            if 'photo' in photoForm.cleaned_data:
                user.photo = request.FILES.get('photo')
            user.save()
        else:
            print(photoForm.errors)
    
    else:
        photoForm = PhotoForm()           
    return HttpResponseRedirect("../home/")

def add_category(request): 
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category = category_form.save()
            category.save()
    return HttpResponseRedirect("../home/")

def add_tool(request): 
    user = AppUser.objects.get(user = request.user)

    if request.method == 'POST':
        tool_location ={}
        tool_location_form = AddressForm(request.POST, request.FILES)
        if tool_location_form.is_valid():
            tool_location = tool_location_form.save()
            tool_location.save()
        else:
            print(tool_location_form.errors)        

        tool_form = ToolForm(request.POST, request.FILES)
        if tool_form.is_valid():
            tool = tool_form.save(commit=False)
            tool.tool_owner = user
            tool.tool_location = tool_location
            tool.save()
        else:
            print(tool_form.errors)
    return HttpResponseRedirect("../home/")

@login_required         
def inventory(request):
    djangouser = request.user # get django user 
    user = AppUser.objects.get(user = djangouser)
    toolList = Tool.objects.all()
    categories = Category.objects.all()
    category_search_results = None

    # tool_request_tuple_list = []
    # for tool in toolList:
    #     tool_request_tuple_list.append((tool, BorrowRequests.objects.filter(tool_id= tool)))
    # "tool_request_tuple_list":tool_request_tuple_list

    return render(request, 'proteindata/inventory.html',{"toolList":toolList,
                                                         "categories":categories,
                                                         "category_search_results": category_search_results
                                                         }) 

@login_required 
def send_borrow_request(request):
    djangouser = request.user # get django user 
    user = AppUser.objects.get(user = djangouser)
    if request.method == 'POST':
        tool_id = request.POST['tool_id'] 
        tool_from_id = Tool.objects.get(tool_id = tool_id)

        try:
            test_request = BorrowRequests.objects.get(tool_id= tool_from_id,
                                                    borrower = user) 
            return HttpResponse("You have sent this request before.") 
        except:
            row= BorrowRequests.objects.create(tool_id= tool_from_id,
                                                borrower = user,
                                                acceptance_status = False)
            row.save()        
        return HttpResponse("Borrow request has been sent")

def request_acceptance (request):
    if request.method == 'POST':
        # Each borrow request has a unique id
        request_id = request.POST['request_id']
        print(request_id)
        borrowRequest = BorrowRequests.objects.get(request_id = request_id)
        borrowRequest.acceptance_status = True # change status of acceptance to confirmed
        borrowRequest.save()
        return HttpResponseRedirect("../home/") 

def room(request, room_name):
    return render(request, 'proteindata/room.html', {'room_name': room_name })
    
def category_search(request):
    toolList = Tool.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':       
        category = request.POST['category']
        category_search_results = Tool.objects.filter(tool_category = category )        
        return render(request, 'proteindata/inventory.html', {"toolList":toolList,
                                                         "categories":categories,
                                                        'category_search_results': category_search_results, 
                                               })

def people(request):
    master_users = AppUser.objects.all() # Get list of all users in the database
    return render(request, 'proteindata/people.html', {'master_users': master_users,
                                               })

def delete(request):
    if request.method == 'POST':
        # Each borrow request has a unique id
        tool_id = request.POST['tool_id']
        tool = Tool.objects.get(tool_id=tool_id)
        BorrowRequests.objects.filter(tool_id=tool).delete()
        Tool.objects.filter(tool_id=tool_id).delete()        
        return HttpResponseRedirect("../home/")  

 