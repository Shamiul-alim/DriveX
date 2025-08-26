from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import os
from urllib.parse import urlparse
from flask import jsonify, request

app = Flask(__name__)
# Secret key from env (fallback to "dev-secret" if not set)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret')

# Database config: use Railway env var, fallback to local SQLite for testing
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///local.db'  # fallback if env var is not set
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    license = db.Column(db.String(50), nullable=True)
    nid = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    nid = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    nid = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)  
    carVIN_No = db.Column(db.String(100), nullable=False, unique=True) 
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)  
    capacity = db.Column(db.Integer, nullable=False) 
    color = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(255), nullable=True)  
    image_url = db.Column(db.String(255), nullable=True)  
    plate_num = db.Column(db.String(50), nullable=False) 
    price = db.Column(db.Float, nullable=True)  
    pickup_point_id = db.Column(db.Integer, db.ForeignKey('pickup_points.id'), nullable=False)  

    def __repr__(self):
        return f"<Car {self.carVIN_No} - {self.model}>"

class PickupPoint(db.Model):
    __tablename__ = 'pickup_points'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    cars = db.relationship('Car', backref='pickup_point', lazy=True)

    def __repr__(self):
        return f"<PickupPoint {self.name}>"


app.app_context().push()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        nid = request.form['nid']
        password = generate_password_hash(request.form['password'])

        role = request.form['registration_type']
        if role == 'user':
            license = request.form['license']
            new_user = User(name=name, email=email, license=license, nid=nid, password=password)
            db.session.add(new_user)
        elif role == 'employee':
            employee_id = request.form['employee_id']
            position = request.form['e_position']
            new_employee = Employee(name=name,email=email, employee_id=employee_id, position=position, nid=nid, password=password)
            db.session.add(new_employee)
        elif role == 'admin':
            admin_id = request.form['admin_id']
            position = request.form['a_position']
            new_admin = Admin(name=name,email=email, admin_id=admin_id, position=position, nid=nid, password=password)
            db.session.add(new_admin)
        
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if role == 'user':
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['username'] = user.name
                flash('Login successful!', 'success')
                return redirect(url_for('user_dashboard'))
    
        elif role == 'employee':
            employee = Employee.query.filter_by(email=email).first()  
            if employee and check_password_hash(employee.password, password):
                flash('Login successful!', 'success')
                return redirect(url_for('employee_dashboard'))
    
        elif role == 'admin':
            admin = Admin.query.filter_by(email=email).first()  
            if admin and check_password_hash(admin.password, password):
                flash('Login successful!', 'success')
                return redirect(url_for('home'))

        flash('Invalid credentials or role mismatch. Please try again.', 'danger')
        return redirect(url_for('login'))        
        
    return render_template('login.html')

# Route Page
@app.route('/route', methods=['GET'])
def route():
    username = session.get('username', 'Guest') 
    pickup = request.args.get('pickup', '')
    dropoff = request.args.get('dropoff', '')
    
    
    pickup_point_1 = PickupPoint.query.filter_by(id=1).first()
    pickup_point_2 = PickupPoint.query.filter_by(id=2).first()
    
    cars_point_1 = Car.query.filter_by(pickup_point_id=1).all()
    cars_point_2 = Car.query.filter_by(pickup_point_id=2).all()
    for car in cars_point_1 + cars_point_2:
        if not car.image_url:
            car.image_url = 'default.jpg'
 
    return render_template('route.html',  pickup=pickup, dropoff=dropoff, cars_point_1=cars_point_1,cars_point_2=cars_point_2 ,username=username)


#user_dashboar
@app.route('/user_dashboard')
def user_dashboard():
    username = session.get('username', 'Guest') 
    return render_template('user_dashboard.html', username=username)


@app.route('/employee_dashboard', methods=['GET', 'POST'])
def employee_dashboard():
    if request.method == 'POST':
        action = request.form.get('action')
        
        full_url = request.form.get('image_url', '')
        image_name = os.path.basename(urlparse(full_url).path)

        # Handle adding a car
        if action == 'add_car':
            try:
                new_car = Car(
                    carVIN_No=request.form['carVIN_No'],
                    name=request.form['name'],
                    model=request.form['model'],
                    capacity=int(request.form['capacity']),
                    color=request.form['color'],
                    description=request.form.get('description', ''),
                    image_url=f"{image_name}" if image_name else None,
                    plate_num=request.form['plate_num'],
                    price=float(request.form['price']),
                    pickup_point_id=int(request.form['pickup_point_id'])
                )
                db.session.add(new_car)
                db.session.commit()
                flash("Car added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Failed to add car: {str(e)}", "error")

        # Handle deleting a car
        elif action == 'delete_car':
            try:
                car_id = int(request.form['car_id'])
                car_to_delete = Car.query.get(car_id)
                if car_to_delete:
                    db.session.delete(car_to_delete)
                    db.session.commit()
                    flash("Car deleted successfully!", "success")
                else:
                    flash("Car not found.", "error")
            except Exception as e:
                db.session.rollback()
                flash(f"Failed to delete car: {str(e)}", "error")

    # Fetch all cars for the "View All Cars" section
    cars = Car.query.all()
    return render_template('employee_dashboard.html', cars=cars)


@app.route('/search_car', methods=['POST'])
def search_car():
    try:
        data = request.get_json()  # Get JSON data from the request
        query = data.get('query', '').strip()  # Retrieve search query

        if query:
            # Search the car database for matching names (case-insensitive)
            cars = Car.query.filter(Car.name.ilike(f"%{query}%")).all()
        else:
            cars = Car.query.all()  # Return all cars if no query is provided

        # Convert the car data into a list of dictionaries
        car_list = [
            {
                'id': car.id,
                'carVIN_No': car.carVIN_No,
                'name': car.name,
                'model': car.model,
                'capacity': car.capacity,
                'color': car.color,
                'pickup_point_id': car.pickup_point_id,
            }
            for car in cars
        ]

        return jsonify({'cars': car_list})

    except Exception as e:
        return jsonify({'error': str(e)}), 500





@app.route('/logout', methods=['POST'])
def logout():
    print("Logout route accessed")
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/select_car', methods=['POST'])
def select_car():
    # Get the car details from the form or request
    car_name = request.form.get('carName')  # Replace with actual form field name
    car_image = request.form.get('carImage')  # Replace with actual form field name

    # Store car details in session
    session['car_name'] = car_name
    session['car_image'] = car_image

    # Redirect to payment page
    return redirect(url_for('payment'))


@app.route('/payment')
def payment():
    # Retrieve car details from session
    image_url = "example_image.jpg" 
    car_name = session.get('car_name', 'Unknown Car')
    car_image = session.get('car_image', 'default.jpg')  # Default image if not found

    # Pass data to the template
    return render_template('payment.html', car_name=car_name, car_image=car_image, image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
