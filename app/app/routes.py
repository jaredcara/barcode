##  routes.py
##  
##  This provides all flask functionality for the front end webpage.
##  Routes include index, expressedgenes, expressedgenes_consensustissue,...
##


##  Import packages.
#   The primary flask functions imported.
from flask import render_template, flash, redirect, url_for, request, send_file
#   Import os.
import os
#   Import timeit for runtime calculations.
import timeit
##  Import app functions.
#   Import add, database.
from app import app, db
#   Import database models.
from app.models import Sample, Gene, GeneQual
#   Import entry forms.
from app.forms import InputTypeSelectionForm, ExpressedGenesForm_Consensus, TissueComparisonForm_Consensus


##  Index route.
#   The home webpage.
@app.route('/')
@app.route('/index')
def index():
    # Renders index.
    return render_template('index.html', title='Home')


##  ExpressedGenes route.
#   Displays expressed genes options, consensus tissue and ...
@app.route('/ExpressedGenes', methods=['GET', 'POST'])
def expressedgenes():
    # Loads InputTypeSelectionForm.
    form = InputTypeSelectionForm()
    
    # If form entry is valid, then submit form.
    if form.validate_on_submit():
        # Operator to select consensus tissue or ...
        if form.input_type.data == 'Consensus Tissue':
            # Redirect to consensus tissue.
            return redirect(url_for('expressedgenes_consensustissue'))
        else:
            flash(form.input_type.data)
            return redirect(url_for('index'))
    
    # Render expressedgenes page.
    return render_template('expressedgenes.html',\
            title='Expressed Genes',\
            form=form)


##  Expressedgenes_consensustissue route.
#   Displays consensus tissue options, displays results.
@app.route('/ExpressedGenes/ConsensusTissue', methods=['GET', 'POST'])
def expressedgenes_consensustissue():
    # Query all Samples to find unique tissues.
    # This is not optimal, working on a permanent, efficient query.
    all_samples = Sample.query.all()
    unique_tissues = []
    
    # Loops each sample to add unique to all_tissues.
    for each in all_samples:
        if each.tissue not in unique_tissues:
            unique_tissues.append(each.tissue)
    
    # Sets choices to unique tissues.
    choices = [(i, unique_tissues[i]) for i in range(len(unique_tissues))]
    
    # Initializes Consensus tissue form.
    form = ExpressedGenesForm_Consensus()
    # Sets choices to unique tissues.
    form.select_tissue.choices = choices
    
    # If form is valid, submit form.
    if form.validate_on_submit():
        '''
        # Old function, efficent when n samples is small, crashes when n is large.
        for i in range(len(samples)):
            samples[i] = samples[i].genes
        
        results = []
        for item in zip(*samples):
            sums = 0
            for i in range(len(item)):
                if item[i].barcode:
                    sums += 1
            if sums >= (len(item)*0.95):
                results.append(item[0].gene_id)
        '''
        # Initialize results to empty list.
        results = []
        # Proportion for consensus calculation from entry field.
        calc = float(db.session.query(Sample)
                .filter(Sample.tissue==choices[form.select_tissue.data][1])
                .count() * form.proportion.data)
        
        # Loops GeneQual database for all genes.
        for each in db.session.query(GeneQual).all():
            # Query Sample, Gene database.
            # Query Sample and Gene reference,
            #       First filter: tissue type.
            #       Second filter: each gene id in loop and barcode is True.
            # If the count of query is >= proportion,
            #       Append gene to results.
            if db.session.query(Sample)\
                    .outerjoin(Sample.genes)\
                    .filter(Sample.tissue==choices[form.select_tissue.data][1],
                        Gene.gene_id==each.gene_id,
                        Gene.barcode==True)\
                    .count() >= calc:
                        results.append(each)

        # Render results.
        return render_template('results.html',
                title='Results',
                results=results)
    
    # Render consensus tissue selection page.
    return render_template('expressedgenes_consensustissue.html',
            title='Expressed Genes',
            form=form)


##  ExpressedGenes route.
#   Displays expressed genes options, consensus tissue and ...
@app.route('/TissueComparison', methods=['GET', 'POST'])
def tissuecomparison():
    # Loads InputTypeSelectionForm.
    form = InputTypeSelectionForm()

    # If form entry is valid, then submit form.
    if form.validate_on_submit():
        # Operator to select consensus tissue or ...
        if form.input_type.data == 'Consensus Tissue':
            # Redirect to consensus tissue.
            return redirect(url_for('tissuecomparison_consensustissue'))
        else:
            flash(form.input_type.data)
            return redirect(url_for('index'))

    # Render expressedgenes page.
    return render_template('tissuecomparison.html',\
            title='Tissue Comparison',\
            form=form)


##  Expressedgenes_consensustissue route.
#   Displays consensus tissue options, displays results.
@app.route('/TissueComparison/ConsensusTissue', methods=['GET', 'POST'])
def tissuecomparison_consensustissue():
    # Query all Samples to find unique tissues.
    # This is not optimal, working on a permanent, efficient query.
    all_samples = Sample.query.all()
    unique_tissues = []

    # Loops each sample to add unique to all_tissues.
    for each in all_samples:
        if each.tissue not in unique_tissues:
            unique_tissues.append(each.tissue)

    # Sets choices to unique tissues.
    choices = [(i, unique_tissues[i]) for i in range(len(unique_tissues))]

    # Initializes Consensus tissue form.
    form = TissueComparisonForm_Consensus()
    # Sets choices to unique tissues.
    form.select_tissue1.choices = choices
    form.select_tissue2.choices = choices

    # If form is valid, submit form.
    if form.validate_on_submit():
        # Initialize results to empty list.
        results = []
        
        start = timeit.default_timer()
        # Proportion for consensus calculation from entry field.
        calc1 = float(db.session.query(Sample)\
                .filter(Sample.tissue==choices[form.select_tissue1.data][1])\
                .count() * form.proportion.data)
        calc2 = float(db.session.query(Sample)\
                .filter(Sample.tissue==choices[form.select_tissue2.data][1])\
                .count() * form.proportion.data)

        if form.boolean_expression.data == 'AND':
            # Loops GeneQual database for all genes.
            for each in db.session.query(GeneQual).all():
                # Query Sample, Gene database.
                # Query Sample and Gene reference,
                #       First filter: tissue type.
                #       Second filter: each gene id in loop and barcode is True.
                # If the count of query is >= proportion,
                #       Append gene to results.
                if db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue1.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() >= calc1\
                    and db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue2.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() >= calc2:
                            results.append(each)

        elif form.boolean_expression.data == 'OR':
            # Loops GeneQual database for all genes.
            for each in db.session.query(GeneQual).all():
                # Query Sample, Gene database.
                # Query Sample and Gene reference,
                #       First filter: tissue type.
                #       Second filter: each gene id in loop and barcode is True.
                # If the count of query is >= proportion,
                #       Append gene to results.
                if db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue1.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() >= calc1\
                    or db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue2.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() >= calc2:
                            results.append(each)
        elif form.boolean_expression.data == 'XOR':
            # Loops GeneQual database for all genes.
            for each in db.session.query(GeneQual).all():
                # Query Sample, Gene database.
                # Query Sample and Gene reference,
                #       First filter: tissue type.
                #       Second filter: each gene id in loop and barcode is True.
                # If the count of query is >= proportion,
                #       Append gene to results.
                if (db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue1.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() >= calc1)\
                    ^ (db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue2.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() >= calc2):
                            results.append(each)
        elif form.boolean_expression.data == 'NOR':
            # Loops GeneQual database for all genes.
            for each in db.session.query(GeneQual).all():
                # Query Sample, Gene database.
                # Query Sample and Gene reference,
                #       First filter: tissue type.
                #       Second filter: each gene id in loop and barcode is True.
                # If the count of query is >= proportion,
                #       Append gene to results.
                if (db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue1.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() <= calc1)\
                    and (db.session.query(Sample)\
                        .outerjoin(Sample.genes)\
                        .filter(Sample.tissue==choices[form.select_tissue2.data][1],\
                            Gene.gene_id==each.gene_id,\
                            Gene.barcode==True)\
                        .count() <= calc2):
                            results.append(each)
        stop = timeit.default_timer()
        print('Time: ', stop-start)
        # Render results.
        return render_template('results.html',\
                title='Results',\
                results=results)

    # Render consensus tissue selection page.
    return render_template('tissuecomparison_consensustissue.html',\
            title='Expressed Genes',\
            form=form)


'''
@app.route('/GeneCatalog', methods=['GET', 'POST'])
def genecatalog():
    
'''
