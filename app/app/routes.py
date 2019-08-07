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
from app.models import Tissue, Gene, GeneQual
#   Import entry forms.
from app.forms import ExpressedGenesForm, TissueComparisonForm, GeneCatalogForm


##  Index route.
#   The home webpage.
@app.route('/')
@app.route('/index')
def index():
    # Renders index.
    return render_template('index.html', title='Home')


##  Expressedgenes route.
#   Displays consensus tissue options, displays results.
@app.route('/ExpressedGenes', methods=['GET', 'POST'])
def expressedgenes():
    # Query tissues.
    all_tissues = Tissue.query.all()

    # Sets choices to unique tissues.
    choices = [(i, all_tissues[i].tissue) for i in range(len(all_tissues))]
    
    # Initializes Consensus tissue form.
    form = ExpressedGenesForm()
    # Sets choices to unique tissues.
    form.select_tissue.choices = choices
    
    # If form is valid, submit form.
    if form.validate_on_submit():
        # Initialize results to empty list.
        results = []

        genes = Tissue.query.filter_by(tissue=choices[form.select_tissue.data][1]).first().genes

        for each in genes:
            if each.barcode_count >= each.total_count * form.proportion.data:
                gene = GeneQual.query.filter_by(gene_id=each.gene_id).first()
                results.append(gene)
        
        # Render results.
        return render_template('results.html',
                title='Results',
                results=results)
    
    # Render consensus tissue selection page.
    return render_template('expressedgenes.html',
            title='Expressed Genes',
            form=form)


##  Expressedgenes_consensustissue route.
#   Displays consensus tissue options, displays results.
@app.route('/TissueComparison', methods=['GET', 'POST'])
def tissuecomparison():
    # Query all Samples to find unique tissues.
    # Sets choices to unique tissues.
    all_tissues = Tissue.query.all()
    choices = [(i, all_tissues[i].tissue) for i in range(len(all_tissues))]

    # Initializes Consensus tissue form.
    form = TissueComparisonForm()
    # Sets choices to unique tissues.
    form.select_tissue1.choices = choices
    form.select_tissue2.choices = choices

    # If form is valid, submit form.
    if form.validate_on_submit():
        # Initialize results to empty list.
        results = []
        genes1 = Tissue.query.filter_by(tissue=choices[form.select_tissue1.data][1]).first().genes
        genes2 = Tissue.query.filter_by(tissue=choices[form.select_tissue2.data][1]).first().genes
        
        if form.boolean_expression.data == 'AND':
            for each1, each2 in zip(genes1, genes2):
                if each1.barcode_count >= each1.total_count * form.proportion.data and each2.barcode_count >= each2.total_count * form.proportion.data:
                    gene = GeneQual.query.filter_by(gene_id=each1.gene_id).first()
                    results.append(gene)

        elif form.boolean_expression.data == 'OR':
            for each1, each2 in zip(genes1, genes2):
                if (each1.barcode_count >= each1.total_count * form.proportion.data) or (each2.barcode_count >= each2.total_count * form.proportion.data):
                    gene = GeneQual.query.filter_by(gene_id=each1.gene_id).first()
                    results.append(gene)
        
        elif form.boolean_expression.data == 'XOR':
            for each1, each2 in zip(genes1, genes2):
                if (each1.barcode_count >= each1.total_count * form.proportion.data) != (each2.barcode_count >= each2.total_count * form.proportion.data):
                    gene = GeneQual.query.filter_by(gene_id=each1.gene_id).first()
                    results.append(gene)
        
        elif form.boolean_expression.data == 'NOR':
            for each1, each2 in zip(genes1, genes2):
                if (each1.barcode_count <= each1.total_count * form.proportion.data) and (each2.barcode_count <= each2.total_count * form.proportion.data):
                    gene = GeneQual.query.filter_by(gene_id=each1.gene_id).first()
                    results.append(gene)

        
        # Render results.
        return render_template('results.html',\
                title='Results',\
                results=results)

    # Render consensus tissue selection page.
    return render_template('tissuecomparison.html',\
            title='Expressed Genes',\
            form=form)


'''
@app.route('/GeneCatalog', methods=['GET', 'POST'])
def genecatalog():
    form = GeneCatalogForm()
    
    if form.validate_on_submit():
        # = []
        
        for each in form.text_entry.data.split():
            if each[:4] == 'ENSG':
                
            else:
                print(each + 'no')
        print(form.input_type.data)
        return redirect(url_for('index'))
        
    return render_template('genecatalog.html',
            title='Gene Catalog',
            form=form)
'''
