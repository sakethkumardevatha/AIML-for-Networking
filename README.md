🛡️ SQL Injection Detection App

This project uses **Machine Learning + Rule-Based Detection** to identify potential SQL Injection (SQLi) attacks in queries

 Features
- Accepts single or batch SQL queries / URLs

- Uses a trained ML model with TF-IDF + Logistic Regression
  
- Applies rule-based detection for common SQLi patterns
  
- Built using **Streamlit** for interactive UI


📁 Project Structure
AIML-for-Networking/
├── app.py # Streamlit frontend app
├── train.py # Model training script
├── model/
│ └── sqli_detector.pkl # Trained model file
├── SQLiV3_cleaned.csv # Cleaned & balanced dataset
├── dataset.csv # Raw or working dataset
├── requirements.txt # Python dependencies
└── .gitignore


---
Setup Instructions
1. Clone the Repository

git clone https://github.com/sakethkumardevatha/AIML-for-Networking.git  

cd AIML-for-Networking

2. Create and Activate Virtual Environment (recommended)

python3 -m venv venv

source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install Dependencies
   
pip install -r requirements.txt

4. (Re)Train the Model
   
python train.py

5.Run the app 

streamlit run app.py

Now, give some sample input to test
-- Malicious:

SELECT * FROM users WHERE id = 1 OR 1=1;

' OR '1'='1

admin' -- 

1; DROP TABLE users

-- Safe:
SELECT * FROM users WHERE id = 1;

SELECT name FROM customers WHERE age > 30;

UPDATE orders SET status = 'shipped' WHERE id = 10;

OUTPUT:

the output will be like this if user entered any queries to test 
![image](https://github.com/user-attachments/assets/cecdf1f2-7684-457e-ba7c-64660997b9cb)

Dataset Info

cleaned datasets used for training:SQLiV3_cleaned.csv
The original dataset has been taken from this repo "https://github.com/nidnogg/sqliv5-dataset" and its name is SQLiV3.csv
It consists of various patterns of sql injection attacks which is useful for the model to train,but it has some unequality in its data so we cleaned it up. 
SO, after cleaninhg the dataset is balanced 50/50 between safe and malicious queries

Built With
Python
Scikit-learn
Pandas
Streamlit
