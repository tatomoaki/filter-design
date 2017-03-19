from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
	
	return render_template("home.html")
	
@app.route("/filteroutput", methods=["POST"])
def filter_design():
	
	filter_name = request.form['filter']
	order = request.form['order']
	filter_type = request.form['cutoff']
	funits = request.form['funits']
	filter_response = request.form['FilterResponse']
			
	return render_template("filteroutput.html", filter_name = filter_name)	


if __name__ == "__main__":
	app.run(debug=True)
