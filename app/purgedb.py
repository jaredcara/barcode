
from app import db
from app.models import Tissue, Gene

for each in Tissue.query.all():
    db.session.delete(each)

for each in Gene.query.all():
    db.session.delete(each)

db.session.commit()

