from flask import Flask, render_template, request, redirect
import pyodbc

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/tabla')
def tabla():
    # Establecer la conexión a SQL Server
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=casa;DATABASE=Sistema;UID=sa;PWD=Password1234'
    cnxn = pyodbc.connect(connection_string)

    # Ejecutar una consulta SQL
    cursor = cnxn.cursor()
    cursor.execute('SELECT top(5) * FROM Productos')
    results = cursor.fetchall()

    # Cerrar la conexión
    cnxn.close()

    return render_template('tabla.html', data=results)

@app.route('/insert', methods=['POST'])
def insert():
    # Obtener los datos del formulario
    codigo = request.form['Codigo']
    nombre = request.form['Nombre']
    menu = request.form['Ubic']

    # Establecer la conexión a SQL Server
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=casa;DATABASE=Sistema;UID=sa;PWD=Password1234'
    cnxn = pyodbc.connect(connection_string)

    # Ejecutar la consulta SQL para insertar los datos
    cursor = cnxn.cursor()
    cursor.execute("INSERT INTO Roles (codigo, nombre, menu) VALUES (?, ?, ?)", (codigo, nombre, menu))
    cnxn.commit()

    # Cerrar la conexión
    cnxn.close()

    # Redirigir a la página de la tabla
    return redirect('/tabla')

@app.route('/modificar', methods=['POST'])
def modificar():
    # Obtener los datos del formulario de modificación
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    menu = request.form['menu']

    # Establecer la conexión a SQL Server
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=SERVIDOR\SQLEXPRESS;DATABASE=Sistema;UID=sa;PWD=Password1234'
    cnxn = pyodbc.connect(connection_string)

    try:
        # Ejecutar la consulta SQL para actualizar los datos
        cursor = cnxn.cursor()
        cursor.execute("UPDATE Roles SET nombre = ?, menu = ? WHERE codigo = ?", (nombre, menu, codigo))
        cnxn.commit()

        # Redirigir a la página de la tabla
        return redirect('/tabla')

    except pyodbc.Error as e:
        # Ocurrió un error durante la actualización
        error_message = str(e)
        # Manejar el error según tus necesidades (mostrar mensaje de error, redirigir

if __name__ == '__main__':
    app.run(debug=True)
