import mysql.connector
import bcrypt

# Conexión a la base de datos MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="weatherwhisper",
            user="root",
            password="victormt26.2024"
        )
        return connection
    except mysql.connector.Error as e:
        print("Error al conectarse a la base de datos:", e)
        return None

# Registro de usuario en la base de datos
def register_user(name, email, password, phone_number):
    conn = get_db_connection()
    if conn is None:
        return False  # Si no hay conexión, regresar False

    cursor = conn.cursor()
    #hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, phone_number) VALUES (%s, %s, %s, %s)", 
            (name, email, password, phone_number)
        )
        conn.commit()
        return True  # Registro exitoso
    except mysql.connector.Error as e:
        print("Error al registrar el usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# Validación de usuario al iniciar sesión
def validate_user(name, password):
    conn = get_db_connection()
    if conn is None:
        return False  # Si no hay conexión, regresar False

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE name = %s", (name,))
        user = cursor.fetchone()
        
        if user and password:
            return True
        return False
    except mysql.connector.Error as e:
        print("Error al validar el usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()
