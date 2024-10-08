from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pyodbc  # Librería para conectar a SQL Server

app = Flask(__name__)
app.secret_key = 'Hola'

@app.route('/')
def home():
    return render_template('index.html')

def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=Desktop\\SQLEXPRESS;'  # Cambia esto si tu instancia tiene otro nombre
        'DATABASE=ServicentroCorazonDB;'
        'Trusted_Connection=yes;' 
    )
    return connection

def obtener_rol_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT e.rol
    FROM Empleados e
    INNER JOIN Usuarios u ON u.empleado_id = e.empleado_id
    WHERE u.usuario_id = ?
    """
    cursor.execute(query, (usuario_id,))
    rol = cursor.fetchone()
    conn.close()
    
    return rol[0] if rol else None

def requiere_rol(roles_permitidos):
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            rol = session.get('rol')
            if rol not in roles_permitidos:
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorada
    return decorador

def requiere_autenticacion(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor inicia sesión para continuar.')
            return redirect(url_for('autenticacion'))
        return f(*args, **kwargs)
    return decorada

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada con éxito')
    return redirect(url_for('autenticacion'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Módulo Reabastecimiento

@app.route('/reabastecimiento')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico'])
def reabastecimiento():
    return render_template('reabastecimiento.html')

@app.route('/configurar_umbrales')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico'])
def configurar_umbrales():
    return render_template('configurar_umbrales.html')

@app.route('/solicitud_reabastecimiento')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico'])
def solicitud_reabastecimiento():
    return render_template('solicitud_reabastecimiento.html')

@app.route('/configurar_alertas')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico'])
def configurar_alertas():
    return render_template('configurar_alertas.html')

@app.route('/registro_entregas')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico'])
def registro_entregas():
    return render_template('registro_entregas.html')

@app.route('/incidencias')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico'])
def incidencias():
    return render_template('incidencias.html')

# Módulo de Autenticación

@app.route('/autenticacion', methods=['GET', 'POST'])
def autenticacion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Usuarios WHERE nombre_usuario = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password): 
            session['usuario_id'] = user[0]  # ID del usuario
            session['rol'] = obtener_rol_usuario(user[0])  # Obtener el rol del usuario
            flash('Inicio de sesión exitoso')
            return redirect(url_for('home'))
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

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Usuarios WHERE nombre_usuario = ?', (username,))
        user = cursor.fetchone()

        if user:
            flash('El nombre de usuario ya está en uso')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

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
    if 'usuario_id' not in session:
        return redirect(url_for('autenticacion'))
    return render_template('emp_index.html')

@app.route('/empleados/crear_empleado', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente'])
def crear_empleado():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        fecha_contratacion = request.form.get('fecha_contratacion')
        rol = request.form.get('rol')
        estatus = request.form.get('estatus')

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Empleados (nombre, apellido, email, telefono, direccion, fecha_contratacion, rol, estatus)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                               (nombre, apellido, email, telefono, direccion, fecha_contratacion, rol, estatus))

                conn.commit()
                flash('Empleado creado con éxito', 'success')
                return redirect(url_for('detalles_empleado')) 
        except Exception as e:
            flash(f'Error al crear el empleado: {str(e)}', 'danger')

    return render_template('crear_empleado.html')

@app.route('/empleados/detalles_empleado')
@requiere_rol(['Administrador', 'Gerente'])
def detalles_empleado():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT empleado_id, nombre, apellido, email, telefono, rol, estatus FROM Empleados")
            empleados = cursor.fetchall()

            empleados_list = []
            for empleado in empleados:
                empleados_list.append({
                    'empleado_id': empleado.empleado_id,
                    'nombre': empleado.nombre,
                    'apellido': empleado.apellido,
                    'email': empleado.email,
                    'telefono': empleado.telefono,
                    'rol': empleado.rol,
                    'estatus': empleado.estatus
                })

    except Exception as e:
        flash(f'Error al cargar la lista de empleados: {str(e)}', 'danger')
        return redirect(url_for('crear_empleado'))
    
    return render_template('detalles_empleado.html', empleados=empleados_list)

@app.route('/empleados/editar_empleado/<int:empleado_id>', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente'])
def editar_empleado(empleado_id):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        direccion = request.form.get('direccion')
        fecha_contratacion = request.form.get('fecha_contratacion')
        rol = request.form.get('rol')
        estatus = request.form.get('estatus')

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE Empleados
                                  SET nombre = ?, apellido = ?, email = ?, telefono = ?, direccion = ?, fecha_contratacion = ?, rol = ?, estatus = ?
                                  WHERE empleado_id = ?""",
                               (nombre, apellido, email, telefono, direccion, fecha_contratacion, rol, estatus, empleado_id))

                conn.commit()
                flash('Empleado actualizado con éxito', 'success')
                return redirect(url_for('detalles_empleado', empleado_id=empleado_id))
        except Exception as e:
            flash(f'Error al actualizar el empleado: {str(e)}', 'danger')

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Empleados WHERE empleado_id = ?", (empleado_id,))
            empleado = cursor.fetchone()
            if empleado is None:
                flash('Empleado no encontrado', 'danger')
                return redirect(url_for('editar_empleado'))

            empleado = {
                'empleado_id': empleado.empleado_id,
                'nombre': empleado.nombre,
                'apellido': empleado.apellido,
                'email': empleado.email,
                'telefono': empleado.telefono,
                'direccion': empleado.direccion,
                'fecha_contratacion': empleado.fecha_contratacion,
                'rol': empleado.rol,
                'estatus': empleado.estatus
            }
    except Exception as e:
        flash(f'Error al cargar los datos del empleado: {str(e)}', 'danger')
        return redirect(url_for('detalles_empleado'))

    return render_template('editar_empleado.html', empleado=empleado)

@app.route('/empleados/eliminar_empleado/<int:empleado_id>', methods=['POST'])
@requiere_rol(['Administrador', 'Gerente'])
def eliminar_empleado(empleado_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Empleados WHERE empleado_id = ?", (empleado_id,))
            conn.commit()
            flash('Empleado eliminado con éxito', 'success')
            return redirect(url_for('detalles_empleado'))
    except Exception as e:
        flash(f'Error al eliminar el empleado: {str(e)}', 'danger')
        return redirect(url_for('detalles_empleado'))

@app.route('/empleados/solicitar_vacaciones')
def solicitar_vacaciones():
    if 'usuario_id' not in session:
         return redirect(url_for('autenticacion'))
    return render_template('solicitar_vacaciones.html')

@app.route('/ver_solicitudes')
def ver_solicitudes():
    if 'usuario_id' not in session:
        return redirect(url_for('autenticacion'))

    usuario_id = session['usuario_id']
    rol = session.get('rol')  

    if rol in ['Administrador', 'Gerente']:
        solicitudes = SolicitudVacaciones.query.all()  
    else:
        solicitudes = SolicitudVacaciones.query.filter_by(empleado_id=usuario_id).all()  

    return render_template('ver_solicitudes.html', solicitudes=solicitudes, rol=rol)

@app.route('/empleados/revisar_solicitud')
@requiere_rol(['Administrador', 'Gerente'])
def revisar_solicitud():
    return render_template('revisar_solicitud.html')

@app.route('/empleados/calcular_nomina')
@requiere_rol(['Administrador', 'Gerente'])
def calcular_nomina():
    return render_template('calcular_nomina.html')

@app.route('/empleados/revision_nomina')
@requiere_rol(['Administrador', 'Gerente'])
def revision_nomina():
    return render_template('revision_nomina.html')

@app.route('/empleados/error_calculo_nomina')
@requiere_rol(['Administrador', 'Gerente'])
def error_calculo_nomina():
    return render_template('error_calculo_nomina.html')

@app.route('/empleados/evaluar_desempeno')
@requiere_rol(['Administrador', 'Gerente'])
def evaluar_desempeno():
    return render_template('evaluar_desempeno.html')

@app.route('/empleados/resultado_evaluacion')
def resultado_evaluacion():
    if 'usuario_id' not in session:
        return redirect(url_for('autenticacion'))

    usuario_id = session['usuario_id']
    rol = session.get('rol')

    if rol in ['Administrador', 'Gerente']:
        evaluaciones = EvaluacionDesempeno.query.all()
    else:
        evaluaciones = EvaluacionDesempeno.query.filter_by(empleado_id=usuario_id).all()

    return render_template('resultado_evaluacion.html', evaluaciones=evaluaciones, rol=rol)


@app.route('/empleados/actualizar_evaluacion')
@requiere_rol(['Administrador', 'Gerente'])
def actualizar_evaluacion():
    return render_template('actualizar_evaluacion.html')

@app.route('/empleados/error_evaluacion')
@requiere_rol(['Administrador', 'Gerente'])
def error_evaluacion():
    return render_template('error_evaluacion.html')

@app.route('/empleados/registrar_ventas')
@requiere_rol(['Administrador', 'Gerente'])
def registrar_ventas():
    
    return render_template('registrar_ventas.html')

@app.route('/empleados/consultar_ventas')
def consultar_ventas():
    if 'usuario_id' not in session:
        return redirect(url_for('autenticacion'))

    rol = session.get('rol')  # Obtener el rol del usuario desde la sesión
    return render_template('consultar_ventas.html', rol=rol)

@app.route('/empleados/actualizar_ventas')
@requiere_rol(['Administrador', 'Gerente'])
def actualizar_ventas():
    return render_template('actualizar_ventas.html')

# ADT

@app.route('/tienda/gestion_inventario')
@requiere_rol(['Administrador', 'Gerente'])
def gestion_inventario():
    return render_template('gestion_inventario.html')

@app.route('/tienda/gestion_proveedores')
@requiere_rol(['Administrador', 'Gerente'])
def gestion_proveedores():
    return render_template('gestion_proveedores.html')

@app.route('/tienda/gestion_promociones')
@requiere_rol(['Administrador', 'Gerente'])
def gestion_promociones():
    return render_template('gestion_promociones.html')

@app.route('/tienda/reportes_financieros')
@requiere_rol(['Administrador', 'Gerente'])
def reportes_financieros():
    return render_template('reportes_financieros.html')

@app.route('/tienda/gestion_productos')
@requiere_rol(['Administrador', 'Gerente'])
def gestion_productos():
    return render_template('gestion_productos.html')

@app.route('/tienda/registro_producto')
@requiere_rol(['Administrador', 'Gerente'])
def registro_producto():
    return render_template('registro_producto.html')


@app.route('/tienda/registro_proveedor')
@requiere_rol(['Administrador', 'Gerente'])
def registro_proveedor():
    return render_template('registro_proveedor.html')

@app.route('/tienda/crear_promocion')
@requiere_rol(['Administrador', 'Gerente'])
def crear_promocion():
    return render_template('crear_promocion.html')

@app.route('/tienda/actualizar_precio_producto')
@requiere_rol(['Administrador', 'Gerente'])
def actualizar_precio_producto():
    return render_template('actualizar_precio_producto.html')

@app.route('/tienda/gestion_devoluciones')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def gestion_devoluciones():
    return render_template('gestion_devoluciones.html')

##################################

@app.route('/servicios')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def servicios():
    return render_template('servicios.html')

@app.route('/ADT')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def ADT():
    return render_template('adt_index.html')

@app.route('/process_sale')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def process_sale():
    return render_template('ventas')

@app.route('/generate_report')
@requiere_rol(['Administrador', 'Gerente'])
def generate_report():
    return render_template('ventas')


@app.route('/configure_promotion')
@requiere_rol(['Administrador', 'Gerente'])
def configure_promotion():
    return render_template('ventas')

@app.route('/configure_payment_method')
@requiere_rol(['Administrador', 'Gerente'])
def configure_payment_method():
    return render_template('ventas')

@app.route('/pre_ventas')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def pre_ventas():
    return render_template('pre_ventas.html')

@app.route('/cashier_functions')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def cashier_functions():
    return render_template('cashier_functions.html')

@app.route('/admin_functions')
@requiere_rol(['Administrador', 'Gerente'])
def admin_functions():
    return render_template('admin_functions.html')

@app.route('/mantenimiento')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico','Mantenimiento'])
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/technical_functions')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico','Mantenimiento'])
def technical_functions():
    return render_template('technical_functions.html')

@app.route('/admin_functions_maintenance')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico','Mantenimiento'])
def admin_functions_maintenance():
    return render_template('admin_functions_maintenance.html')

@app.route('/configure_parameters')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico','Mantenimiento'])
def configure_parameters():
    return render_template('technical_functions')

@app.route('/generate_maintenance_report')
@requiere_rol(['Administrador', 'Gerente', 'Tecnico','Mantenimiento'])
def generate_maintenance_report():
    return render_template('admin_functions_maintenance')

@app.route('/train_system')
@requiere_rol(['Administrador', 'Gerente'])
def train_system():
    return render_template('admin_functions_maintenance')


if __name__ == '__main__':
    app.run(debug=True)