# "All code below written by the student."

# Description of file: Model for the database.

# ORM model of the data

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Hobby category liek sewing, carpentry
class Category(models.Model):    
    category_name =  models.CharField(max_length=256,primary_key = True, null=False, blank=False)
    category_description = models.CharField(max_length=1056, null=False, blank=False)
    def __str__(self):
        return str(self.category_name)
    
class Address(models.Model):
    address_id =  models.AutoField(auto_created = True, primary_key = True, serialize = False) 
    house_no =  models.CharField(max_length=256, null=False, blank=False)
    street = models.CharField(max_length=556, null=False, blank=False)
    city = models.CharField(max_length=256, null=False, blank=False)
    country = CountryField()
    def __str__(self):
        return str(self.address_id)
    
class AppUser(models.Model):
    # Relates to Django User object.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.CharField(max_length=256, null=True, blank=True)
    # Changeable and can be added later
    status = models.CharField(max_length=1256, null=True, blank=True)
    user_address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)     
    photo = models.ImageField(upload_to='proteindata/static/profilePics/', null=True, blank=True)

    def __unicode__(self):
        return self.user.username    
    

class Tool(models.Model):
    tool_id = models.AutoField(auto_created = True, primary_key = True, serialize = False) 
    tool_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tool_name = models.CharField(max_length=256, null=False, blank=False)
    tool_description =  models.CharField(max_length=1056, null=False, blank=False)
    tool_photo = models.ImageField(upload_to='proteindata/static/toolPics/', null=True, blank=True)
    tool_location = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    tool_owner = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING)
    def __str__(self):
        return str(self.tool_id)
    

class BorrowRequests(models.Model):
    request_id = models.AutoField(auto_created = True, primary_key = True, serialize = False)
    tool_id = models.ForeignKey(Tool, on_delete=models.DO_NOTHING)
    borrower = models.ForeignKey(AppUser, on_delete=models.DO_NOTHING)
    acceptance_status = models.BooleanField(null=False, blank=True)
    def __str__(self):
        return str(self.request_id)






# Pfam/Domain table: contains only the id and description. Unique entries.
# class Pfam(models.Model):
#     pfam_id = models.CharField(max_length=13, null=False, blank=False)
#     pfam_description = models.CharField(max_length=256, null=False, blank=False)
#     def __str__(self):
#         return str(self.pfam_id)

# # Organism/ Taxonomy table: each row is one unique organism and its id, glade and scientific name.
# class Taxonomy(models.Model):
#     taxa_id = models.IntegerField(null=False, blank=True)
#     clade = models.CharField(max_length=1, null=False, blank=False)
#     genus = models.CharField(max_length=256, null=False, blank=False)
#     species = models.CharField(max_length=256, null=False, blank=False)    
#     def __str__(self):
#         return str(self.taxa_id)   

# # Protein table: Unique protien entries and data about id, sequence, length and the organism it belongs to.
# # Forein key relation to Taxonomy table
# class Protein(models.Model):    
#     protein_id = models.CharField(max_length=10, null=False, blank=False) 
#     sequence = models.CharField(max_length=40001)#sometime null, max length 40001 
#     protein_length = models.IntegerField(null=False, blank=True)    
#     taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)     
#     def __str__(self):
#         return str(self.protein_id)
    
    
    
    
# # Domain table: Unique domain ids 
# # Many to many relationship to protein table through "ProteinDomainLink" table.
# # Foreign key to Pfam table.
# class Domain(models.Model):
#     domain_id =  models.CharField(max_length=13, null=False, blank=False)    
#     domain_description = models.CharField(max_length=256)       
#     pfam_link= models.ForeignKey(Pfam, on_delete=models.DO_NOTHING)
#     protein = models.ManyToManyField(Protein, through='ProteinDomainLink') 
#     def __str__(self):
#        return self.domain_id

# # Protein-Domain_Link Table:
# # Stores all many to many protein/domain connections along with associated domain location
# # Foreign keys to both Protein table and Domain table
# class ProteinDomainLink(models.Model):    
#     ProteinDomainLink_id = models.IntegerField(null=False, blank=True)
#     domain_start = models.IntegerField(null=False, blank=True)
#     domain_end = models.IntegerField(null=False, blank=True)
#     protein_id = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)
#     domain_id = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)
#     def __str__(self):
#        return str(self.ProteinDomainLink_id)                            
    

    

#______________________________________________________________END_______________________________________________________________________________  




# Below are 2 other database designs considered prior to the above model.

#latest old .......................................................................................
# from django.db import models

# class Pfam(models.Model):
#     domain_id = models.CharField(max_length=7, null=False, blank=False)
#     domain_description = models.CharField(max_length=256, null=False, blank=False)
#     def __str__(self):
#         return self.domain_id


# class Taxonomy(models.Model):
#     taxa_id = models.IntegerField(null=False, blank=True)
#     clade = models.CharField(max_length=1, null=False, blank=False)
#     genus = models.CharField(max_length=256, null=False, blank=False)
#     species = models.CharField(max_length=256, null=False, blank=False)    
#     def __str__(self):
#         return self.taxa_id


# #Main class
# class Protein(models.Model):
#     # protein_id = models.ForeignKey(ProteinProduct, on_delete=models.DO_NOTHING) 
#     protein_id = models.CharField(max_length=10, null=False, blank=False, db_index=True)  
#     taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING) 
#     protein_length = models.IntegerField(null=False, blank=True) 
    
#     # domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING) 
    
#     def __str__(self):
#         return self.protein_id
    

# class ProteinProduct(models.Model):
#     # protein_product_id = models.CharField(max_length=10, null=False, blank=False) 
#     protein_product_id = models.ForeignKey(Protein, on_delete=models.CASCADE)       
#     sequence = models.CharField(max_length=40001)#sometime null, max length 40001
     
#     def __str__(self):
#         return self.protein_product_id
    

# class Domain(models.Model):
#     pfam = models.ForeignKey(Pfam, on_delete=models.DO_NOTHING) 
#     description = models.CharField(max_length=256)
#     start = models.IntegerField(null=False, blank=True)
#     stop = models.IntegerField(null=False, blank=True)
#     protein = models.ManyToManyField(Protein, through='ProteinDomainLink')
#     def __str__(self):
#        return self.pfam+":"+self.description


# class ProteinDomainLink(models.Model):
#     protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)
#     domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)








# older one>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# File written by student:

# from django.db import models

# class Pfam(models.Model):
#     domain_id = models.CharField(max_length=7, null=False, blank=False)
#     domain_description = models.CharField(max_length=256, null=False, blank=False)
#     def __str__(self):
#         return self.domain_id


# class Taxonomy(models.Model):
#     taxa_id = models.IntegerField(null=False, blank=True)
#     clade = models.CharField(max_length=1, null=False, blank=False)
#     genus = models.CharField(max_length=256, null=False, blank=False)
#     species = models.CharField(max_length=256, null=False, blank=False)    
#     def __str__(self):
#         return self.taxa_id


# #Main class
# class Protein(models.Model):
#     # protein_id = models.ForeignKey(ProteinProduct, on_delete=models.DO_NOTHING) 
#     protein_id = models.CharField(max_length=10, null=False, blank=False, db_index=True)  
#     taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING) 
#     # domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING) 
#     def __str__(self):
#         return self.protein_id
    

# class ProteinProduct(models.Model):
#     # protein_product_id = models.CharField(max_length=10, null=False, blank=False) 
#     protein_product_id = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)       
#     sequence = models.CharField(max_length=20)#sometime null, max length 20
#     length = models.IntegerField(null=False, blank=True)  
#     def __str__(self):
#         return self.protein_product_id
    

# class Domain(models.Model):
#     pfam = models.ForeignKey(Pfam, on_delete=models.DO_NOTHING) 
#     description = models.CharField(max_length=256)
#     start = models.IntegerField(null=False, blank=True)
#     stop = models.IntegerField(null=False, blank=True)
#     def __str__(self):
#        return self.pfam+":"+self.description


# class ProteinDomainLink(models.Model):
#     protein = models.ForeignKey(Protein, on_delete=models.DO_NOTHING)
#     domain = models.ForeignKey(Domain, on_delete=models.DO_NOTHING)


