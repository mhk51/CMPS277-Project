# CMPS277-Project

## Step 1:
```diff
Unix: 
+ . venv/bin/activate
Windows: 
+ venv\Scripts\activate
```

## Step 2: 
```diff
+ pip install -r requirements.txt
```
## Step 3:
```diff
Create a python file in the root directory called db_config.py with the following contents:
+ DB_CONFIG = 'mysql+pymysql://{username}:{password}@{ip}:{port}/{schema}'
```

## Step 3: 
```diff
Run Python enviroment and type the following:
+ from app import db
+ db.create_all()
+ exit()
```
