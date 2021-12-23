from flask import Flask, render_template, url_for, request, redirect
import csv
import os
# from flask_mail import Mail
app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('./index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_csv(data):
    with open('database.csv', mode='a') as database:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database,  delimiter=',',  quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,subject,message])
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('./thankyou.html')
    else:
        return 'something went wrong'
if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))
     app.run(debug=True, port=port)
