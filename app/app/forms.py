##  forms.py
##  
##  This initializes all forms for the flask application, these functions
##  are used to submit options to run comparisions.
##


##  Import packages.
#   Flask wtf and wtforms are the packages used to manage forms.
from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


##  ExpressedGenesForm class manages choices for consensus
##  tissue comparisons.
#   Select_tissue, proportion, and submit fields.
class ExpressedGenesForm(FlaskForm):
    # Coerce is used so the selection is dynamic, choices are 
    # queried from the database.
    select_tissue = SelectField('Tissue', coerce=int)
    
    # Proportion is a DecimalField, accepts number between 0,1.
    proportion = DecimalField('Consensus Proportion',\
            default = 0.95,\
            places=2,\
            validators=[DataRequired(), NumberRange(min=0, max=1)])

    submit = SubmitField('Submit')


##  TissueComparisonForm class manages choices for consensus
##  tissue comparisons.
#   Select_tissue, proportion, and submit fields.
class TissueComparisonForm(FlaskForm):
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


class GeneCatalogForm(FlaskForm):
    input_type = RadioField('Input type', choices=[('symbol', 'Gene Symbol'), ('gene_id', 'ENSG gene id')], validators=[DataRequired()])
    text_entry = TextAreaField('Genes:', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_text(form, field):
        for each in field:
            if each[:4] != 'ENSG':
                raise ValidationError('Genes must begin with ENSG')

