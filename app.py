from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc  # Librería para conectar a SQL Server
app = Flask(__name__)
app.secret_key = 'Hola'

def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\SQLEXPRESS;'  # Cambia esto si tu instancia tiene otro nombre
        'DATABASE=ServicentroCorazonDB;'
         'Trusted_Connection=yes;' 
    )
    return connection

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

@app.route('/autenticacion', methods=['GET', 'POST'])
def autenticacion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Conectar a la base de datos SQL Server
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar credenciales
        cursor.execute('SELECT * FROM Usuarios WHERE nombre_usuario = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):  # user[2] es la columna de contraseña
            flash('Inicio de sesión exitoso')
            return redirect(url_for('home'))  # Redirige al home o dashboard
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return redirect(url_for('autenticacion'))
    
    return render_template('autenticacion.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Conectar a la base de datos SQL Server
        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificar si el usuario ya existe
        cursor.execute('SELECT * FROM Usuarios WHERE nombre_usuario = ?', (username,))
        user = cursor.fetchone()

        if user:
            flash('El nombre de usuario ya está en uso')
            return redirect(url_for('register'))

        # Crear el hash de la contraseña
        hashed_password = generate_password_hash(password)

        # Insertar el nuevo usuario en la base de datos
        try:
            cursor.execute('''INSERT INTO Usuarios (nombre_usuario, contrasena, rol, estatus)
                              VALUES (?, ?, 'Cliente', 'Activo')''', (username, hashed_password))
            conn.commit()
            flash('Usuario registrado exitosamente')
            return redirect(url_for('autenticacion'))
        except Exception as e:
            flash(f'Error al registrar el usuario: {e}')
            return redirect(url_for('register'))
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

# EMP

@app.route('/EMP')
def EMP():
    return render_template('emp_index.html')

@app.route('/empleados/solicitar_vacaciones')
def solicitar_vacaciones():
    return render_template('solicitar_vacaciones.html')

@app.route('/empleados/ver_solicitudes')
def ver_solicitudes():
    return render_template('ver_solicitudes.html')

@app.route('/empleados/revisar_solicitud')
def revisar_solicitud():
    return render_template('revisar_solicitud.html')

@app.route('/empleados/crear_empleado')
def crear_empleado():
    return render_template('crear_empleado.html')

@app.route('/empleados/detalles_empleado')
def detalles_empleado():
    return render_template('detalles_empleado.html')

@app.route('/empleados/editar_empleado')
def editar_empleado():
    return render_template('editar_empleado.html')

@app.route('/empleados/calcular_nomina')
def calcular_nomina():
    return render_template('calcular_nomina.html')

@app.route('/empleados/revision_nomina')
def revision_nomina():
    return render_template('revision_nomina.html')

@app.route('/empleados/error_calculo_nomina')
def error_calculo_nomina():
    return render_template('error_calculo_nomina.html')

@app.route('/empleados/evaluar_desempeno')
def evaluar_desempeno():
    return render_template('evaluar_desempeno.html')

@app.route('/empleados/resultado_evaluacion')
def resultado_evaluacion():
    return render_template('resultado_evaluacion.html')

@app.route('/empleados/actualizar_evaluacion')
def actualizar_evaluacion():
    return render_template('actualizar_evaluacion.html')

@app.route('/empleados/error_evaluacion')
def error_evaluacion():
    return render_template('error_evaluacion.html')

@app.route('/empleados/registrar_ventas')
def registrar_ventas():
    return render_template('registrar_ventas.html')

@app.route('/empleados/consultar_ventas')
def consultar_ventas():
    return render_template('consultar_ventas.html')

@app.route('/empleados/actualizar_ventas')
def actualizar_ventas():
    return render_template('actualizar_ventas.html')

# ADT

@app.route('/tienda/gestion_inventario')
def gestion_inventario():
    return render_template('gestion_inventario.html')

@app.route('/tienda/gestion_proveedores')
def gestion_proveedores():
    return render_template('gestion_proveedores.html')

@app.route('/tienda/gestion_promociones')
def gestion_promociones():
    return render_template('gestion_promociones.html')

@app.route('/tienda/reportes_financieros')
def reportes_financieros():
    return render_template('reportes_financieros.html')

@app.route('/tienda/gestion_productos')
def gestion_productos():
    return render_template('gestion_productos.html')

@app.route('/tienda/registro_producto')
def registro_producto():
    return render_template('registro_producto.html')


@app.route('/tienda/registro_proveedor')
def registro_proveedor():
    return render_template('registro_proveedor.html')

@app.route('/tienda/crear_promocion')
def crear_promocion():
    return render_template('crear_promocion.html')

@app.route('/tienda/actualizar_precio_producto')
def actualizar_precio_producto():
    return render_template('actualizar_precio_producto.html')

@app.route('/tienda/gestion_devoluciones')
def gestion_devoluciones():
    return render_template('gestion_devoluciones.html')

##################################


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/ADT')
def ADT():
    return render_template('adt_index.html')

@app.route('/process_sale')
def process_sale():
    return render_template('ventas')

@app.route('/generate_report')
def generate_report():
    return render_template('ventas')

@app.route('/configure_promotion')
def configure_promotion():
    return render_template('ventas')

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
