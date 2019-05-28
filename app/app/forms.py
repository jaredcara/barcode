##  forms.py
##  
##  This initializes all forms for the flask application, these functions
##  are used to submit options to run comparisions.
##


##  Import packages.
#   Flask wtf and wtforms are the packages used to manage forms.
from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField, DecimalField
from wtforms.validators import DataRequired, NumberRange


##  InputTypeSelectionForm class manages initial choices consensus/individual.
#   Input type and submit fields.
class InputTypeSelectionForm(FlaskForm):
    # Input type is a Radio field, select one or the other.
    # Choices is a list of tuples, [(label, data), (label, data)].
    input_type = RadioField('Input type',\
            choices=[('Consensus Tissue', 'Consensus Tissue'),\
                ('Individual Sample', 'Individual Sample')])
    submit = SubmitField('Next')


##  ExpressedGenesForm_Consensus class manages choices for consensus
##  tissue comparisons.
#   Select_tissue, proportion, and submit fields.
class ExpressedGenesForm_Consensus(FlaskForm):
    # Coerce is used so the selection is dynamic, choices are 
    # queried from the database.
    select_tissue = SelectField('Tissue', coerce=int)
    
    # Proportion is a DecimalField, accepts number between 0,1.
    proportion = DecimalField('Consensus Proportion',\
            default = 0.95,\
            places=2,\
            validators=[DataRequired(), NumberRange(min=0, max=1)])

    submit = SubmitField('Submit')


##  Form_Consensus class manages choices for consensus
##  tissue comparisons.
#   Select_tissue, proportion, and submit fields.
class TissueComparisonForm_Consensus(FlaskForm):
    # Coerce is used so the selection is dynamic, choices are
    # queried from the database.
    select_tissue1 = SelectField('Tissue 1', coerce=int)

    # Proportion is a DecimalField, accepts number between 0,1.
    proportion = DecimalField('Consensus Proportion',
            default = 0.95,
            places=2,
            validators=[DataRequired(), NumberRange(min=0, max=1)])
    
    boolean_expression = SelectField('Boolean Expression', 
            choices=[('AND', 'AND (intersection)'),
                ('OR', 'OR (union)'),
                ('XOR', 'XOR (one or the other but not both)'),
                ('NOR', 'NOR (not present in either)')])
    
    select_tissue2 = SelectField('Tissue 2', coerce=int)
    
    submit = SubmitField('Submit')

