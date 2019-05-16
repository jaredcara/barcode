
from app import db
from app.models import Sample, Gene

for each in Sample.query.all():
    db.session.delete(each)

for each in Gene.query.all():
    db.session.delete(each)

db.session.commit()

