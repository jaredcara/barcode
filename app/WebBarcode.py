from app import app, db
from app.models import Sample, Gene

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Sample': Sample, 'Gene': Gene}

