# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Thu Dec  8 08:45:17 BRST 2016

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Find the total energy, HOMO and LUMO in a file calculated in G09

"""
import linecache

class find_in_a_energy(object):

	def __init__(self,file):
		self.file = str(file)

	def homo_lumo(self):
		lookup = 'Alpha  occ. eigenvalues'
		myLog = open (self.file, 'r')
		for num, line in enumerate(myLog, 1):
			if lookup in line:
				last_line = int(num)

		line_homo = linecache.getline(self.file, last_line)
		homo = line_homo.split()[-1]
		line_lumo = linecache.getline(self.file, last_line + 1)
		lumo = line_lumo.split()[4]
		homoNlumo = {'HOMO' : homo, 'LUMO' : lumo}
		return homoNlumo

	def energy(self):
		lookup = 'Done'
		myLog = open (self.file, 'r')
		for num, line in enumerate(myLog, 1):
			if lookup in line:
				last_line = int(num)
		line_energy = linecache.getline(self.file, last_line)
		energy = line_energy.split()[4]
		return float(energy)