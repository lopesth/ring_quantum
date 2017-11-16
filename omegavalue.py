# -*- coding: UTF-8 -*-
"""
Created on Thu Dec  13 10:47:29 BRST 2016

Author: @thiago_o_lopes / lopes.th.o@gmail.com
 
Program using the 'Golden Section Search' to minimize the omega, through the G09 package

"""
# ____________________________________________ Imports _________________________________________________

from energies_1_0 import *
from input_1_0 import *
from checkcalc_1_0 import *
from run_1_0 import *
from goldenSectionSearch import *
import sys, linecache

# ____________________________________________ Functions _______________________________________________

def w_set(w1, w2):
	w3 = newGoldenValue(w1, w2)

def iq_unb_system(g09_input_name, omega):
	x = OmegaInput(g09_input_name, originalFileName, method, basis, omega, charge, mult, complement)
	x.copy_chk()
	x.create_input()
	xrun = G09_calculation_unb(g09_input_name, mem, cpus, cluster)
	job_list.append(xrun.sub_unb_iq())
	run_name_list.append(g09_input_name)

def gatech_system(g09_input_name, omega):
	x = OmegaInput(g09_input_name, originalFileName, method, basis, omega, charge, mult, complement)
	x.copy_chk()
	x.create_input()
	xrun = G09_calculation_gatech(g09_input_name, mem, cpus, cluster, mail)
	job_list.append(xrun.sub_gatech())
	run_name_list.append(g09_input_name)

def generic_desktop_system(g09_input_name, omega):
	x = OmegaInput(g09_input_name, originalFileName, method, basis, omega, charge, mult, complement)
	x.copy_chk()
	x.create_input(g09_input_name, mem, cluster, mail)
	print ('This has not been established yet.')
	sys.exit()


def J2_calc(molecule_j2):
	yneutral = find_in_a_energy(str(molecule_j2)+'_n_w_'+''.join(('%.4f' %(w_middle)).split('.'))+'.log')
	ycation = find_in_a_energy(str(molecule_j2)+'_c_w_'+''.join(('%.4f' %(w_middle)).split('.'))+'.log')
	yanion = find_in_a_energy(str(molecule_j2)+'_a_w_'+''.join(('%.4f' %(w_middle)).split('.'))+'.log')
	
	eNeutral = float(yneutral.energy())
	eCation = float(ycation.energy())
	eAnion = float(yanion.energy())
	eHomoNeutral = float(yneutral.homo_lumo()['HOMO'])
	eHomoAnion = float(yanion.homo_lumo()['HOMO'])
	
	jip = eHomoNeutral + (eCation - eNeutral)
	jea = eAnion +(eNeutral - eAnion)
	j2 = (jip*jip) + (jea*jea)
	j2_list.append(j2)

# _________________________________ Pick up input file attributes ______________________________________

inputFileName = sys.argv[-1]
print(linecache.getline(inputFileName, 8))
originalFileName = list(linecache.getline(inputFileName, 8).split()[4]).split('.')[0]
method = list(linecache.getline(inputFileName, 21).split()[1]).split('\"')[1]
basis = list(linecache.getline(inputFileName, 21).split()[5]).split('\"')[1]
charge = list(linecache.getline(inputFileName, 25).split()[1])
mult = list(linecache.getline(inputFileName, 25).split()[4])
mem = list(linecache.getline(inputFileName, 17).split()[3])
cluster = list(linecache.getline(inputFileName, 16).split()[2])
cpus = list(linecache.getline(inputFileName, 18).split()[3])
complement = ' '.join(list(linecache.getline(inputFileName, 22).split()[2:])).split('\"')[1]
w_startvalue = float(list(linecache.getline(inputFileName, 29)).split()[5])
w_endvalue = float(list(linecache.getline(inputFileName, 30).split())[6])
mail = str(list(linecache.getline(inputFileName, 34)).split()[1])

# ______________________________________________________________________________________________________

print (' _____________________________________________________________\n')
print ('	 Leedmol G09 Omega and Jgap minimization 1.0\n')
print (' This program was made by Thiago Lopes - lopes.th.o@gmail.com \n')
print (' _____________________________________________________________')

try:
	originalCHKname = originalFileName+'.chk'
	temp = open(originalCHKname, 'r')
	del originalCHKname
	temp.close()
	print ('OK, I found a checkpoint file (%s.chk), let\'s proceed.' %(originalFileName))
except IOError:
	print ('An error has occurred, the checkpoint file (%s.chk) is not in the working directory' %(originalFileName))
	sys.exit()

system_chosen = []
if (linecache.getline(inputFileName, 11).split()[2]) == '(X)':
	system_chosen.append('Cluster IQ-UnB')
if (linecache.getline(inputFileName, 11).split()[6]) == '(X)':
	system_chosen.append('Cluster Gatech')
if (linecache.getline(inputFileName, 11).split()[11]) == '(X)':
	system_chosen.append('Generic Desktop System')

if len(system_chosen) >= 2:
	print ('You should choose only one calculation system. You have chosen:')
	print (", ".join(system_chosen))
	sys.exit()
else:
	pass

print ('You chose the system: %s' %(system_chosen[0]))

counter_j2 = 0
j2_list = []
condition = ''
while condition != 'Stop':
	w_set = newGoldenValue(w_startvalue , w_endvalue)
	w_middle = w_set.newValue()

	omega_mol_list = []
	job_list = []
	run_name_list = []
	for omega in w_startvalue, w_endvalue, w_middle:

		omega_title = ''.join(('%.4f' %(omega)).split('.'))		

		for charge_of_molecule in 'c', 'a', 'n':

			if charge_of_molecule == 'c':
				charge = str(1)
				mult = str(2)
			elif charge_of_molecule == 'a':
				charge = str(-1)
				mult = str(2)
			else:
				pass

			FileName = str(originalFileName)+'_'+charge_of_molecule+'_w_'+omega_title
			omega_mol_list.append(FileName)
			if system_chosen[0] == 'Cluster IQ-UnB':
				iq_unb_system(FileName, omega)
			elif system_chosen[0] == 'Cluster Gatech':
				gatech_system(FileName, omega)
			elif system_chosen[0] == 'Generic Desktop System':
				generic_desktop_system(FileName, omega)

	print ('The following calculations were submitted: %s' %(omega_mol_list))
	m = check_calculation(job_list, run_name_list)
	result_job = m.check_g09()

	if result_job == "Done":
		print ('The calculations jobs (of the interval of omega between %.4f and %.4f) finished the execution.' %(w_startvalue, w_endvalue))
	elif result_job == "Error":
		print ('One of the calculations jobs (from the omega interval between %.4f and %.4f) encountered an error during execution' %(w_startvalue, w_endvalue))
		sys.exit()
	else:
		print ('An error occurred in the library \'checkcalc\'' )
		sys.exit()

	J2_calc(originalFileName)

	if len(j2_list) != 1:
		if float(j2_list[counter_j2]) < float(j2_list[counter_j2 - 1]):
			w_startvalue = w_middle
			w_endvalue = w_endvalue
		if float(j2_list[counter_j2]) > float(j2_list[counter_j2 - 1]):
			w_startvalue = w_startvalue
			w_endvalue = w_middle
		else:
			print ('It\'s over')
			condition = 'Stop'
	else:
		w_startvalue = w_middle
		w_endvalue = w_endvalue

	counter_j2 +=1







