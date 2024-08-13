from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
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

@app.route('/configurar_umbrales')
def configurar_umbrales():
    return render_template('configurar_umbrales.html')

@app.route('/solicitud_reabastecimiento')
def solicitud_reabastecimiento():
    return render_template('solicitud_reabastecimiento.html')

@app.route('/alertas_nivel_bajo')
def alertas_nivel_bajo():
    return render_template('alertas_nivel_bajo.html')

@app.route('/registro_entregas')
def registro_entregas():
    return render_template('registro_entregas.html')

@app.route('/incidencias')
def incidencias():
    return render_template('incidencias.html')

@app.route('/')
def autenticacion():
    return render_template('autenticacion.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/tienda')
def tienda():
    return render_template('tienda.html')

# Ruta para procesar la venta
@app.route('/process_sale')
def process_sale():
    return render_template('ventas')

# Ruta para generar reportes
@app.route('/generate_report')
def generate_report():
    return render_template('ventas')

# Ruta para configurar promociones
@app.route('/configure_promotion')
def configure_promotion():
    return render_template('ventas')

# Ruta para configurar métodos de pago
@app.route('/configure_payment_method')
def configure_payment_method():
    return render_template('ventas')

@app.route('/pre_ventas')
def pre_ventas():
    return render_template('pre_ventas.html')

@app.route('/cashier_functions')
def cashier_functions():
    return render_template('cashier_functions.html')

@app.route('/admin_functions')
def admin_functions():
    return render_template('admin_functions.html')

@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/technical_functions')
def technical_functions():
    return render_template('technical_functions.html')

@app.route('/admin_functions_maintenance')
def admin_functions_maintenance():
    return render_template('admin_functions_maintenance.html')

@app.route('/configure_parameters')
def configure_parameters():
    return render_template('technical_functions')

@app.route('/generate_maintenance_report')
def generate_maintenance_report():
    return render_template('admin_functions_maintenance')

@app.route('/train_system')
def train_system():
    return render_template('admin_functions_maintenance')

@app.route('/emisiones')
def emisiones():
    return render_template('emisiones.html')

@app.route('/configurar_alertas')
def configurar_alertas():
    return render_template('configurar_alertas.html')

if __name__ == '__main__':
    app.run(debug=True)
