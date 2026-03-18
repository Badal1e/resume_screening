import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="resume_db"
    )



# import pymysql

# conn = pymysql.connect(
#     host="localhost",
#     user="root",
#     password="root123",
#     database="resume_db"
# )

# print("Connected!")