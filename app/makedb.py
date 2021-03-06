##  makedb.py
##  
##  This is to initialize the database.
##  It has allready been initialized, so functions have been commented out.
##

#   Import database.
from app import db
from app.models import Tissue, Gene, GeneQual
#   Import subprocess for command line functions.
import subprocess
#   Import pandas for csv reading.
import pandas
from ensemblrest import EnsemblRest


#   Read all barcode files in directory to list "files".
process = subprocess.Popen(['ls', '/media/jared/Drive/test/barcode_out'], stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
files = stdout.decode('ascii').splitlines()


#   Open the table with GSM table to retrieve sample tissue names.
with open('../functions/GPL11154_normals.csv') as f:
    pandas_df = pandas.read_csv(f)

#   Reads all barcode file in files list.
for sample in files:
    # Strips ".barcode" from filename.
    sample = sample[:-8]
    print(sample)

    exit = False
    for index, row in pandas_df.iterrows():
        if exit:
            break
        # esearch command to retrieve information on sample.
        cmd = "esearch -db sra -query {} | efetch -format runinfo".format(row['filename'])
        # Run the esearch command.
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.communicate()[0].decode('ascii').splitlines()
        # Iterate through the lines of esearch result.
        for each in output:
            # Split the lines at ','
            each = each.split(',')

            # If the first characters are SRR, this is what we are looking for.
            if each[0] == sample:
                this_tissue=row['Tissue']
                cell_type=row['Cell Type']
                exit = True
                break
    
    t = Tissue.query.filter_by(tissue=this_tissue).first()

    if t:
        with open('/media/jared/Drive/test/barcode_out/' + sample + '.barcode') as f:
            line = f.readline()
            while line:
                # Strip new line character, split at '\t' character.
                line = line.strip().split()

                # Creates row for every gene in the barcode file in the Gene table.

                # Sets gene_id to the name of the gene,
                # barcode as boolean, True if 1, False if 0,
                # name is a link to the sample 's'.
                g = Gene.query.filter_by(gene_id=line[0], tissue=t.id).first()
                if line[1]=='1':
                    g.barcode_count = g.barcode_count + 1
                    g.total_count = g.total_count + 1
                else:
                    g.total_count = g.total_count + 1

                # Add this gene to the session.
                db.session.add(g)
                line = f.readline()
        db.session.commit()
    else:
        t = Tissue(tissue=this_tissue, cell_type=cell_type)
        db.session.add(t)
        db.session.commit()

        with open('/media/jared/Drive/test/barcode_out/' + sample + '.barcode') as f:
            line = f.readline()
            while line:
                # Strip new line character, split at '\t' character.
                line = line.strip().split()

                # Creates row for every gene in the barcode file in the Gene table.

                # Sets gene_id to the name of the gene,
                # barcode as boolean, True if 1, False if 0,
                # name is a link to the sample 's'.
                if line[1]=='1':
                    g = Gene(gene_id=line[0], barcode_count=1, total_count=1, name=t)
                else:
                    g = Gene(gene_id=line[0], barcode_count=0, total_count=1, name=t)
                # Add this gene to the session.
                db.session.add(g)
                line = f.readline()
        db.session.commit()
    '''
    # Opens 'each' barcode file.
    with open('/media/jared/Drive/test/barcode_out/' + each + '.barcode') as f:
        line = f.readline()
        while line:
            # Strip new line character, split at '\t' character.
            line = line.strip().split()
            
            # Creates row for every gene in the barcode file in the Gene table.
            
            # Sets gene_id to the name of the gene,
            # barcode as boolean, True if 1, False if 0,
            # name is a link to the sample 's'.
            
            g = Gene(gene_id=line[0], barcode=line[1]=='1', name=s)
            # Add this gene to the session.
            db.session.add(g)
            line = f.readline()
    
    print(s.SRR_id)
    # Commit session change for each sample.
    db.session.commit()
    # Expunge current session. This is for memory management, clears the session for the next sample to be added.
    db.session.expunge_all()
    '''
print('done')
'''
#   Open the table with GSM table to retrieve sample tissue names.
with open('../functions/GPL11154_normals.csv') as f:
    pandas_df = pandas.read_csv(f)


#   Iterate each row in the table
for index, row in pandas_df.iterrows():
    print(row['Cell Type'])
    # esearch command to retrieve information on sample.
    cmd = "esearch -db sra -query {} | efetch -format runinfo".format(row['filename'])
    # Run the esearch command.
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0].decode('ascii').splitlines()
    # Iterate through the lines of esearch result.
    for each in output:
        # Split the lines at ','
        each = each.split(',')
        
        # If the first characters are SRR, this is what we are looking for.
        if each[0][0:3] == 'SRR':
            
            # Query the Sample table for this SRR id.
            query = Sample.query.filter_by(SRR_id=each[0]).first()
            
            # If this SRR id is in the database.
            if query:
                
                print(query)
                # Update the row entry for sample.
                # ExperimentID, tissue, and cell_type are added to this entry from the esearch results.
                db.session.query(Sample).filter_by(SRR_id=each[0]).update(dict(GSM_acc=row['filename'], experiment_id=row['ExperimentID'], tissue=row['Tissue'], cell_type=row['Cell Type']))
                db.session.commit()
'''
'''
ensRest = EnsemblRest()
for each in Sample.query.get(1).genes.all():
    if not GeneQual.query.filter_by(gene_id=each.gene_id).all():
        
        gene = each.gene_id.split('.')[0]
        try:
            geneinfo = ensRest.getLookupById(id=gene)
            g = GeneQual(gene_id=each.gene_id, symbol=geneinfo['display_name'], name=geneinfo['description'], location='Chromosome {}: {}-{}'.format(geneinfo['seq_region_name'], geneinfo['start'], geneinfo['end']))
        except:
            print('error: ' + each.gene_id)
            g = GeneQual(gene_id=each.gene_id)
        db.session.add(g)
        db.session.commit()
'''
