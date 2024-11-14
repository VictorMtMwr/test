from flask import Flask, request, render_template, redirect,url_for
from auth_db import register_user, validate_user
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')

        # Validación básica para evitar que los campos estén vacíos
        if not name or not email or not password or not phone_number:
            error_message = "Todos los campos son obligatorios."
            return render_template('register.html', error=error_message)
        
        try:
            register_user(name, email, password, phone_number)  # Guardar el nuevo usuario en la base de datos
            print("Registro completado, redirigiendo al login...")
            return redirect(url_for('login'))  # Redirigir al login después del registro
        except Exception as e:
            print("Error al registrar el usuario:", e)
            return "Error al registrar el usuario", 500  # Enviar mensaje de error si falla

    return render_template('register.html')

# Ruta para iniciar sesión (validar usuario)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        if validate_user(name, password):
            print('ok...')
            return redirect(url_for('index'))  # Redirigir al index si el login es exitoso
        else:
            error_message = "Credenciales incorrectas. Intenta nuevamente."
            return render_template('login.html', error=error_message)  # Mostrar mensaje de error

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug=True)
