import ahkab
from ahkab import printing, time_functions, circuit 
from filter_design import standardLC
import pylab as plt
import numpy as np	
from matplotlib.widgets import Cursor
	
class Responsecurve(object):
	"""
	Responsecurve class simulates the behaviour of a filter constructed from filter_design script
	ref : http://ecee.colorado.edu/~mathys/ecen2420/pdf/UsingFilterTables.pdf
	"""
	def __init__(self, E12Components):
		"""Class constructor, initialises components dictionary"""
		self.E12Components = E12Components		
		self.plot_schematic()
	
	def plot_schematic(self):
		"""Build circuit netlist and graph AC analysis under a pulse input"""
		it = 0
		
		schematic = circuit.Circuit("Filter Response Curve")	
		gnd = schematic.get_ground_node()
	
		for partID in sorted(self.E12Components):
			if (partID[0] == 'C'):
				it += 1
				schematic.add_capacitor(partID, n1="n%s"%(partID[1]), n2=gnd, value=self.E12Components[partID])
			elif (partID[0] == 'L'):
				schematic.add_inductor(partID, n1="n%s"%(partID[1]), n2="n%s"%(int(partID[1])+1), value=self.E12Components[partID])
				
		voltage_step = time_functions.pulse(v1=0, v2=5, td=0, tr=1e-9, pw=2, tf=1e-9, per=2e-3)
		
		#input and output impedance need to be the same
		schematic.add_resistor("Rs", n1="n0", n2="n1", value=50)
		if (it%2 == 0):
			it = it + 1
		schematic.add_resistor("Rl", n1="n%d"%(it), n2=gnd, value=50)
		schematic.add_vsource("V1", n1="n0", n2=gnd, dc_value=5, ac_value=2, function=voltage_step)
				
		print (schematic)
				
		
		ac_analysis = ahkab.new_ac(start=1e3, stop=200e6, points=100)	
		r = ahkab.run(schematic, an_list=[ac_analysis])
		fig = plt.figure()
		
		plt.subplot(211)
		plt.ylabel("Gain [dB]")		
		plt.title(" - AC simulation")	
		plt.semilogx(r['ac']['f'], 20*np.log10(np.abs(r['ac']['Vn%d'%(it)])/np.abs(r['ac']['Vn%d'%(it)]).max()))		
		plt.subplot(212)
		plt.grid(True)
		plt.semilogx(r['ac']['f'], np.angle(r['ac']['Vn%d'%(it)]))
		plt.ylabel("Phase")	
		plt.xlabel("Frequency [Hz]")
		plt.show()



