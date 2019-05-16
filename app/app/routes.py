from flask import render_template, flash, redirect, url_for, request, send_file

import os

from app import app, db
from app.models import Sample, Gene
from app.forms import ExpressedGenesForm, ExpressedGenesForm_Consensus


##  Index route.
#   The home webpage.
@app.route('/')
@app.route('/index')
def index():
    # Renders index.
    return render_template('index.html', title='Home')


@app.route('/ExpressedGenes', methods=['GET', 'POST'])
def expressedgenes():
    form = ExpressedGenesForm()
    
    if form.validate_on_submit():
        if form.input_type.data == 'Consensus Tissue':
            return redirect(url_for('expressedgenes_consensustissue'))
        else:
            flash(form.input_type.data)
            return redirect(url_for('index'))
    return render_template('expressedgenes.html', title='Expressed Genes', form=form)


@app.route('/ExpressedGenes/ConsensusTissue', methods=['GET', 'POST'])
def expressedgenes_consensustissue():
    all_samples = Sample.query.all()
    all_tissues = []

    for each in all_samples:
        if each.tissue not in all_tissues:
            all_tissues.append(each.tissue)
    
    choices = [(i, all_tissues[i]) for i in range(len(all_tissues))]

    form = ExpressedGenesForm_Consensus()
    form.select_tissue.choices = choices

    if form.validate_on_submit():
        flash(choices[form.select_tissue.data][1])
        return redirect(url_for('index'))
    return render_template('consensustissue.html', title='Consensus Tissue', form=form)


@app.route('/ExpressedGenes/ConsensusTissues/Results')
def expressedgenes_consensustissue_results(query_this):
    

