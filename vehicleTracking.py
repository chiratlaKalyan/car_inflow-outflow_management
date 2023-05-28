from flask import Flask,render_template
from dbOperations import*

vehLogEntry = vehManagement()
app = Flask(__name__,template_folder='Templates', static_folder='assets')

table_headings= ("S.No","Car Licence Number","Entry Time","Exit Time","Status")
rows=vehLogEntry.select_all_tasks('vehicle_logging')
table_data=tuple(tuple(row) for row in rows)

@app.route("/")
def index():
    return render_template("index.html",headings=table_headings,data=table_data)

if __name__ == "__main__":
   app.run(debug=True)
