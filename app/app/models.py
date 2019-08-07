##  models.py
##
##  This initializes all models for the database.
##  Includes Sample, Gene, GeneQual.
##  


##  Import app functions.
#   Imports the database.
from app import app, db


##  Sample class initializes the Sample table for the database.
#   Columns include; id, SRR_id, GSM_acc, experiement_id, tissue
#   cell_type, and genes.
#   
#   -id is the primary key for each entry (1).
#   -SRR_id is a string for the sample SRR index ('SRR577581').
#   -GSM_acc is the GSM accession from where the SRR came from ('GSM1010946').
#   -Experiment id an NCBI id for the experiment ('GSE16256').
#   -Genes is a reference to the Gene table for a samples gene data.
class Tissue(db.Model):
    # Primary key.
    id = db.Column(db.Integer, primary_key=True)
    # SRR_id, unique identifier for each row in table.
    tissue = db.Column(db.String(64), index=True, unique=True)

    cell_type = db.Column(db.String(64))

    # Reference to the Gene table.
    genes = db.relationship('Gene', backref='name', lazy='dynamic')
    
    # Returns the Sample type.
    def __repr__(self):
        return '<Tissue {}>'.format(self.tissue)


##  Gene class initializes the Gene table for the database.
#   Columns include id, gene_id, barcode, and sample_id.
#
#   -id is the primary key for each entry (1).
#   -Gene_id is a string for the gene_id ('ENSG00000223972.4').
#   -Barcode is a boolean value from the barcode calculation (False).
#   -Sample_id is the back reference to the Sample table.
class Gene(db.Model):
    # Primary key.
    id = db.Column(db.Integer, primary_key=True)
    gene_id = db.Column(db.String(20), index=True)
    
    barcode_count = db.Column(db.Integer)
    total_count = db.Column(db.Integer)

    tissue = db.Column(db.Integer, db.ForeignKey('tissue.id'))
    
    # Returns the Gene type.
    def __repr__(self):
        return '<Gene_id {}>'.format(self.gene_id)


##  GeneQual class initializes the GeneQual table for the database.
#   This stores each gene one time, along with qualities for the gene.
#   Columns include id, gene_id, symbol, name, and location.
#
#   -id is the primary key for each entry (1).
#   -Gene_id is string for the gene_id ('ENSG00000223972.4').
#   -Symbol is a string for the gene symbol from Ensembl ('DDX11L1').
#   -Name is a string for the gene name from Ensembl ('DEAD/H-box helicase 11...').
#   -Location is a string for the gene chromosome location from Ensembl ('Chromosome 1: 11869-14409').
class GeneQual(db.Model):
    # Primary key.
    id = db.Column(db.Integer, primary_key=True)
    gene_id = db.Column(db.String(20), index=True)
    
    symbol = db.Column(db.String(32))
    name = db.Column(db.String(32))
    location = db.Column(db.String(64))
    
    # Returns the GeneQual type.
    def __repr__(self):
        return '<Gene_Qual {}>'.format(self.gene_id)

