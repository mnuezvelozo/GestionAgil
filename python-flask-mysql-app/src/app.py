from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM productos")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObject)

#Ruta para guardar usuarios en la bdd
@app.route('/productos', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    valor = request.form['valor']
    cantidad = request.form['cantidad']
    ubicacion = request.form['ubicacion']

    if nombre and descripcion and valor and cantidad and ubicacion:
        cursor = db.database.cursor()
        sql = "INSERT INTO productos (nombre, descripcion, valor, cantidad, ubicacion) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre, descripcion, valor, cantidad, ubicacion)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM productos WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    valor = request.form['valor']
    cantidad = request.form['cantidad']
    ubicacion = request.form['ubicacion']

    if nombre and descripcion and valor and cantidad and ubicacion:
        cursor = db.database.cursor()
        sql = "UPDATE productos SET nombre = %s, descripcion = %s, valor = %s, cantidad = %s, ubicacion = %s WHERE id = %s"
        data = (nombre, descripcion, valor, cantidad, ubicacion ,id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)