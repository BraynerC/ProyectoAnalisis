from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pyodbc  # Librería para conectar a SQL Server

app = Flask(__name__)
app.secret_key = 'Hola'

def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=ServicentroCorazonDB;'
        'Trusted_Connection=yes;' 
    )
    return connection

def requiere_autenticacion(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor inicia sesión para continuar.')
            return redirect(url_for('autenticacion'))
        return f(*args, **kwargs)
    return decorada

def obtener_roles(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    SELECT rol
    FROM Usuarios
    WHERE usuario_id = ?
    """
    cursor.execute(query, (usuario_id,))
    roles = cursor.fetchall()
    conn.close()
    
    return [rol[0] for rol in roles]  # Devuelve una lista de roles

def requiere_rol(roles_permitidos):
    def decorador(f):
        @wraps(f)
        def decorada(*args, **kwargs):
            user_roles = session.get('user_roles', [])
            if not any(rol in roles_permitidos for rol in user_roles):
                flash('No tienes permiso para acceder a esta página.', 'danger')
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorada
    return decorador

@app.route('/')
@requiere_autenticacion
def home():
    usuario_id = session['usuario_id']
    user_roles = session.get('user_roles', [])  # Obtener roles de la sesión
    print(f"Roles del usuario: {user_roles}")  # Debug
    return render_template('index.html', user_roles=user_roles)

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

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/ADT')
def ADT():
    return render_template('adt_index.html')

@app.route('/pre_ventas')
def pre_ventas():
    return render_template('pre_ventas.html')

@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/gestion_devoluciones')
def gestion_devoluciones():
    return render_template('gestion_devoluciones.html')

@app.route('/solicitar_vacaciones')
def solicitar_vacaciones():
    return render_template('solicitar_vacaciones.html')

@app.route('/ver_solicitudes')
def ver_solicitudes():
    return render_template('ver_solicitudes.html')

@app.route('/resultado_evaluacion')
def resultado_evaluacion():
    return render_template('resultado_evaluacion.html')

@app.route('/consultar_ventas')
def consultar_ventas():
    return render_template('consultar_ventas.html')

@app.route('/gestion_inventario')
def gestion_inventario():
    return render_template('gestion_inventario.html')

@app.route('/gestion_proveedores')
def gestion_proveedores():
    return render_template('gestion_proveedores.html')

@app.route('/gestion_promociones')
def gestion_promociones():
    return render_template('gestion_promociones.html')

@app.route('/gestion_productos')
def gestion_productos():
    return render_template('gestion_productos.html')

@app.route('/reportes_financieros')

def reportes_financieros():
    return render_template('reportes_financieros.html')

@app.route('/cashier_functions')
def cashier_functions():
    return render_template('cashier_functions.html')

@app.route('/process_sale')
def process_sale():
    return render_template('process_sale.html')

@app.route('/configure_promotion')
def configure_promotion():
    return render_template('configure_promotion.html')

@app.route('/technical_functions')
def technical_functions():
    return render_template('technical_functions.html')

@app.route('/configure_parameters')
def configure_parameters():
    return render_template('configure_parameters.html')

@app.route('/registro_producto')
def registro_producto():
    return render_template('registro_producto.html')

@app.route('/registro_proveedor')
def registro_proveedor():
    return render_template('registro_proveedor.html')

@app.route('/crear_promocion')
def crear_promocion():
    return render_template('crear_promocion.html')

@app.route('/actualizar_precio_producto')
def actualizar_precio_producto():
    return render_template('actualizar_precio_producto.html')



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

        if user is None:
            flash('El nombre de usuario no existe', 'danger')
        elif not check_password_hash(user[2], password):
            flash('La contraseña es incorrecta', 'danger')
        else:
            session['usuario_id'] = user[0]  # ID del usuario
            session['user_roles'] = obtener_roles(user[0])  # Guarda todos los roles en sesión
            print(f"Roles guardados en sesión: {session['user_roles']}")  # Debug
            
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        
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
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            cursor.execute('''INSERT INTO Usuarios (nombre_usuario, contrasena, rol, estatus)
                              VALUES (?, ?, 'Cliente', 'Activo')''', (username, hashed_password))
            conn.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('autenticacion'))
        except Exception as e:
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
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
    except Exception as e:
        flash(f'Error al cargar el empleado: {str(e)}', 'danger')
        return redirect(url_for('detalles_empleado'))

    return render_template('editar_empleado.html', empleado=empleado)

if __name__ == '__main__':
    app.run(debug=True)
