# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Sat Dec  11 09:06:38 BRST 2016

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Check if calculations have been completed in a qsub system

"""
import os, sys, time
class check_calculation(object):

	def __init__(self, input_list, run_name_list):
		self.input_list = input_list
		self.run_name_list = run_name_list

	def check_g09(self):

		result_qstat = []
		result_finished = {}
		calculations_error = []
		y = True
		w = True
		while y == True or w == True:
			result_qstat = []
			for input_element in self.input_list:
				command = "qstat -t "+input_element
				try:
					result_qstat.append(os.popen(command, 'r', 1).read().split()[18])
				except IndexError:
					pass
			print (result_qstat)
			y = 'R' in result_qstat
			w = 'Q' in result_qstat
			time.sleep(60)

		for input_element in self.run_name_list:
			input_name = input_element+'.log'
			x = "Normal termination" in open(input_name, 'r').read()
			result_finished.update({ input_name : x })
		
		print (result_finished)

		for key_result_finished, value_result_finished in result_finished.items():
			if value_result_finished == False:
				calculations_error.append(key_result_finished)

		if len(calculations_error) != 0:
			return "Error"
		else:
			return "Done"



