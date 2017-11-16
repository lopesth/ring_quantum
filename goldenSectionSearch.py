# -*- coding: UTF-8 -*-
"""
Created on Thu Dec  11 17:45:22 BRST 2016

Author: @thiago_o_lopes / lopes.th.o@gmail.com
 
Program using the 'Golden Section Search' to minimize X

"""
import math 

class newGoldenValue(object):

	def __init__(self, x_start, x_end):
		self.x_start = x_start
		self.x_end = x_end

	def newValue(self):
		golden = (math.sqrt(5)-1)/2
		new_x = float(self.x_end - ((self.x_end - self.x_start) * golden))
		return new_x
