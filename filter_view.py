from flask import Flask, request, render_template, make_response
from filter_design import Filter_design
from responsecurve import Responsecurve
import urllib
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
	minf = int(request.form['minf'])
	maxf = int(request.form['maxf'])
	runits = request.form['runits']
	if (runits == 'MHz'):
		minf *= 1e6
		maxf *= 1e6
	elif (runits == 'Khz'):
		minf *= 1e6
		maxf *= 1e6
		
	F = Responsecurve(parts, filter_name, minf, maxf)	
	fig = F.plot_schematic()
	image_out = get_image(fig)
	
	return render_template("filteroutput.html", filter_name = filter_name, parts = parts, img_data=urllib.quote(image_out.rstrip('\n')) )	
	

def get_image(fig):
	""""""
	
	import StringIO
	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas	
	
	canvas = FigureCanvas(fig)
	png_output = StringIO.StringIO()
	canvas.print_png(png_output)
	return png_output.getvalue().encode("base64")
	
	
if __name__ == "__main__":
	app.run(debug=True)
