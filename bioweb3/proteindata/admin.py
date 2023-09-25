# # "All code below written by the student."

# # Description of file: Admin page with data tables.

# #-------------LOGINS FOR ADMIN-----------------
# #username: admin
# #password: apple@1234

from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_description')

class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'house_no', 'street', 'city', 'country')

class AppUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organisation', 'status', 'user_address', 'photo')

class ToolAdmin(admin.ModelAdmin):
    list_display = ('tool_id', 'tool_category', 'tool_name', 'tool_description', 'tool_photo', 'tool_location', 'tool_owner')

class BorrowRequestsAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'tool_id', 'borrower', 'acceptance_status')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Tool, ToolAdmin)
admin.site.register(BorrowRequests, BorrowRequestsAdmin)



# # # All the 5 tables of our database:
# # class ProteinDomainLinkAdmin(admin.ModelAdmin):
# #     list_display = ('ProteinDomainLink_id','domain_start','domain_end','protein_id','domain_id')    

# # class ProteinAdmin(admin.ModelAdmin):
# #     list_display = ('protein_id','protein_length','taxonomy','sequence') 

# # class PfamAdmin(admin.ModelAdmin):
# #     list_display = ('pfam_id','pfam_description' )

# # class TaxonomyAdmin(admin.ModelAdmin):
# #     list_display = ('taxa_id', 'clade', 'genus', 'species')

# # class DomainAdmin(admin.ModelAdmin):
# #     list_display = ('domain_id', 'domain_description', 'pfam_link')






# # admin.site.register(ProteinDomainLink, ProteinDomainLinkAdmin)
# # admin.site.register(Pfam, PfamAdmin)
# # admin.site.register(Taxonomy, TaxonomyAdmin)
# # admin.site.register(Domain, DomainAdmin)
# # admin.site.register(Protein, ProteinAdmin)
