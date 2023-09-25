# "All code below written by the student."

# Description of file: 
# This file has the script to populate database, It reads the 3 .csv data files provided and loads it into the sql3 database.

# Importing modules used:
import os
import sys 
import django 
import csv
from collections import defaultdict

sys.path.append('../bioweb3')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bioweb3.settings')
django.setup()

# Importing data models.
from proteindata.models import *

# The 3 csv files provided and their location:
data_file1 = '../assignment_data_sequences.csv'
data_file2 = '../assignment_data_set.csv'
data_file3 = '../pfam_descriptions.csv'

# Python data structure to temporarily store data read from the csv file.
proteins = defaultdict(list)
pfam = defaultdict(list)
taxonomy = defaultdict(list)#for non redundant entries
domain = defaultdict(list)
proteinDomainLink = defaultdict(list)

#protein_id/sequence csv file
# Fills just the sequence and protein_id column of proteins table.
with open (data_file1) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # header = csv_reader.__next__() # NO HEADER
    for row in csv_reader:
        pro_id = row[0]
        pro_seq = row[1] 
        proteins[pro_id] = [pro_seq] # filling protein table with sequence        
        

# pfam id and pfam description file
# Fills pfam_id, pfam_description of the pfam table
with open (data_file3) as csv_file:    
    csv_reader = csv.reader(csv_file, delimiter=',')
    # header = csv_reader.__next__() # NO HEADER
    for row in csv_reader: 
        pfam[row[0]] = [row[1]]       
        
        
        
#Big csv file with domains/protein info.
with open (data_file2) as csv_file:

    #csv file description:
    #[protein_id-0, taxa_id-1, clade2, genus 3-firsthalf, species 3-secondhalf, domain-descr-4, domain-id-5, domain-start-6, domain-end-7, protein_length-8]
    
    csv_reader = csv.reader(csv_file, delimiter=',')
    # header = csv_reader.__next__() #NO HEADER
    
    for i,row in enumerate(csv_reader):

        #First, fill the domain table [domain-id]-> [descr, pfam_link/domain-id]
        domain[row[5]]= [row[4]]+[row[5]] 
        #Second fill the taxonomy table
        organism_pair = row[3].split (' ')
        #taxa_id - clade, genus, species
        taxonomy[row[1]] = [row[2]] + [organism_pair[0]] + [organism_pair[1]]        
        
        #Third fill the main proteins table: [protein-id]-> [sequence, length, taxonomy]
        #sequence has been filled already
        #appending length
        proteins[row[0]].append(row[8])         
        
        #appending taxonomy
        proteins[row[0]].append(row[1])         

        # if a new row is created , one that didnt exist in the sequence table
        if len(proteins[row[0]] ) < 3:
            proteins[row[0]] = ['nan'] + proteins[row[0]]

        #Adding to proteinDomainlink table, 
        # uniqueid/ [ProteinDomainLink_id]-> [domain_start, domain_end,protein_id,domain_id ]
        proteinDomainLink[i]= [row[6]] + [row[7]] + [row[0]] + [row[5]]
        
        

#delete all data that might be there prior to us inserting
ProteinDomainLink.objects.all().delete ()
Protein.objects.all().delete()
Taxonomy.objects.all().delete()
Domain.objects.all().delete()
Pfam.objects.all().delete()

#foreign keys
pfam_rows = {} #dictionary refereing pfam element from pfam id
taxonomy_rows = {}
domain_rows = {}
protein_rows = {}

# Populating database final steps.
# Creating django data model object based on the csv data and filing the foreign keys:

for pfam_id, data in pfam.items():    
    row = Pfam.objects.create(pfam_id=pfam_id, pfam_description= data[0])
    row.save()
    pfam_rows[pfam_id] = row
#pfam_id or domain_id is a foreign key

for taxa_id, data in taxonomy.items():
    row = Taxonomy.objects.create(taxa_id=taxa_id, clade=data[0], genus=data[1], species=data[2] )
    row.save( )
    taxonomy_rows[taxa_id] = row
#taxa_id is is a foreign key

for protein_id, data in proteins.items():      
    row = Protein.objects.create(protein_id = protein_id, 
                                 sequence = data[0],
                                 protein_length = data[1],
                                 taxonomy = taxonomy_rows[data[2]])
    row.save()
    protein_rows[protein_id] = row
#protein_id is the foreign key here

for domain_id, data in domain.items():
    row = Domain.objects.create(domain_id =domain_id , 
                                domain_description=data[0], 
                                pfam_link = pfam_rows[domain_id],#OR pfam = pfam_rows[data[1]]
                                ) 
    row.save()
    domain_rows[domain_id] = row
# domain_is is the foreing key here.  

for proteinDomainLink_id, data in proteinDomainLink.items():
    row = ProteinDomainLink.objects.create(ProteinDomainLink_id=proteinDomainLink_id,
                                            domain_start = data[0],
                                            domain_end = data[1],
                                            protein_id = protein_rows[data[2]],
                                            domain_id= domain_rows[data[3]])
    
    row.save()

    








    






        



