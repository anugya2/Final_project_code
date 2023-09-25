# "All code below written by the student."

# Description of file: Contains all the API classes for all our GET and POST methods.

# Imports:
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import mixins


class ToolDetails(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 generics.GenericAPIView):    
    lookup_field = 'tool_name'
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer  
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)    


class AppUserDetail(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    lookup_field = 'pk' 
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs) 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class BorrowRequestsD(mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    lookup_field = 'request_id' 
    queryset = BorrowRequests.objects.all()
    serializer_class = BorrowRequestsSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs) 
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  

























        
# 2. Returns all details about a proteins.
# POST protein entry along with all domain and other details.
# class ProteinDetails(mixins.CreateModelMixin,
#                  mixins.RetrieveModelMixin,
#                  generics.GenericAPIView):    
#     lookup_field = 'protein_id'
#     queryset = Protein.objects.all()
#     serializer_class = ProteinSerializer  
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

# # Returns list of proteins:
# class ProteinList(generics.ListAPIView):
#     queryset = Protein.objects.all()
#     serializer_class = ProteinListSerializer

# # 4 Return all proteins associated with a single organism.
# class OrganismProteins(generics.ListAPIView,mixins.RetrieveModelMixin):    
#     protein = Protein.objects.all()
#     def get_queryset(self):        
#         qs = [x for x in self.protein if x.taxonomy.taxa_id == self.kwargs['taxa_id']]
#         return qs    
#     serializer_class = OrganismProteinsSerializer

# # 5 Return all domains associated with proteins of a single organism.
# class OrganismDomains(generics.ListAPIView,mixins.RetrieveModelMixin):    
#     protein = Protein.objects.all()
#     proteinDomainLinks = ProteinDomainLink.objects.all()
#     def get_queryset(self):        
#         filtered_proteins = [x for x in self.protein if x.taxonomy.taxa_id == self.kwargs['taxa_id']]
#         filtered_domainLinks = [x for x in self.proteinDomainLinks if x.protein_id  in filtered_proteins]
#         filtered_domains = [x.domain_id for x in filtered_domainLinks]
#         return filtered_domains    
#     serializer_class = DomainSerializer



# # 3. Return for domain/ pfam id and description based on id.
# class PfamDetail(
#                  mixins.RetrieveModelMixin,             
#                  generics.GenericAPIView):    
#     lookup_field = 'pfam_id'
#     queryset = Pfam.objects.all()
#     serializer_class = PfamSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# # 6. Return Coverage. GET and calculate coverage.
# @api_view(['GET'])
# def calculate_coverage(request, protein_id):
#     if request.method == 'GET':        
#         proteinDomainLink = ProteinDomainLink.objects.all() 
#         #Filtered list of all domains-protein links with our specified protein id:           
#         filtered_proteinDomainLink= [x for x in proteinDomainLink if x.protein_id.protein_id==protein_id]
#         # Store the sum of dom location values in these variables
#         dom_start_sum = 0
#         dom_end_sum = 0
#         for unit in filtered_proteinDomainLink:            
#             dom_start_sum = dom_start_sum + unit.domain_start
#             dom_end_sum = dom_end_sum +unit.domain_end            
#         dom_length = dom_end_sum - dom_start_sum        
#         prot_length = filtered_proteinDomainLink[0].protein_id.protein_length        
#         # calculate coverage value
#         coverage_value = dom_length / prot_length        
#         return Response({"Coverage: ": f"{coverage_value}"})


#______________________________________________________________END_______________________________________________________________________________

    




# Rough notes below: 
# working on this one >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# class OrganismProteins(mixins.RetrieveModelMixin,generics.ListAPIView,generics.GenericAPIView):
#     # # queryset = Protein.objects.all()
#     # # lookup_field = 'taxa_id'
#     # queryset = Protein.objects.all()
    
#     # # def get_queryset(self):        
#     # #     return Protein.objects.filter(taxonomy = 'taxonomy')
    
#     # serializer_class = OrganismProteinsSerializer  

#     lookup_field = 'protein_id'

#     queryset = Protein.objects.all()
#     serializer_class = ProteinListSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# no longer in user:
# # for the first API: # POST API protein page: make this complex
# class Protein(mixins.CreateModelMixin,
#               generics.GenericAPIView):
#     # lookup_field = "protein_id"
#     # queryset = Protein.objects.all()
#     serializer_class = ProteinSerializer1

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)   
        




# class GeneDetails(mixins.CreateModelMixin,
#                  mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin,
#                  generics.GenericAPIView):
#     queryset = Gene.objects.all()
#     serializer_class = GeneSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# {
#     "gene_id": "Gene6",
#     "entity": "Chromosome",
#     "start": 234,
#     "stop": 456,
#     "sense": "+",
#     "start_codon": "M",
#     "ec": {
#         "id": 5,
#         "ec_name": "oxidoreductase"
#     },
#     "sequencing": {
#         "id": 3,
#         "sequencing_factory": "Sanger",
#         "factory_location": "UK"
#     }
# }

# # @api_view(['GET'])
# # def genes_list(request):

# #     try:
# #         gene = Gene.objects.all()
# #     except Gene.DoesNotExist:
# #         return HttpResponse(status=404)

# #     if request.method == 'GET':
# #         gene = Gene.objects.all()
# #         serializer = GeneListSerializer(gene, many=True)
# #         return Response(serializer.data)


# class GeneList (generics.ListAPIView):
#     queryset = Gene.objects.all()
#     serializer_class = GeneListSerializer





# {
#     "protein_id": "YY",
#     "protein_length": 10,
#     "taxonomy": {
#         "taxa_id": 568076,
#         "clade": "568076",
#         "genus": "E",
#         "species": "Metarhizium"
#     },
#     "sequence": "MAPVKVGING"
# }



# Doesnt get anything, but the post api has all the fields.
# class ProteinFullDetails(mixins.CreateModelMixin,
#                  mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin,
#                  generics.GenericAPIView):
#     lookup_field = 'protein_id'
#     queryset = ProteinDomainLink.objects.all()
#     serializer_class = ProteinDomainLinkSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)