INSTRUCTIONS

Note: You need to have Python pre-installed to run this application!

1. Run PyCharm IDE as administrator and go to File > Open and select this project named <name>.

   A virtual environment is already created for you using the command python -m venv .venv.

2. Open the terminal and activate the virtual environment using the command: 

   .venv\Scripts\activate
           
3. Install the required dependencies: 

   pip install flask
                                          
   pip install flask-sqlalchemy
                                                                                                        
   Note that, alternatively, you might need to add python -m before each command.
   
4. To output dependencies in a file for easier access, run:

   pip freeze > requirements.txt

5. The database table is already set up and currently holds the data of one object (to lookup, run in terminal: python and then DeliveryFee.query.all()). If you want
to add more objects in the table, run the commands:

   db.session.add(DeliveryFee(cart_value: 800, delivery_distance: 1560, number_of_items: 6, time: "2022-30-01T14:00:00Z")

   db.session.commit()

6. To run the application, create the environment variables:

   set FLASK_APP=delivery_fee.py

   set FLASK_ENV=development

   flask run
    
   In macOS, replace set with export. To exit the python interactive mode, run exit().
   
At this point, you should be able to access from your terminal 127.0.0.1:5000/request and 127.0.0.1:5000/response/1, or with the
corresponding id of the object/delivery for which you want to calculate the delivery fee.