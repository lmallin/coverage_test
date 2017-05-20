#!/usr/bin/env python

#################################

# File name: covergae.py
# Author: Lucy Mallin
# Date created: 16/05/2017
# Date last modified: 20/05/2017
# Python version: 2.7
# License:

#################################

import sys
import pandas as pd
import pdfkit
import argparse
from jinja2 import Environment, FileSystemLoader
from collections import Counter


class Coverage(object):
	""" Take an input file and identify genes with 30x coverage below 100%"""

	def __init__(self, input_file, output_file):
		""" iniitalise file location arguments """
		self.input_file = input_file
		self.output_file = output_file
	
				
	def load_data(self):
		""" load data from input file to pandas dataframe.  Name columns and define index """
		self.data = pd.read_csv(self.input_file, sep="\t", comment='#', header=None)
		self.data.columns=['Chrom','Start Position', 'End Position','FullPosition', 'NotUsed','NotUsed','GeneSymbol;Accession','Gene Size','Read Count','Mean Coverage','% Coverage at 30x','Sample Name']
		self.data['Gene Symbol'], self.data['Accession'] = self.data['GeneSymbol;Accession'].str.split(';', 1).str
		self.indexed = self.data.set_index(['Chrom','Start Position', 'End Position',])
		self.filter_data()
		self.test_load()
		
	def filter_data(self):
		""" group the data by Gene then apply a lambda filter to get rows where 30x coverage is below 100% """
		self.genes_lowcoverage = self.indexed.groupby(['Sample Name', 'Gene Symbol' , 'Accession', 'Gene Size']).apply(lambda x: x[x['% Coverage at 30x'] < 100])
		self.gene_summary()
		self.test_values()
	
	def gene_summary(self):
		""" define some summary stats - count the number of regions within each gene with < 100% coverage """
		per_gene_count = self.genes_lowcoverage.index.get_level_values(1)
		self.summary = Counter(per_gene_count)
		self.make_report()
	
	def make_report(self):
		""" make a pdf report to display the data """
		sys.stdout.write("Generating Coverage Report...")
		env = Environment(loader=FileSystemLoader('.'))
		template = env.get_template('coverage_report.html')
		title = "Gene Coverage Report"
		css = 'style.css'
		header=['Read Count','Mean Coverage','% Coverage at 30x']
		options = {
			'page-size': 'A4',
			'margin-top': '0.75in',
			'margin-right': '0.75in',
			'margin-bottom': '0.75in',
			'margin-left': '0.75in',
			'encoding': "UTF-8", 
		}
		 
		# Test if pdfkit is installed, if not write to csv
		pdfkit.from_string(env.get_template('coverage_report.html').render(genes_lowcoverage=self.genes_lowcoverage.to_html(columns=header), summary=self.summary, input_file=self.input_file), self.output_file, options=options, css=css)

	def test_load(self):
		""" check there is data in the dataframe """
		if self.data.empty:
			sys.stdout.write("There was an error loading data from the file")
	
	def test_values(self):
		""" test to check if the any of the results pulled out have coverage = 100% """
		test = (self.genes_lowcoverage['% Coverage at 30x'] == 100).any()
		if test == True:
			sys.stdout.write("check output")


if __name__ == '__main__':
	""" Create argument options for command line when running the program """
	parser = argparse.ArgumentParser(description='Database connection options')
	parser.add_argument('-i', help='input file location', action='store', dest='input_file', required=True)
	parser.add_argument('-o', help='desired output file location', action='store', default='coverage_report.pdf', dest='output_file')
	args = parser.parse_args()
	coverage = Coverage(args.input_file, args.output_file)
	coverage.load_data()

	