from flask import Flask, request, render_template
from filter_design import Filter_design
#from responsecurve import Responsecurve
app = Flask(__name__)

@app.route('/')
def index():
	
	return render_template("home.html")
	
@app.route("/filteroutput", methods=["POST"])
def filter_design():
	
	filter_name = request.form['filter']
	order = request.form['order']
	cut_off = int(request.form['cutoff'])
	
	funits = request.form['funits']
	if (funits == 'MHz'):
		 cut_off *= 1e6
	elif (funits == 'KHz'):
		 cut_off *= 1e3
	
	filter_response = request.form['FilterResponse']
	parts = {}
	if (filter_response == 'Lowpass'):
		if (filter_name == 'Bessel'):	
			B = Filter_design('Bessel')	
			Cbessel, Lbessel = B.CapInductBess(order)
			parts = B.lowpass_filter(Cbessel, Lbessel, cut_off)
			
		elif (filter_name == 'Butterworth'):
			BW = Filter_design('Butterworth')
			Cbutter, Lbutter = BW.CapInductButter(order)
			parts = BW.lowpass_filter(Cbutter, Lbutter, cut_off)
		elif (filter_name == 'Chebyshev'):
			CH = Filter_design('Chebyshev')
			Ccheb, Lcheb = BW.CapInductCheb(order)
			parts = CH.lowpass_filter(Ccheb, Lcheb, cut_off)
				
	elif (fitler_response == 'Highpass'):
		#implement high pass filter
		pass
		
		
	return render_template("filteroutput.html", filter_name = filter_name)	


if __name__ == "__main__":
	app.run(debug=True)
