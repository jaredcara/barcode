from app import app, db

class Sample(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    SRR_id = db.Column(db.String(10), index=True, unique=True)
    
    experiment_id = db.Column(db.String(10))
    tissue = db.Column(db.String(64))
    cell_type = db.Column(db.String(64))

    genes = db.relationship('Gene', backref='name', lazy='dynamic')
    
    def __repr__(self):
        return '<SRR_id {}>'.format(self.SRR_id)


class Gene(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    gene_id = db.Column(db.String(20), index=True)
    
    barcode = db.Column(db.Boolean)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'))

    def __repr__(self):
        return '<Gene_id {}>'.format(self.gene_id)

