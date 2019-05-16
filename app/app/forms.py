from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField, DecimalField


class ExpressedGenesForm(FlaskForm):
    input_type = RadioField('Input type', choices=[('Consensus Tissue', 'Consensus Tissue'), ('Individual Sample', 'Individual Sample')])
    submit = SubmitField('Next')

class ExpressedGenesForm_Consensus(FlaskForm):
    select_tissue = SelectField('Tissue', coerce=int)
    #select_tissue = SelectField('Tissue', choices=[('Consensus Tissue', 'Consensus Tissue'), ('Individual Sample', 'Individual Sample')])
    proportion = DecimalField('Consensus Proportion', default = 0.95, places=2)
    submit = SubmitField('Submit')
    
