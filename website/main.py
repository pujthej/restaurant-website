from flask import Flask,render_template,request,session
from flask_session import Session
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "hotel"

@app.route('/',methods=['GET','POST'])
def index():

    return render_template('index.html')


@app.route('/about',methods=['GET','POST'])
def about():

    return render_template('about.html')


@app.route('/menu',methods=['GET','POST'])
def menu():
    cur = mysql.connection.cursor()

    menu_items = cur.execute("SELECT * FROM menu")


    userDetails = cur.fetchall()

    return render_template('menu2.html',userDetails=userDetails)




@app.route('/reservation',methods=['GET','POST'])
def reserve():
    if request.method == 'GET':
        return render_template("booking.html")

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        size = request.form['size']
        date = request.form['date']
        time = request.form['time']
        location = request.form['location']

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO reservation(name,contact,table_size,date,time,location) VALUES (%s,%s,%s,%s,%s,%s)",(name,contact,size,date,time,location))

        mysql.connection.commit()

        cur.close()

        session['name'] = name
        session['contact'] = contact
        session['size'] = size
        session['date'] = date
        session['time'] = time
        session['location'] = location

        return render_template("confirm.html")
    
    return render_template("booking.html")

@app.route('/display',methods=['GET','POST'])
def display():
    cur = mysql.connection.cursor()

    yep = cur.execute("SELECT * FROM reservation")


    userDetails = cur.fetchall()

    

    return render_template('display.html',userDetails=userDetails)



@app.route('/gallery',methods=['GET','POST'])
def gallery():

    return render_template('gallery.html')


@app.route('/contactus',methods=['GET','POST'])
def contact():

    return render_template('contact.html')


@app.route('/addtocart/<string:item_name>',methods=['GET','POST'])
def addtocart(item_name):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM menu WHERE name = %s" , [item_name])
    data=cur.fetchone()
    price = data[1]
    cur.execute("INSERT INTO cart(name,price) VALUES (%s,%s)",(item_name,price))
    mysql.connection.commit()
    
    cur.execute("SELECT * FROM cart")
    data = cur.fetchall()

    return render_template("cart.html",data=data)

@app.route('/delete/<string:food_name>',methods=["GET"])
def delete(food_name):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cart WHERE name=%s' ,[food_name])
    mysql.connection.commit()
    cur.execute("SELECT * FROM cart WHERE name NOT LIKE 'A%'")
    data = cur.fetchall()
    return render_template('cart.html',data=data)


@app.route('/placeorder',methods=['GET','POST'])
def placeorder():

    return render_template('placeorder.html')

    
    
    



if __name__ == "__main__":
    app.run(debug=True)        