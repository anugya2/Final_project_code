# "All code below written by the student."

# Description of file:Forms and validators used for the "add protein entry" page.

#Imports
from django import forms
from django.forms import ModelForm
from .models import *
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = AppUser
        fields = ('organisation','status','photo' )
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('house_no','street','city','country' )
class PhotoForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('photo',)




# I wrote this code
# Form for profile creation.


# class UserAddressFormField(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = ('address_id','house_no','street','city','country' )



    
class ToolForm(forms.ModelForm):     
    class Meta:
        model = Tool
        fields = ('tool_category', 'tool_name', 'tool_description', 'tool_photo')
    
    

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name', 'category_description')
    

        

    







# "Add protein entry" form and validation:
# class ProteinForm(ModelForm):
#     class Meta:
#         model = Protein
#         fields = ['protein_id', 'sequence', 'protein_length', 'taxonomy']
    
#     def clean(self):
#         cleaned_data = super(ProteinForm, self).clean()
#         protein_id = cleaned_data.get("protein_id")
#         sequence = cleaned_data.get("sequence")
#         protein_length = cleaned_data.get("protein_length")

#         #All validations used here:
#         # Id must be 10 character long or less
#         if not len(protein_id) <= 10:
#             raise forms.ValidationError("Protein Id 10 characters long")
        
#         # If length of protein is not a positive integer or 0
#         if not protein_length >=0:
#             raise forms.ValidationError("Length of protein is a positive integer")
        
#         # These are the only letters that can be used in a protein sequence
#         Protein_sequence_characters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y','X', 'B', 'Z', 'J', 'X', '*', ' ', '.']
        
#         #if the entry for protein sequence contains letters not in the standards.
#         if not type(sequence) == int:
#             for char in sequence:
#                 if char not in Protein_sequence_characters:
#                     raise forms.ValidationError("Sequence is made up of alphabets denoting aminon acids such as A, C, D, F, ....")

#         # Return validated data:
#         return(cleaned_data)