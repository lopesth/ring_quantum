# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Sat Dec  10 17:21:15 BRST 2016

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Creating input from omega minimization files

"""
import os, sys, linecache

class OmegaInput(object):

	def __init__(self, name, original, method, basis, omega, charge, mult, complement):
		self.name = str(name)
		self.original = str(original)
		self.method = str(method)
		self.basis = str(basis)
		self.omega = float(omega)
		self.charge = int(charge)
		self.mult = int(mult)
		self.complement = complement

	def copy_chk(self):
		checkpoint_file = self.name+'.chk'
		original_checkpoint_file = self.original+'.chk'
		temp_chk = open(original_checkpoint_file, 'r')
		temp_chk_cache = temp_chk.read()
		temp_chk.close()
		try:
			os.remove(checkpoint_file)
		except OSError:
			pass
		chk_file = open(checkpoint_file,'a')
		chk_file.write(temp_chk_cache)
		chk_file.close()

	def create_input(self):
		percent = '%'
		checkpoint_file = self.name+'.chk'
		input_file_name = self.name+'.com'
		try:
			os.remove(input_file_name)
		except OSError:
			pass
		omega_std = '0' + ('%.9f' %(self.omega)).split('.')[1]
		input_file = open (input_file_name, 'a')
		input_file.write('%schk=%s \n' %(percent, checkpoint_file))
		input_file.write('%sNProcShared=4 \n' %(percent))
		input_file.write('%sMem=2000MB \n' %(percent))
		input_file.write('#p %s/%s %s iop(3/108=%s) iop(3/107=%s ) \n' %(
			self.method, self.basis, self.complement, omega_std, omega_std))
		input_file.write('# guess=read geom=check \n')
		input_file.write('\n')
		input_file.write('Calculation of file %s \n' %(self.name))
		input_file.write('\n')
		input_file.write('%d %d \n' %(self.charge, self.mult))
		input_file.write('\n')
		input_file.write('\n')
		input_file.close()


class GenericInput(object):

	def __init__(self, name, original, method, basis, charge, mult, complement):
		self.name = str(name)
		self.original = str(original)
		self.method = str(method)
		self.basis = str(basis)
		self.charge = int(charge)
		self.mult = int(mult)
		self.complement = str(complement)

	def create_input(self):
		percent = '%'
		checkpoint_file = self.name+'.chk'
		input_file_name = self.name+'.com'
		orig_geom_file = self.original+'.com'
		orig_geom_file_alternative = self.original+'.gjf'

		try:
			geom_file = open(orig_geom_file, "r")
		except IOError:
			try:
				geom_file = open(orig_geom_file_alternative, "r")
			except IOError:
				print ("No geometry file found in directory")
				raise

		lookup = ' 1 '
		for num, line in enumerate(geom_file, 1):
			if lookup in line:
				end_geom_file = int(num)-1
		start_geom_file = int(7)
		geom_file.close()

		try:
			os.remove(input_file_name)
		except OSError:
			pass

		input_file = open (input_file_name, 'a')
		input_file.write('%schk=%s \n' %(percent, checkpoint_file))
		input_file.write('%sNProcShared=4 \n' %(percent))
		input_file.write('%sMem=2000MB \n' %(percent))
		input_file.write('#p %s/%s %s \n' %(
			self.method, self.basis, self.complement))
		input_file.write('\n')
		input_file.write('Omega calculation of file %s \n' %(self.name))
		input_file.write('\n')
		input_file.write('%d %d \n' %(self.charge, self.mult))

		for line_number in range(start_geom_file, end_geom_file):
			try:
				temp = open(orig_geom_file)
				input_file.write(linecache.getline(orig_geom_file, line_number))
			except IOError:
				input_file.write(linecache.getline(orig_geom_file_alternative, line_number))

		input_file.write('\n')
		input_file.write('\n')
		input_file.write('\n')
		input_file.close()		

class GenericIputPCM(object):

	def __init__(self, name, original, method, basis, charge, mult, complement, solvent):
		super(GenericIputPCM, self).__init__(name, original, method, basis, charge, mult, complement)
		self.solvent = str(solvent)

	def create_input(self):
		percent = '%'
		checkpoint_file = self.name+'.chk'
		input_file_name = self.name+'.com'
		orig_geom_file = self.original+'.com'
		orig_geom_file_alternative = self.original+'.gjf'

		try:
			geom_file = open(orig_geom_file, "r")
		except IOError:
			try:
				geom_file = open(orig_geom_file_alternative, "r")
			except IOError:
				print ("No geometry file found in directory")
				raise

		lookup = ' 1 '
		for num, line in enumerate(geom_file, 1):
			if lookup in line:
				end_geom_file = int(num)-1
		start_geom_file = int(7)
		geom_file.close()

		try:
			os.remove(input_file_name)
		except OSError:
			pass

		input_file = open (input_file_name, 'a')
		input_file.write('%schk=%s \n' %(percent, checkpoint_file))
		input_file.write('%sNProcShared=4 \n' %(percent))
		input_file.write('%sMem=2000MB \n' %(percent))
		input_file.write('#p %s/%s %s scrf=(iefpcm, solvent=%s)\n' %(
			self.method, self.basis, self.complement, self.solvent))
		input_file.write('\n')
		input_file.write('Omega calculation of file %s \n' %(self.name))
		input_file.write('\n')
		input_file.write('%d %d \n' %(self.charge, self.mult))

		for line_number in range(start_geom_file, end_geom_file):
			try:
				temp = open(orig_geom_file)
				input_file.write(linecache.getline(orig_geom_file, line_number))
			except IOError:
				input_file.write(linecache.getline(orig_geom_file_alternative, line_number))

		input_file.write('\n')
		input_file.write('\n')
		input_file.write('\n')
		input_file.close()		

