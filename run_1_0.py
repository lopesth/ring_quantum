# -*- coding: UTF-8 -*-
"""
Python 2.7

Created on Thu Dec  8 08:45:17 BRST 2016

Author: @thiago_o_lopes / lopes.th.o@gmail.com

Submit the calculation, adapted for the Cluster UnB IQ and for the Gatech

"""

import os, sys
class G09_calculation_unb(object):

	def __init__(self, name_file, mem, cpus, cluster):
		self.mem = int(mem)
		self.cpus = str(cpus)
		self.cluster = str(cluster)
		self.name_file = str(name_file)

	def sub_unb_iq(self):
		memory = str(self.mem)+'000' 
		yes_file = open('yes.txt','w')
		yes_file.write("y")
		yes_file.close()
		nome_com=self.name_file+'.com'
		command = "llg09new "+nome_com+" -mem "+memory+" -ncpus "+self.cpus+" "+self.cluster+" < yes.txt"
		print (command)
		x = (os.popen(command, 'r', 1).read().split()[-1]).split('.')[0]
		return x

class G09_calculation_gatech(object):

	def __init__(self,name_file, mem, cpus, cluster, mail):
		self.name_file = name_file
		self.mail = mail
		self.mem = mem
		self.cluster = cluster
		self.cpus = cpus

	def sub_gatech(self):
		name_opt=self.name_file+'.opt'
		name_com=self.name_file+'.com'
		try:
			os.remove(name_opt)
		except OSError:
			pass
		sub_file = open(name_opt,'a')
		sub_file.write("#!/bin/bash\n \n")
		sub_file.write("#PBS -j oe\n")
		sub_file.write("#PBS -l nodes=%s:ppn=1\n" %self.cpus)
		sub_file.write("#PBS -l pmem=%sgb\n" %(self.mem))
		sub_file.write("#PBS -N %s\n" %(self.name_file))
		sub_file.write("#PBS -V\n")
		sub_file.write("#PBS -q %s\n" %(self.cluster))
		sub_file.write("#PBS -l walltime=120:00:00\n")
		sub_file.write("#PBS -m e\n")
		sub_file.write("#PBS -M %s \n \n" %(self.mail))
		sub_file.write("## source the Gaussian environment\n")
		sub_file.write("export g09root=/usr/local/pacerepov1/gaussian/G09D01LINDA\n")
		sub_file.write(". ${g09root}/g09/bsd/g09.profile\n")
		sub_file.write("export PATH=$TMPDIR:$PATH\n")
		sub_file.write("EXE=$g09root/g09/g09\n \n \n")
		sub_file.write("cd $PBS_O_WORKDIR\n \n")
		sub_file.write("myscratch=$HOME/scratch/$(echo $PBS_JOBID | cut -d\".\" -f1); export myscratch\n \n")
		sub_file.write("for i in $(cat $PBS_NODEFILE);\n")
		sub_file.write("do echo \"Creating scratch directoy \" $myscratch \" on \" $i; \n")
		sub_file.write("#bpsh $i\n")
		sub_file.write("mkdir $myscratch;\n")
		sub_file.write("done\n")
		sub_file.write("export GAUSS_SCRDIR=$myscratch \n \n")
		sub_file.write("/bin/rm -f tmp_nodefile\n")
		sub_file.write("for host in $(cat $PBS_NODEFILE); do\n")
		sub_file.write("  echo \"${host}-ib\" >> tmp_nodefile \n")
		sub_file.write("done\n")
		sub_file.write("\n \n")
		temp_nodes = "\"`cat tmp_nodefile`"
		bar = "\\"
		sub_file.write("export NODES=%s%s%s\" \n" %(bar, temp_nodes, bar) )
		sub_file.write("export GAUSS_LFLAGS=\"-nodefile tmp_nodefile -vv\" \n \n")
		sub_file.write("cat tmp_nodefile\n")
		sub_file.write("#cd  \$myscratch;\n")
		sub_file.write("date\n")
		sub_file.write("g09 %s \n" %(name_com))
		sub_file.write("date\n \n")
		sub_file.write("#\n \n")
		sub_file.write("for i in $(cat $PBS_NODEFILE);\n")
		sub_file.write("do echo \"Removing scratch directoy \" $myscratch \" on \" $i; \n")
		sub_file.write("#bpsh $i \n")
		sub_file.write("rm -r -f $myscratch; \n")
		sub_file.write("done\n \n \n")
		sub_file.close()

		change_mod_command = "chmod +x "+name_opt
		sub_command = "qsub "+name_opt
		x = os.popen(sub_command, 'r', 1).read().split('.')[0]
		return x


		
