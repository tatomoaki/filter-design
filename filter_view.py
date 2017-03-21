from flask import Flask, request, render_template
from filter_design import Filter_design
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
	
	if (filter_name == 'Bessel'):	
		B = Filter_design('Bessel')
		
		Cbessel, Lbessel = B.CapInductBess(order)
		B.lowpass_filter(Cbessel, Lbessel, cut_off)
			
	return render_template("filteroutput.html", filter_name = filter_name)	


if __name__ == "__main__":
	app.run(debug=True)
