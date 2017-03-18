from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
	
	return render_template("home.html")
	
@app.route("/filteroutput", methods=["POST"])
def filter_design():
	result = request.form['filter']
			
	return render_template("filteroutput.html", filter_name = result)	


if __name__ == "__main__":
	app.run(debug=True)
