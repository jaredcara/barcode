
from app import db
from app.models import Sample, Gene, GeneQual
import subprocess
import pandas
import ensemblrest import EnsemblRest

#process = subprocess.Popen(['ls', '/media/jared/Drive/test/barcode_out'], stdout=subprocess.PIPE)

#stdout, stderr = process.communicate()
#files = stdout.decode('ascii').splitlines()
'''
for each in files:
    each = each[:-8]
    s = Sample(SRR_id=each)
    db.session.add(s)

    with open('/media/jared/Drive/test/barcode_out/' + each + '.barcode') as f:
        line = f.readline()
        while line:
            line = line.strip().split()
            g = Gene(gene_id=line[0], barcode=line[1]=='1', name=s)
            db.session.add(g)
            line = f.readline()

    db.session.commit()
    db.session.expunge_all()
    print(each)

'''
'''
with open('../GPL11154_normals.csv') as f:
    pandas_df = pandas.read_csv(f)
print(pandas_df['Cell Type'])

count = 0
for index, row in pandas_df.iterrows():
    print(row['filename'])
    cmd = "esearch -db sra -query {} | efetch -format runinfo".format(row['filename'])
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0].decode('ascii').splitlines()
    for each in output:
        each = each.split(',')
        if each[0][0:3] == 'SRR':
            query = Sample.query.filter_by(SRR_id=each[0]).first()
            if query:
                db.session.query(Sample).filter_by(SRR_id=each[0]).update(dict(experiment_id=row['ExperimentID'], tissue=row['Tissue'], cell_type=row['Cell Type']))
                db.session.commit()
                print(query)
                count += 1

print(count)
'''
'''
ensRest = EnsemblRest()
for each in Sample.query.get(1).genes.all():
    gene = each.split('.')[0]
    geneinfo = ensRest.getLookupById(id=gene)
    g = GeneQual(symbol=geneinfo['display_name'], name=geneinfo['description'], location='Chromosome {}: {}-{}'.format(geneinfo['seq_region_name'], geneinfo['start'], geneinfo['end']))
    db.session.add(g)
    db.session.commit()
    db.session.
'''
