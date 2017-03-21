import argparse
import math
import numpy as np

"""Values below have been obtained from: http://www.crbond.com/papers/bsf2.pdf Frequency normalized table
Alternating capacitor and inductor values for normalized filter at cut-off freq 1 rad/sec impedance 1 ohm
"""
class Filter_design(object):

	normalizedBesselCoefficients = {   '1' :[2.000],
									   '2' :[2.1478, 0.5755],
									   '3' :[2.2034, 0.9705, 0.3374],
									   '4' :[2.2404, 1.0815, 0.6725, 0.2334],
									   '5' :[2.2582, 1.1110, 0.8040, 0.5072, 0.1743],
									   '6' :[2.2645, 1.1126, 0.8538, 0.6392, 0.4002, 0.1365],
									   '7' :[2.2659, 1.1052, 0.8690, 0.7020, 0.5249, 0.3259, 0.1106],
									   '8' :[2.2656, 1.0956, 0.8695, 0.7303, 0.5936, 0.4409, 0.2719, 0.0919],
									   '9' :[2.2649, 1.0862, 0.8639, 0.7407, 0.6306, 0.5108, 0.3769, 0.2313, 0.07797],
									   '10':[2.2641, 1.0781, 0.8561, 0.7420, 0.6493, 0.5528, 0.4454, 0.3270, 0.2000, 0.0672]}

	normalizedChebyshevCoefficients = { '2': [0.4489, 0.4078],
										'3': [0.6292, 0.9703, 0.6292],
										'4': [0.7129, 1.2004, 1.3213, 0.6476],
										'5': [2.20715, 1.12798, 3.10248, 1.12798, 2.20715],
										#'5': [0.7563, 1.3049, 1.5773, 1.3049, 0.7563],
										#'5': [1.7058 ,	1.2296, 	2.5409, 	1.2296, 	1.7058],
										'6': [0.7814, 1.3600, 1.6897, 1.5350, 1.4970, 0.7098],
										'7': [0.7970, 1.3924, 1.7481, 1.6331, 1.7481, 1.3924, 0.7970],
										'8': [0.8073, 1.4131, 1.7824, 1.6833, 1.8529, 1.6193, 1.5555, 0.7334],
										'9': [0.8145, 1.4271, 1.8044, 1.7125, 1.9058, 1.7125, 1.8044, 1.4271, 0.8145]}

	normalizedButterworthCoefficients = {
									   '1' :[2.000],
									   '2' :[1.41421, 1.41421],
									   '3' :[1.00000, 2.00000, 1.00000],
									   '4' :[0.76537, 1.84776, 1.84776,	0.76537],
									   '5' :[0.61803, 1.61803, 2.00000,	1.61803, 0.61803],
									   '6' :[0.51764, 1.41421, 1.93185,	1.93185, 1.41421, 0.51764],
									   '7' :[0.44504, 1.24698, 1.80194,	2.00000, 1.80194, 1.24698, 0.44504],
									   '8' :[0.39018, 1.11114, 1.66294,	1.96157, 1.96157, 1.66294, 1.11114,	0.39018],
									   '9' :[0.34730, 1.00000, 1.53209,	1.87938, 2.00000, 1.87938, 1.53209,	1.00000, 0.34730],
									   '10':[0.31287, 0.90798, 1.41421, 1.78201, 1.97538, 1.97538, 1.78201,	1.41421, 0.90798, 0.31287]}
	def __init__(self, filter_name):
		self.filter_name = filter_name		
		
	def CapInductCheb(self, order):
		"""Return normalized chebyshev filter coefficients 0.1 dB ripple"""
		Cap = self.normalizedChebyshevCoefficients.__getitem__(str(order))[0:][::2]
		Inductor = self.normalizedChebyshevCoefficients.__getitem__(str(order))[1:][::2]
		
		return Cap, Inductor

	def CapInductBess(self, order):
		"""Return normalized besself filter coefficients"""
		Cap = self.normalizedBesselCoefficients.__getitem__(str(order))[0:][::2]
		Inductor = self.normalizedBesselCoefficients.__getitem__(str(order))[1:][::2]
		
		return Cap, Inductor
		
	def CapInductButter(self, order):
		"""Return normalized butterworth filter coefficients"""
		Cap = normalizedButterworthCoefficients.__getitem__(str(order))[0:][::2]
		Inductor = normalizedButterworthCoefficients.__getitem__(str(order))[1:][::2]
		
		return Cap, Inductor

	def lowpass_inductance(self, L, R, F):
		"""Return low pass inductor value"""
		return (L * R) / (2 * math.pi * F)

	def lowpass_capacitance(self, C, R, F):
		"""Return low pass capacitor value"""
		return C / (2 * math.pi * F * R)

	def highpass_inductance(self, R, F, C):
		"""Return high pass inductor value"""
		return R / (2 * math.pi * F * C)

	def highpass_capacitance(self, L, F, R):
		"""Return high pass capacitor value"""
		return 1 / (2 * math.pi * F * R * L)

	def bandpasslcp(self, R, L, Fu, Fl ):
		"""Return banpass parallel inductor and capacitor values"""
		C1 = (Fu-Fl) / (2 * math.pi * Fu * Fl * R * L)
		L1 = (R * L) / (2 * math.pi * (Fu - Fl))

		return (C1, L1)

	def bandpasslcs(self, R, C, Fu, Fl):
		"""Return banpass series inductor and capacitor values"""
		C2 = C / (2 * math.pi * (Fu - Fl) * R)
		L2 = ((Fu - Fl) * R) * (2 * math.pi * Fu * Fl * C)

		return (C2, L2)

	def lowpass_filter(self, C, L, cut_off):
		"""Calculate  lowpass filter"""	
		impedance = 50	
		items_dict = {}
		Cap = C
		Inductor = L
		for i,l in enumerate (Inductor, start=1):
			ind = "L%d"%i
			items_dict[ind] = self.lowpass_inductance(i, impedance, cut_off)

		for i,c in enumerate (Cap, start=1):
			cap = "C%d"%i
			items_dict[cap] = self.lowpass_capacitance(c, impedance, cut_off)		

		return self.standardLC(items_dict)

	def highpass_filter(self, order, cut_off, impedance):
		"""Calculate highpass filter"""
		items_dict = {}
		for i, l in enumerate(Inductor):
			ind = "L%d"%(i)
			items_dict[ind] = highpass_inductance(l, R, F)

		for i, c in enumerate(Cn):
			cap = "C%d"%(i)
			items_dict[cap] = highpass_capacitance(c, R, F)
		standardLC(items_dict, fname)
		
	
	def standardLC(self, components_dict):	
		"""Return standard Capacitor and Inductor E12 values"""
		
		E12Components = {}
		for part in components_dict:
			if part[0] == 'L':
				E12Components[part] = self.get_approximate(components_dict[part])

			elif part[0] == 'C':
				E12Components[part] = self.get_approximate(components_dict[part])
		#responsecurve.responsecurve(E12Components) #pass dictionary to responsecurve constructor
		self.print_values(E12Components)

		return E12Components
		
	def get_approximate(self, val):
		"""Approximates closest component value to E12 standards"""

		standardE12 = [1, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

		val_ = np.floor(np.log10(np.abs(val)))
		i  = val * (math.pow(10, val_*(np.sign(val_))))
		j =  ((round(i,1)))
			
		return((min(standardE12, key=lambda x:abs(x-j)))*math.pow(10,val_))	

	def inductor_design(self, inductance):
		pass

	def print_values(self, E12Components):
		"""Print sorted required components values"""
		for key in sorted(E12Components):
			print ("%s : %s")%(key, E12Components[key])


