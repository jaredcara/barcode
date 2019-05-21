##  WebBarcode.py
##  
##  This function creates a shell context that adds the database instance
##  and its models to the shell context.
##


#   Imports app and database.
from app import app, db
#   Imports database models.
from app.models import Sample, Gene, GeneQual


#   Processor for application.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Sample': Sample, 'Gene': Gene, 'GeneQual': GeneQual}

