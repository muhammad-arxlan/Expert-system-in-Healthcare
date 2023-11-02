import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import io
from PIL import Image
import webbrowser
import mysql.connector
from passlib.hash import pbkdf2_sha256

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="arslan",
    password="arslan123",
    database="project"
)
cursor = db.cursor()

def create_admin_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS admin (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255))")
    db.commit()

def admin_login(username, password):
    cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
    admin = cursor.fetchone()
    if admin:
        return True
    return False

# Create the users table
def create_users_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), email VARCHAR(255))")
    db.commit()

# Check if the user exists in the database
def user_login(username, password):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    users = cursor.fetchone()
    if users and pbkdf2_sha256.verify(password, users[3]):
        return True
    return False

def user_registration(username, password, email):
    if username == "arslan":
        return False
    else:
        hashed_password = pbkdf2_sha256.hash(password)
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
            db.commit()
            return True
        except mysql.connector.IntegrityError:
            return False
    
def logout():
    # Reset session state variables
    st.session_state.logged_in = False
    st.session_state.is_admin = False    
    
# Function to retrieve and display registered user information
def show_registered_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    if users:
        st.subheader("Registered Users")
        
        # Define column names
        column_names = ["User ID", "Email", "UserName", "Password"]
        
        table_data = []
        table_data.append(column_names)  # Add column names to the table
        
        for user in users:
            table_data.append([user[0], user[1], user[2], user[3]])
        
        # Generate HTML table code
        table_html = "<table>"
        for row in table_data:
            table_html += "<tr>"
            for cell in row:
                table_html += "<td>{}</td>".format(cell)
            table_html += "</tr>"
        table_html += "</table>"
        
        # Apply CSS styles to the table
        css = """
        <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """
        
        # Render the table with CSS
        st.write(css, unsafe_allow_html=True)
        st.write(table_html, unsafe_allow_html=True)
            
    else:
        st.warning("No registered users found.")


  #Initialize logged_in and is_admin attributes in session_state
 #=============================================================================
if "logged_in" not in st.session_state:
     st.session_state.logged_in = False
 
if "is_admin" not in st.session_state:
     st.session_state.is_admin = False
 
 ##Check if logged_in is False and display login/register form
if not st.session_state.logged_in:
     st.title("Login or Register to access the Expert System")
 
     # Tggle button for login/register
     option = st.radio("Select an option:", ("Login", "Register"), key="login_register_toggle", index=1)
 
     if option == "Login":
         with st.form("login_form"):
             st.write("<div align='center'><h1><b>Login</b></h1></div>", unsafe_allow_html=True)
 
             username = st.text_input("Username")
             password = st.text_input("Password", type="password")
             submit_button = st.form_submit_button("Login")
 
             if submit_button:
                 if username == "arslan" and admin_login(username, password):
                     # Set admin logged_in state to True
                     st.session_state.logged_in = True
                     st.session_state.is_admin = True
                     st.success("Logged in successfully as admin")
                     
                     # Open new page to display registered user information
                     new_page_url = "http://localhost:8501/admin_registered_users"
                     script = f"""
                     <script>
                     window.open("{new_page_url}");
                     </script>
                     """
                     st.markdown(script, unsafe_allow_html=True)
                     
                 elif user_login(username, password):
                     # Set logged_in state to True
                     st.session_state.logged_in = True
                     st.session_state.is_admin = False
                     st.success("Logged in successfully as user")
                     
                 else:
                     st.error("Invalid username or password")
 
     elif option == "Register":
         with st.form("register_form"):
             st.write("<div align='center'><h1><b>Register</b></h1></div>", unsafe_allow_html=True)
 
             username = st.text_input("Username")
             password = st.text_input("Password", type="password")
             email = st.text_input("Email")
             submit_button = st.form_submit_button("Register")
 
             if submit_button:
                 if user_registration(username, password, email):
                     st.success("Registration successful. Please login.")
                 else:
                     st.error("Username already exists. Please choose a different username.")
# 
# =============================================================================
# =============================================================================
# =============================================================================
                

# loading the saved models

diabetes_model = pickle.load(open('C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/saved models/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/saved models/heart_disease_model.sav','rb'))

# =============================================================================
# parkinsons_model = pickle.load(open('C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/saved models/parkinsons_model.sav', 'rb'))
# =============================================================================




# Read the image file and convert it to bytes
with open('C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/IMG_1163.jpg', 'rb') as f:
              image_bytes = io.BytesIO(f.read())
with open('C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/IMG_1164.jpg', 'rb') as f:
              image_bytes1 = io.BytesIO(f.read())
with open('C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/IMG_1165.jpg', 'rb') as f:
              image_bytes2 = io.BytesIO(f.read())
              
doctors = {
    'Prof. Dr. Taj Jamshaid': {
        'Specialization': 'Consultant Physician Diabetologist & Hepatologist',
        'Email': 'drjamshaid@gmail.com',
        'Available Timings': ['Monday: 10am-1pm', 'Wednesday: 3pm-6pm'],
         'Image': image_bytes
        
    },
    'Assoc. Prof. Dr. Naresh Khurana': {
        'Specialization': 'Interventional Cardiologist  MBBS, FCPS, MCPS',
        'Email': 'ProfNaresh@gmail.com',
        'Available Timings': ['Tuesday: 2pm-5pm', 'Thursday: 10am-1pm'],
        'Image': image_bytes1
    },
    'Dr. Bashir Ahmed Khan': {
        'Specialization': 'PMC Verified  MBBS,MS, FCPS (Neuro Surgery)',
        'Email': 'khanBashir@gmail.com',
        'Available Timings': ['Tuesday: 2pm-5pm', 'Thursday: 10am-1pm'],
        'Image': image_bytes2
    },
    
}          

# =============================================================================
# =============================================================================
# =============================================================================
selected = None
if st.session_state.is_admin:
# =============================================================================
#   =============================================================================
# =============================================================================
#  =============================================================================
#   
#  =============================================================================
#   sidebar for navigation
 with st.sidebar:
      
          selected = option_menu('Expert System in Healthcare',
                                 ['Users','Home',
                                  'Diabetes Prediction',
                                  'Heart Disease Prediction',
                                  'Doctors Detail',
                                  'Developed By',
                                  
                                  'logout'],
                                 icons=['house-fill','', 'activity', 'heart', 'person', 'info','code-slash', 'power'],
                                 default_index=0)
          
 
 
elif st.session_state.logged_in:
 # =============================================================================
 # =============================================================================
 #    =============================================================================
 # sidebar for navigation
 with st.sidebar:      
          selected = option_menu('Expert System in Healthcare',
                                 ['Home',
                                  'Diabetes Prediction',
                                  'Heart Disease Prediction',
                                  'Doctors Detail',
                                  'Developed By', 
                                  'Logout'],
                                 icons=['house-fill','', 'activity', 'heart', 'person', 'info','code-slash', 'power'],
                                default_index=0)
 
# # Display additional menu options for admin
# 
if st.session_state.is_admin:
     if selected == "Users":
        show_registered_users()
# =============================================================================
  
if selected == "Home":
    st.title("Expert System in Health Care")
    img = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/intro.jpg")
    st.image(img,width=700, caption="Health Care", use_column_width=True)

    # Add your project statement or description here
    st.write("The healthcare expert system is a web-based application designed to assist users in predicting and managing various diseases. The application provides a user-friendly interface where users can log in or register to access the system's features.")
    st.write("Upon logging in or registering, users are presented with a home page that serves as the main hub for navigation. From the home page, users can choose different options such as disease prediction, diabetes prediction, heart disease prediction, Parkinson's disease prediction, doctor's details, and more.")
    st.write("The disease prediction feature allows users to select a specific disease they want to predict. By providing relevant input data, such as medical parameters, the system utilizes machine learning models to generate predictions for the selected disease.")
    st.write("For diabetes prediction, users are prompted to input medical information such as the number of pregnancies, glucose level, blood pressure, insulin level, BMI, and more. The system then predicts whether the user is diabetic or not based on the provided data.")
    st.write("Similarly, for heart disease prediction, users are required to input parameters such as age, sex, chest pain types, blood pressure, cholesterol level, and other relevant information. The system employs machine learning models to predict the presence or absence of heart disease based on the given data.")
    st.write("In the case of Parkinson's disease prediction, users need to input specific voice-related parameters. The system uses machine learning techniques to analyze the input and generate predictions regarding the presence or absence of Parkinson's disease.")
    st.write("Additionally, the application provides information about doctors specializing in different fields, including their contact details, available timings, and images. Users can access this information to seek appropriate medical assistance.")
    st.write("The project aims to assist users in gaining insights into their health conditions and making informed decisions. By utilizing machine learning models and providing user-friendly interfaces, the healthcare expert system offers a convenient platform for disease prediction and management.")

    

            
# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    img = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/diabetes.jpg")
    
    # page title
    st.title('Diabetes Prediction using ML')
    st.image(img, width=600)

    
    # page title
    st.title('Diabetes Prediction using ML')
    
    
    # getting the input data from the user
    col1, col2, col3 = st.columns(3)
    
    with col1:
        
        Pregnancies = st.text_input('Number of Pregnancies(Enter the number of pregnancies)')
        
        
    with col2:
        Glucose = st.text_input('Glucose Level(0 -> 199)')
    
    with col3:
        BloodPressure = st.text_input('Blood Pressure value(80 -> 300)')
    
    with col1:
        SkinThickness = st.text_input('Skin Thickness value(1 -> 99)')
    
    with col2:
        Insulin = st.text_input('Insulin Level(10 -> 846)')
    
    with col3:
        BMI = st.text_input('BMI value(1.0 -> 67.1)')
    
    with col1:
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value(0.078 -> 2.42)')
    
    with col2:
        Age = st.text_input('Age of the Person')
    
    
    # code for Prediction
    diab_diagnosis = ''
    
    # creating a button for Prediction
    
    if st.button('Diabetes Test Result'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        
        if (diab_prediction[0] == 1):
          diab_diagnosis = 'The person is diabetic'
        else:
          diab_diagnosis = 'The person is not diabetic'
        
    st.success(diab_diagnosis)




# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):
    
    # page title
    img = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/heart.jpg")
    
    # page title
    st.title('Heart Disease Prediction using ML')
    st.image(img, width=600)
    
    # page title
    st.title('Heart Disease Prediction using ML')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age = st.text_input('Age')
        
    with col2:
        sex = st.text_input('Sex , male =1 , female=0')
        
    with col3:
        cp = st.text_input('Chest Pain(0 -> 3)')
        
    with col1:
        trestbps = st.text_input('Resting Blood Pressure(94 -> 200)')
        
    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl(126 -> 564)')
        
    with col3:
        fbs = st.text_input('Fasting Blood Sugar, yes =1 , no =0')
        
    with col1:
        restecg = st.text_input('Resting Electrocardiographic results (0 -> 2)')
        
    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved(71 -> 202)')
        
    with col3:
        exang = st.text_input('Exercise Induced Angina(0 -> 1)')
        
    with col1:
        oldpeak = st.text_input('ST depression induced by exercise(1.0 -> 6.2)')
        
    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment(0 -> 2)')
        
    with col3:
        ca = st.text_input('Major vessels colored by flourosopy(0 -> 4)')
        
    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')
        
        
     
     
    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction
    if st.button('Heart Disease Test Result'):
        # Convert input values to numeric format
        age = int(age)
        sex = int(sex)
        cp = int(cp)
        trestbps = int(trestbps)
        chol = int(chol)
        fbs = int(fbs)
        restecg = int(restecg)
        thalach = int(thalach)
        exang = int(exang)
        oldpeak = float(oldpeak)
        slope = int(slope)
        ca = int(ca)
        thal = int(thal)
        
        # Make predictions
        heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'
        
    st.success(heart_diagnosis)
        
    
    

# Parkinson's Prediction Page
# =============================================================================
#if (selected == "Parkinsons Prediction"):
#     
#     img = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/parkinsons.jpg")
#   
#   # page title
#     st.title("Parkinson's Disease Prediction using ML")
#     st.image(img, width=600)
#     
#     
#     
#     # page title
#    
#     
#     col1, col2, col3, col4, col5 = st.columns(5)  
#     
#     with col1:
#         fo = st.text_input('MDVP:Fo(Hz)')
#         
#     with col2:
#         fhi = st.text_input('MDVP:Fhi(Hz)')
#         
#     with col3:
#         flo = st.text_input('MDVP:Flo(Hz)')
#         
#     with col4:
#         Jitter_percent = st.text_input('MDVP:Jitter(%)')
#         
#     with col5:
#         Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')
#         
#     with col1:
#         RAP = st.text_input('MDVP:RAP')
#         
#     with col2:
#         PPQ = st.text_input('MDVP:PPQ')
#         
#     with col3:
#         DDP = st.text_input('Jitter:DDP')
#         
#     with col4:
#         Shimmer = st.text_input('MDVP:Shimmer')
#         
#     with col5:
#         Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')
#         
#     with col1:
#         APQ3 = st.text_input('Shimmer:APQ3')
#         
#     with col2:
#         APQ5 = st.text_input('Shimmer:APQ5')
#         
#     with col3:
#         APQ = st.text_input('MDVP:APQ')
#         
#     with col4:
#         DDA = st.text_input('Shimmer:DDA')
#         
#     with col5:
#         NHR = st.text_input('NHR')
#         
#     with col1:
#         HNR = st.text_input('HNR')
#         
#     with col2:
#         RPDE = st.text_input('RPDE')
#         
#     with col3:
#         DFA = st.text_input('DFA')
#         
#     with col4:
#         spread1 = st.text_input('spread1')
#         
#     with col5:
#         spread2 = st.text_input('spread2')
#         
#     with col1:
#         D2 = st.text_input('D2')
#         
#     with col2:
#         PPE = st.text_input('PPE')
#         
#     
#     
#     # code for Prediction
#     parkinsons_diagnosis = ''
#     
#     # creating a button for Prediction    
#     if st.button("Parkinson's Test Result"):
#         parkinsons_prediction = parkinsons_model.predict([[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ,DDP,Shimmer,Shimmer_dB,APQ3,APQ5,APQ,DDA,NHR,HNR,RPDE,DFA,spread1,spread2,D2,PPE]])                          
#         
#         if (parkinsons_prediction[0] == 1):
#           parkinsons_diagnosis = "The person has Parkinson's disease"
#         else:
#           parkinsons_diagnosis = "The person does not have Parkinson's disease"
#         
#     st.success(parkinsons_diagnosis)
# =============================================================================
    
    
    
if selected == 'Doctors Detail':
        st.write('Select a Doctor:')
        selected_doctor = st.selectbox('', list(doctors.keys()))

        # Display the selected doctor's details
        st.write(f"**Specialization:** {doctors[selected_doctor]['Specialization']}")
        st.write(f"**Email:** {doctors[selected_doctor]['Email']}")
        st.write('**Available Timings:**')
        
        for timing in doctors[selected_doctor]['Available Timings']:
            st.write(f"- {timing}")
        
        # Display the doctor's image
        st.image(doctors[selected_doctor]['Image'], width=250, use_column_width=False)

        # Add a button to book the appointment
        if st.button('Book Appointment'):
            # Send an email to the selected doctor
            mailto_url = f"mailto:{doctors[selected_doctor]['Email']}"
            webbrowser.open_new_tab(mailto_url)
            
if selected == 'Developed By':
    st.title("Developed By")
    
    img = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/arslan.jpg")
    img1 = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/saqib.jpg")
    img2 = Image.open("C:/Users/BABAR KHAN/Desktop/Multiple Disease Prediction System/umer.jpg")
    
    # Person 1 details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(img, width=250, use_column_width=False)
        st.markdown("<style>div.stImage > img { padding: 10px; }</style>", unsafe_allow_html=True)
        st.write("Name: M.Arslan")
        st.write("Role: Data Scientist")
        st.write("Email: m.arsalan@gmail.com")
    
    # Person 2 details
    with col2:
        st.image(img1, width=250, use_column_width=False)
        st.markdown("<style>div.stImage > img { padding: 10px; }</style>", unsafe_allow_html=True)
        st.write("Name: M.Saqib")
        st.write("Role: Software Engineer")
        st.write("Email: saqib@gmail.com")
    
    # Person 3 details
    with col3:
        st.image(img2, width=250, use_column_width=False)
        st.markdown("<style>div.stImage > img { padding: 10px; }</style>", unsafe_allow_html=True)
        st.write("Name: Umer Malik")
        st.write("Role: UI/UX Designer")
        st.write("Email: umer@gmail.com")
        
if selected == 'Logout':
    st.session_state.logged_in = False
    st.experimental_rerun()
    
if selected == 'logout':
    logout()
