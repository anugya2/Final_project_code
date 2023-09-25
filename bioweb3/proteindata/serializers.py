# "All code below written by the student."

# Description of file: Contains serializers for all api endpoints.

# Imports:
from rest_framework import serializers
from .models import *
from django_countries.serializers import CountryFieldMixin

class CategorySerializer(serializers.ModelSerializer):    
    class Meta:
        model = Category
        fields = ['category_name', 'category_description']

class AddressSerializer(CountryFieldMixin, serializers.ModelSerializer):    
    class Meta:
        model = Address
        fields = ['address_id', 'house_no', 'street', 'city', 'country']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    user_address = AddressSerializer()
    class Meta:
        model = AppUser
        fields = ['user', 'organisation', 'status', 'user_address', 'photo']

class ToolSerializer(serializers.ModelSerializer):
    tool_category = CategorySerializer()
    tool_location = AddressSerializer()
    tool_owner = AppUserSerializer()
    class Meta:
        model = Tool
        fields = ['tool_id', 'tool_category', 'tool_name', 'tool_description', 'tool_photo', 'tool_location', 'tool_owner']

    def create(self, validated_data):
        tool_category_data = self.initial_data.get('tool_category')  
        tool_location_data = self.initial_data.get('tool_location')
        tool_owner_data = self.initial_data.get('tool_owner')      
        tool = Tool(**{**validated_data, 
                       'tool_category': Category.objects.get(category_name = tool_category_data['category_name']),
                       'tool_location': Address.objects.get(address_id = tool_location_data['address_id']),
                       'tool_owner': User.objects.get(user_id = tool_owner_data['user_id']), 
                       })
        tool.save()
        return tool

class BorrowRequestsSerializer(serializers.ModelSerializer):
    tool_id = ToolSerializer()
    borrower = AppUserSerializer()
    class Meta:
        model = BorrowRequests
        fields = ['request_id', 'tool_id', 'borrower', 'acceptance_status']






























    
# Taxonomy/ Organism table
# class TaxonomySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Taxonomy
#         fields = ['taxa_id','clade','genus','species']

# # GET returning all proteins associating with a single organism.
# class OrganismProteinsSerializer(serializers.ModelSerializer):
#     taxonomy = TaxonomySerializer()    
#     class Meta:
#         model = Protein
#         fields = ['id','protein_id', 'taxonomy']

# # GET pfam/domain id and description
# class PfamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Pfam
#         fields = ['pfam_id','pfam_description']

# # GET, POST domain data.
# # POST is required incase the scientist want to add domains too along with the protein entry.
# class DomainSerializer(serializers.ModelSerializer):
#     pfam_link = PfamSerializer()
#     class Meta:
#         model = Domain
#         fields = ['id','domain_id','domain_description','pfam_link']
#     def create(self, validated_data):
#         pfam_link_data = self.initial_data.get('pfam_link')        
#         domain = Domain(**{**validated_data, 
#                        'pfam_link': Pfam.objects.get(pfam_id = pfam_link_data['pfam_id']), 
#                        })
#         domain.save()
#         return domain

# # GET list of protein ids
# class ProteinListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Protein
#         fields = ['protein_id']
    
# # GET, POST protein-domain-links table
# # different from the first as it doesnt use proteinserialiser and deals with only domain serialiser
# class ProteinDomainLinkSerializer2(serializers.ModelSerializer):    
#     domain_id = DomainSerializer()
#     class Meta:
#         model = ProteinDomainLink
#         fields = ['domain_start','domain_end','domain_id'] 
#     def create(self, validated_data):        
#         domain_id_data = self.initial_data.get('domain_id')        
#         ProteinDomainLink = ProteinDomainLink(**{**validated_data,                         
#                        'domain_id': Domain.objects.get(domain_id = domain_id_data['domain_id']),
#                        })
#         ProteinDomainLink.save()
#         return ProteinDomainLink

# # POST, GET returns the complex details with everything about a protein.
# # Can also post data about protein in the same format (everything about protein)
# class ProteinSerializer(serializers.ModelSerializer): 
#     #Add domains to details about a protein.
#     domains = serializers.SerializerMethodField('domains_finder')    
#     def domains_finder(self, protein_id):        
#         # First get domain ids from link table using protein_id
#         row_domain_ids = ProteinDomainLink.objects.all().filter(protein_id=protein_id)
#         #This will be the final list that stores all the related domains of this protein
#         serializers_list = []        
#         for row in row_domain_ids:
#             serializers_list.append((ProteinDomainLinkSerializer2(row)).data)
#         return serializers_list    
#     taxonomy = TaxonomySerializer()
#     class Meta:
#         model = Protein
#         fields = ['protein_id','protein_length','sequence','taxonomy','domains'] 
#     def validate(self, data):    
#         """
#         Some more specific custom validations:
#         """
#         domains_data = self.initial_data.get('domains')
#         # Validation 1
#         for dom in domains_data:
#             if dom['domain_start'] > dom['domain_end']:
#                 raise serializers.ValidationError("domain_end must be larger than domain_start")
#         # Validation 2: length of protein id should be <11
#         if len(data['protein_id']) > 10:
#             raise serializers.ValidationError("max length of protein id is 10")
#         #Validation 3: protein_length should be 0 or positive
#         if not  data['protein_length'] >=0:
#             raise serializers.ValidationError("Length of protein is a positive integer")
        
#         # These are the only letters that can be used in a protein sequence
#         Protein_sequence_characters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
#                                         'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y','X',
#                                           'B', 'Z', 'J', 'X', '*', ' ', '.']
        
#         #Validation 4: if the entry for protein sequence contains letters not in the standards.
#         if not type(data['sequence']) == int:
#             for char in data['sequence']:
#                 if char not in Protein_sequence_characters:                    
#                     raise serializers.ValidationError("The characters in protein sequences are specific alphabets representing amino acids, so they should be  present in this set ['A', 'C', 'D', 'E','F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V','W', 'Y','X', 'B', 'Z', 'J', 'X', '*', ' ', '.']")        
#         return data   

#     def create(self, validated_data):
#         domains_data = self.initial_data.get('domains')
        
#         # domains_data is a list of {'domain_start': 4, 'domain_end': 9, 'domain_id': {'domain_id': 'AF0AAAA', 'domain_description': 'descriptaseinase', 'pfam_link': {'pfam_id': 'AF0AAAA', 'pfam_description': 'descriptaseinase'}}}
#         # validated_data {'protein_id': 'AAAAAAAAA1', 'protein_length': 10, 'sequence': 'MVI', 'taxonomy': OrderedDict([('taxa_id', 53326), ('clade', 'E'), ('genus', 'Ancylostoma'), ('species', 'ceylanicum')])}
        
#         #Create taxonomy if it doesnt exist:  
#         try:      
#             test_taxonomy = Taxonomy.objects.get(taxa_id= int(validated_data['taxonomy']['taxa_id']))
#         except:
#             row= Taxonomy.objects.create(taxa_id= int(validated_data['taxonomy']['taxa_id']), 
#                             clade= validated_data['taxonomy']['clade'], 
#                             genus= validated_data['taxonomy']['genus'], 
#                             species= validated_data['taxonomy']['species'] )
#             row.save()
            
#         #Create Pfam if it doesnt exist:
#         for dom in domains_data:
#             try: 
#                 test_pfam = Pfam.objects.get(pfam_id=dom['domain_id']['pfam_link']['pfam_id'])        
#             except:
#                 row= Pfam.objects.create(pfam_id=dom['domain_id']['pfam_link']['pfam_id'], 
#                                         pfam_description= dom['domain_id']['pfam_link']['pfam_description'])
#                 row.save()
            
        
#         #Create Protein if it doesnt exist:
#         try:
#             test_protein = Protein.objects.get( protein_id = validated_data['protein_id'])
#         except:            
#             row=Protein.objects.create( protein_id = validated_data['protein_id'],
#                                                 sequence = validated_data['sequence'],
#                                                 protein_length = validated_data['protein_length'],
#                                                 taxonomy = Taxonomy.objects.get(taxa_id= int(validated_data['taxonomy']['taxa_id']), 
#                                                                                 clade= validated_data['taxonomy']['clade'], 
#                                                                                 genus= validated_data['taxonomy']['genus'], 
#                                                                                 species= validated_data['taxonomy']['species'] ))
#             row.save()
        
#         #Create domain if it doesnt exist:
#         # For all domains in the entry data:
#         for dom in domains_data:
#             try:
#                 test_domain = Domain.objects.get(domain_id =dom['domain_id']['domain_id'])
#             except:
#                 row= Domain.objects.create(domain_id =dom['domain_id']['domain_id'],
#                                                                                     domain_description=dom['domain_id']['domain_description'],
#                                                                                     pfam_link=Pfam.objects.get(pfam_id=dom['domain_id']['pfam_link']['pfam_id']))
#                 row.save()

#             try:
#                 test_proteinDomainLink = ProteinDomainLink.objects.get(
#                                                 domain_start = dom['domain_start'],
#                                                 domain_end=dom['domain_end'],
#                                                 protein_id=Protein.objects.get( protein_id = validated_data['protein_id']),
#                                                 domain_id=Domain.objects.get(domain_id =dom['domain_id']['domain_id']))
#             except:
#                 test_proteinDomainLink = ProteinDomainLink.objects.create(ProteinDomainLink_id= '5000',
#                                                 domain_start = dom['domain_start'],
#                                                 domain_end=dom['domain_end'],
#                                                 protein_id=Protein.objects.get( protein_id = validated_data['protein_id']),
#                                                 domain_id=Domain.objects.get(domain_id =dom['domain_id']['domain_id']))                
#                 test_proteinDomainLink.save()   
          
#         protein = Protein(**{**validated_data, 
#                        'taxonomy': Taxonomy.objects.get(taxa_id= int(validated_data['taxonomy']['taxa_id']))})  
        
#         return protein

    


#______________________________________________________________END_______________________________________________________________________________

    



















    





#Rough notes below
#...................................................................................................................


# class ProteinSerializer(serializers.ModelSerializer):

#     domains = serializers.SerializerMethodField('domains_finder')
#     def domains_finder(self, protein_id):        
#         # First get domain ids from link table using protein_id
#         row_domain_ids = ProteinDomainLink.objects.all().filter(protein_id=protein_id)
#         #This will be the final list that stores all the related domains of this protein
#         serializers_list = []        
#         for row in row_domain_ids:
#             serializers_list.append((ProteinDomainLinkSerializer2(row)).data)
#         return serializers_list
    
#     taxonomy = TaxonomySerializer()

#     class Meta:
#         model = Protein
#         fields = ['protein_id','protein_length','sequence','taxonomy','domains'] 

#     # def create(self, validated_data):
#     #     taxonomy_data = self.initial_data.get('taxonomy')     
#     #     protein = Protein(**{**validated_data, 
#     #                    'taxonomy': Taxonomy.objects.get(taxa_id = taxonomy_data['taxa_id'])                       
#     #                    })
#     #     protein.save()        
#     #     return protein
    
    

#     def create(self, validated_data):
#         domains_data = self.initial_data.get('domains')

        
#         # domains_data is a list of {'domain_start': 4, 'domain_end': 9, 'domain_id': {'domain_id': 'AF0AAAA', 'domain_description': 'descriptaseinase', 'pfam_link': {'pfam_id': 'AF0AAAA', 'pfam_description': 'descriptaseinase'}}}
#         # validated_data {'protein_id': 'AAAAAAAAA1', 'protein_length': 10, 'sequence': 'MVI', 'taxonomy': OrderedDict([('taxa_id', 53326), ('clade', 'E'), ('genus', 'Ancylostoma'), ('species', 'ceylanicum')])}
        
#         #Create taxonomy if it doesnt exist:  
#         try:      
#             test_taxonomy = Taxonomy.objects.get(taxa_id= int(validated_data['taxonomy']['taxa_id']), 
#                                 clade= validated_data['taxonomy']['clade'], 
#                                 genus= validated_data['taxonomy']['genus'], 
#                                 species= validated_data['taxonomy']['species'] )
#         except:
#             row= Taxonomy.objects.create(taxa_id= int(validated_data['taxonomy']['taxa_id']), 
#                             clade= validated_data['taxonomy']['clade'], 
#                             genus= validated_data['taxonomy']['genus'], 
#                             species= validated_data['taxonomy']['species'] )
#             row.save()
            
#         #Create Pfam if it doesnt exist:
#         try: 
#             test_pfam = Pfam.objects.get(pfam_id=domains_data[0]['domain_id']['pfam_link']['pfam_id'], 
#                                         pfam_description= domains_data[0]['domain_id']['pfam_link']['pfam_description'])
        
#         except:
#             row= Pfam.objects.create(pfam_id=domains_data[0]['domain_id']['pfam_link']['pfam_id'], 
#                                     pfam_description= domains_data[0]['domain_id']['pfam_link']['pfam_description'])
#             row.save()
            
        
#         #Create Protein if it doesnt exist:
#         try:
#             test_protein = Protein.objects.get( protein_id = validated_data['protein_id'],
#                                                     sequence = validated_data['sequence'],
#                                                     protein_length = validated_data['protein_length'],
#                                                     taxonomy = Taxonomy.objects.get(taxa_id= int(validated_data['taxonomy']['taxa_id']), 
#                                                                                     clade= validated_data['taxonomy']['clade'], 
#                                                                                     genus= validated_data['taxonomy']['genus'], 
#                                                                                     species= validated_data['taxonomy']['species'] ))
#         except:
            
#             row=Protein.objects.create( protein_id = validated_data['protein_id'],
#                                                 sequence = validated_data['sequence'],
#                                                 protein_length = validated_data['protein_length'],
#                                                 taxonomy = Taxonomy.objects.get(taxa_id= int(validated_data['taxonomy']['taxa_id']), 
#                                                                                 clade= validated_data['taxonomy']['clade'], 
#                                                                                 genus= validated_data['taxonomy']['genus'], 
#                                                                                 species= validated_data['taxonomy']['species'] ))
#             row.save()
        
#         #Create domain if it doesnt exist:
#         try:
#             test_domain = Domain.objects.get(domain_id =domains_data[0]['domain_id']['domain_id'],
#                                                                                  domain_description=domains_data[0]['domain_id']['domain_description'],
#                                                                                  pfam_link=Pfam.objects.get(pfam_id=domains_data[0]['domain_id']['pfam_link']['pfam_id'], 
#                                                                                                                pfam_description= domains_data[0]['domain_id']['pfam_link']['pfam_description']))
#         except:
#             row= Domain.objects.create(domain_id =domains_data[0]['domain_id']['domain_id'],
#                                                                                  domain_description=domains_data[0]['domain_id']['domain_description'],
#                                                                                  pfam_link=Pfam.objects.get(pfam_id=domains_data[0]['domain_id']['pfam_link']['pfam_id'], 
#                                                                                                                pfam_description= domains_data[0]['domain_id']['pfam_link']['pfam_description']))

#             row.save()
        

#         try:
#             test_proteinDomainLink = ProteinDomainLink.objects.get(ProteinDomainLink_id= '5000',
#                                                domain_start = domains_data[0]['domain_start'],
#                                                domain_end=domains_data[0]['domain_end'],
#                                                protein_id=Protein.objects.get( protein_id = validated_data['protein_id']),
#                                                domain_id=Domain.objects.get(domain_id =domains_data[0]['domain_id']['domain_id'],
#                                                                                  domain_description=domains_data[0]['domain_id']['domain_description'],
#                                                                                  pfam_link=Pfam.objects.get(pfam_id=domains_data[0]['domain_id']['pfam_link']['pfam_id'], 
#                                                                                                                pfam_description= domains_data[0]['domain_id']['pfam_link']['pfam_description']))
#                                                )
#         except:
#             test_proteinDomainLink = ProteinDomainLink.objects.create(ProteinDomainLink_id= '5000',
#                                                domain_start = domains_data[0]['domain_start'],
#                                                domain_end=domains_data[0]['domain_end'],
#                                                protein_id=Protein.objects.get( protein_id = validated_data['protein_id']),
#                                                domain_id=Domain.objects.get(domain_id =domains_data[0]['domain_id']['domain_id'],
#                                                                                  domain_description=domains_data[0]['domain_id']['domain_description'],
#                                                                                  pfam_link=Pfam.objects.get(pfam_id=domains_data[0]['domain_id']['pfam_link']['pfam_id'], 
#                                                                                                                pfam_description= domains_data[0]['domain_id']['pfam_link']['pfam_description']))
#                                                )
            
#             test_proteinDomainLink.save()


        
#         #.............................................................................................................

#         domains = serializers.SerializerMethodField('domains_finder')
               
#         # First get domain ids from link table using protein_id
#         row_domain_ids = ProteinDomainLink.objects.all().filter(protein_id=validated_data['protein_id'])
#         #This will be the final list that stores all the related domains of this protein
#         serializers_list = domains_finder(self, protein_id)
        
        

#         class Meta:
#             model = Protein
#             fields = ['protein_id','protein_length','sequence','taxonomy','domains']


#         #........................................................................

#         taxonomy_data = self.initial_data.get('taxonomy')     
#         protein = Protein(**{**validated_data, 
#                        'taxonomy': Taxonomy.objects.get(taxa_id = taxonomy_data['taxa_id'])                       
#                        })
               
#         return protein
        

#     # def create(self, validated_data):
#     #     taxonomy_data = self.initial_data.get('taxonomy')     
#     #     protein = Protein(**{**validated_data, 
#     #                    'taxonomy': Taxonomy.objects.get(taxa_id = taxonomy_data['taxa_id'])                       
#     #                    })
#     #     protein.save()        
#     #     # return protein
    

#     # class Meta:
#     #     model = ProteinDomainLink
#     #     fields = ['ProteinDomainLink_id','domain_start','domain_end','taxonomy','domains']


#     # proteins = []
#     # for domain in 'domains':


#     #     def create(self, validated_data):
#     #         domain_id = DomainSerializer()
#     #         taxonomy_data = self.initial_data.get('taxonomy')

#     #         domain_data = self.initial_data.get('domain')
#     #         protein = Protein(**{**validated_data, 
#     #                     'taxonomy': Taxonomy.objects.get(taxa_id = taxonomy_data['taxa_id']),
#     #                     'domain_id': Domain.objects.get(domain_id = domain_data['domain_id'])
#     #                     })
#     #         protein.save()
#     #         proteins.append(protein)

#     #         # domain = Domain.objects.get(domain_id = 'PF06772')
#     #         return proteins



# No longer in user:
# POST API protein page: make this complex
# class ProteinSerializer1(serializers.ModelSerializer):
#     taxonomy = TaxonomySerializer()
#     class Meta:
#         model = Protein
#         fields = ['protein_id','protein_length','sequence','taxonomy'] 





    





# class ECSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EC
#         fields = ['id', 'ec_name'] 

# class SequencingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Sequencing
#         fields = ['id', 'sequencing_factory', 'factory_location'] 

# class GeneSerializer(serializers.ModelSerializer):
#     ec = ECSerializer()
#     sequencing= SequencingSerializer()
#     class Meta:
#         model = Gene
#         fields = ['gene_id', 'entity', 'start', 'stop', 'sense', 'start_codon', 'ec', 'sequencing']

#     def create(self, validated_data):
#         ec_data = self.initial_data.get('ec')
#         seq_data = self.initial_data.get('sequencing')
#         gene = Gene(**{**validated_data, 
#                        'ec': EC.objects.get(pk=ec_data['id']), 
#                        'sequencing': Sequencing.objects.get(pk=seq_data['id'])
#                        })
#         gene.save()
#         return gene

# class GeneListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gene
#         fields = ['id', 'gene_id']



# {
#     "protein_id": "ABCDEFGHIJ",
#     "protein_length": 10,
#     "taxonomy": {
#         "taxa_id": 568076,
#         "clade": "E",
#         "genus": "Metarhizium",
#         "species": "robertsii"
#     },
#     "sequence": "MLYUK"
# }




# GET, POST protein-domain-links table
# different from ProteinDomainLinkSerializer2() as it uses proteinserialiser.
# class ProteinDomainLinkSerializer(serializers.ModelSerializer):
#     protein_id = ProteinSerializer()
#     domain_id = DomainSerializer()
#     class Meta:
#         model = ProteinDomainLink
#         fields = ['ProteinDomainLink_id','domain_start','domain_end','protein_id','domain_id'] 

#     def create(self, validated_data):
#         protein_id_data = self.initial_data.get('protein_id')
#         domain_id_data = self.initial_data.get('domain_id')
        
#         ProteinDomainLink = ProteinDomainLink(**{**validated_data, 
#                        'protein_id': Protein.objects.get(protein_id = protein_id_data['protein_id']), 
#                        'domain_id': Domain.objects.get(domain_id = domain_id_data['domain_id']),
#                        })
#         ProteinDomainLink.save()
#         return ProteinDomainLink






#...........................................................................................................................................................................




    
