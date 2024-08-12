from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reabastecimiento')
def reabastecimiento():
    return render_template('reabastecimiento.html')

@app.route('/autenticacion')
def autentificacion():
    return render_template('autentificacion.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/tienda')
def tienda():
    return render_template('tienda.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/emisiones')
def emisiones():
    return render_template('emisiones.html')

if __name__ == '__main__':
    app.run(debug=True)
