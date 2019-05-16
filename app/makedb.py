##  makedb.py
##  
##  This is to initialize the database.
##  It has allready been initialized, so functions have been commented out.
##

#   Import database.
from app import db
#   Import database models.
from app.models import Sample, Gene
#   Import subprocess for command line functions.
import subprocess
#   Import pandas for csv reading.
import pandas


#   Read all barcode files in directory to list "files".
process = subprocess.Popen(['ls', '/media/jared/Drive/test/barcode_out'], stdout=subprocess.PIPE)
stdout, stderr = process.communicate()
files = stdout.decode('ascii').splitlines()


#   Reads all barcode file in files list.
'''
for each in files:
    # Strips ".barcode" from filename.
    each = each[:-8]

    # Creates row for 'each' sample in the Sample table.
    s = Sample(SRR_id=each)
    # Add this row to the session.
    db.session.add(s)

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
    
    # Commit session change for each sample.
    db.session.commit()
    # Expunge current session. This is for memory management, clears the session for the next sample to be added.
    db.session.expunge_all()
'''

#   Open the table with GSM table to retrieve sample tissue names.
with open('../functions/GPL11154_normals.csv') as f:
    pandas_df = pandas.read_csv(f)
'''
#   Iterate each row in the table
for index, row in pandas_df.iterrows():
    
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

                # Update the row entry for sample.
                # ExperimentID, tissue, and cell_type are added to this entry from the esearch results.
                db.session.query(Sample).filter_by(SRR_id=each[0]).update(dict(experiment_id=row['ExperimentID'], tissue=row['Tissue'], cell_type=row['Cell Type']))
                db.session.commit()
'''

