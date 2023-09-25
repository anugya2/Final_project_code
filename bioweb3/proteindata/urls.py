# "All code below written by the student."

# Description of file: contains urls for all the api edpoints , and the add-protein-entry page , 
# and the main index page

#Imports:
from django.urls import include, path
from . import views
from . import api
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import api
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',  views.user_logout, name='logout'),
    path('home/',  views.home, name='home'),
    path('inventory/', views.inventory, name='inventory'),
    # path('people/',  views.people, name='people'),
    # path('tools/',  views.tools, name='tools'),
    path ('api/userData/<int:pk>', api.AppUserDetail.as_view(), name = 'user_details_api') ,
    path ('api/toolData/<str:tool_name>', api.ToolDetails.as_view(), name = 'tool_details_api') ,
    path ('api/borrowRequestsData/<int:request_id>', api.BorrowRequestsD.as_view(), name = 'borrowRequestsData_api') ,

    path('update_status/', views.update_status, name='update_status'),
    path('update_organisation/', views.update_organisation, name='update_organisation'),
    path('update_address/', views.update_address, name='update_address'),
    path('update_photo/', views.update_photo, name='update_photo'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_tool/', views.add_tool, name='add_tool'),
    path('send_borrow_request/', views.send_borrow_request, name='send_borrow_request'),
    path('request_acceptance/', views.request_acceptance, name='request_acceptance'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('category_search/', views.category_search, name='category_search'),
    path('people/', views.people, name='people'),
    path('delete/', views.delete,name='delete' )

    


    # front page - Main index page with api endpoint hyperlinks
    # path ('', views.front_page, name = 'front_page') ,
    # path ('api/user/', views.create_user, name = 'create_user') , 
    # path ('api/inventory_list_page/', views.inventory_list_page, name = 'inventory_list_page') ,
    # path ('api/tool/<int:tool_id>', api.ToolDetails.as_view(), name = 'tool_details_api') ,
    # path ('api/toolList', api.ToolList.as_view(), name = 'tool_list_api') ,
    # path ('api/filter_tools/<str:category_name>', api.FilteredToolList.as_view(), name = 'filtered_tool_list_api') ,

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # 1st api endpoint - page to add protein entry to protein table.
    # "Simple protein entry"
    # Green page to add protein entry. uses forms and validators and also has a list of proteins.
    # path ('api/protein/', views.create_protein, name = 'create_protein') , 

    # # 2nd api endpoint: return the protein sequence and all we know about it
    # # You can also POST protein entry and all complex details in the same format at the bottom of the page.
    # path('api/protein/<str:protein_id>/', api.ProteinDetails.as_view(), name='protein_details_api'), 

    # # 3rd api endpoint that returns the domain and its description based on pfam_id or domain_id.
    # path('api/pfam/<str:pfam_id>/', api.PfamDetail.as_view(), name = 'pfam_api'),

    # # 4th api endpoint for listing all proteins related to the specified organism.
    # path('api/proteins/<int:taxa_id>/', api.OrganismProteins.as_view(), name = 'organism_proteins_api'),

    # # 5th api endpoint for listing all domains associated with all proteins of the specified organism.
    # path('api/pfams/<int:taxa_id>/', api.OrganismDomains.as_view(), name = 'organism_domains_api'),  

    # # 6th api endpoint for calculating coverage. 
    # path('api/coverage/<str:protein_id>/',api.calculate_coverage, name="calculate_coverage"),

    # #Lists all proteins
    # path('api/proteins/', api.ProteinList.as_view(), name = 'protein_list_api'),

    # # Main spa page
    # path('app/', views.SPA, name = "spa") ,      
]

#______________________________________________________________END_______________________________________________________________________________





# Has just the post method, can enter complex protein entries 
    # this should be the add-protein-entry page and not the simple one. 
    # put things from POST method of protein-details page here instead.
    # path('api/protein/', api.Protein.as_view(), name = 'protein_post_api'), 


# Doeent get anything, but the post api has all the fields.
# path('api/protein1/<str:protein_id>/', api.ProteinFullDetails.as_view(), name = 'protein1_post_api'),