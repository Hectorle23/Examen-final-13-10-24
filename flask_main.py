from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/alumnos')
def show_alumnos():
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM alumnos')
    alumnos = cur.fetchall()
    conn.close()
    return render_template('aula/alumnos.html', alumnos=alumnos)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        aprobado = 'aprobado' in request.form 
        nota = float(request.form['nota'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')

        conn = sqlite3.connect('alumnos.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO alumnos (nombre, apellido, aprobado, nota, fecha) VALUES (?, ?, ?, ?, ?)',
                    (nombre, apellido, aprobado, nota, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for('show_alumnos'))
    return render_template('aula/agregar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        aprobado = 'aprobado' in request.form
        nota = float(request.form['nota'])
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')

        cur.execute('UPDATE alumnos SET nombre = ?, apellido = ?, aprobado = ?, nota = ?, fecha = ? WHERE id = ?',
                    (nombre, apellido, aprobado, nota, fecha, id))
        conn.commit()
        conn.close()
        return redirect(url_for('show_alumnos'))

    cur.execute('SELECT * FROM alumnos WHERE id = ?', (id,))
    alumno = cur.fetchone()
    conn.close()
    return render_template('aula/editar.html', alumno=alumno)


@app.route('/alumnos/eliminar/<int:id>', methods=['POST'])
def eliminar_alumno(id):
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM alumnos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('show_alumnos'))

if __name__ == '__main__':
    app.run(debug=True)
