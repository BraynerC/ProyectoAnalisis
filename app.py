from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
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
    user_roles = session.get('user_roles', [])  
    print(f"Roles del usuario: {user_roles}")  
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

@app.route('/admin_functions')
def admin_functions():
    return render_template('admin_functions.html')

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

#productos

@app.route('/productos')
@requiere_rol(['Administrador','Gerente','Empleado'])  
def listar_productos():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT producto_id, nombre_producto, cantidad, precio_unitario FROM Inventarios")
            productos = cursor.fetchall()
    except Exception as e:
        flash(f'Error al obtener productos: {str(e)}', 'danger')
        productos = []

    return render_template('listar_productos.html', productos=productos)

@app.route('/registro_producto', methods=['GET', 'POST'])
@requiere_rol(['Administrador','Gerente','Empleado']) 
def registro_producto():
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Inventarios (nombre_producto, cantidad, precio_unitario, fecha_ultima_actualizacion)
                                  VALUES (?, ?, ?, GETDATE())""",
                               (nombre_producto, cantidad, precio))
                conn.commit()
                flash('Producto registrado con éxito', 'success')
        except Exception as e:
            flash(f'Error al registrar el producto: {str(e)}', 'danger')

        return redirect(url_for('registro_producto'))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT producto_id, nombre_producto, cantidad, precio_unitario FROM Inventarios")
            productos = cursor.fetchall()
    except Exception as e:
        flash(f'Error al obtener productos: {str(e)}', 'danger')
        productos = []

    return render_template('registro_producto.html', productos=productos)

@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
@requiere_rol(['Administrador','Gerente','Empleado']) 
def editar_producto(producto_id):
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE Inventarios SET nombre_producto = ?, cantidad = ?, precio_unitario = ?, fecha_ultima_actualizacion = GETDATE()
                                  WHERE producto_id = ?""",
                               (nombre_producto, cantidad, precio, producto_id))
                conn.commit()
                flash('Producto actualizado con éxito', 'success')
        except Exception as e:
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')

        return redirect(url_for('listar_productos'))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_producto, cantidad, precio_unitario FROM Inventarios WHERE producto_id = ?", (producto_id,))
            producto = cursor.fetchone()
    except Exception as e:
        flash(f'Error al obtener el producto: {str(e)}', 'danger')
        return redirect(url_for('listar_productos'))

    return render_template('editar_producto.html', producto=producto, producto_id=producto_id)

@app.route('/eliminar_producto/<int:producto_id>')
@requiere_rol(['Administrador', 'Gerente'])  
def eliminar_producto(producto_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Inventarios WHERE producto_id = ?", (producto_id,))
            conn.commit()
            flash('Producto eliminado con éxito', 'success')
    except Exception as e:
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')

    return redirect(url_for('listar_productos'))

#promociones

@app.route('/promociones')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def listar_promociones():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT promocion_id, nombre_promocion, detalles, fecha_inicio, fecha_fin FROM Promociones")
            promociones = cursor.fetchall()
    except Exception as e:
        flash(f'Error al obtener promociones: {str(e)}', 'danger')
        promociones = []

    return render_template('listar_promociones.html', promociones=promociones)

@app.route('/registro_promocion', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def registro_promocion():
    if request.method == 'POST':
        nombre_promocion = request.form['nombre_promocion']
        detalles = request.form['detalles']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']

        # Convertir las cadenas de fecha a objetos datetime
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Error en el formato de las fechas. Asegúrate de que sean válidas.', 'danger')
            return redirect(url_for('registro_promocion'))

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO Promociones (nombre_promocion, detalles, fecha_inicio, fecha_fin, fecha_creacion)
                                  VALUES (?, ?, ?, ?, GETDATE())""",
                               (nombre_promocion, detalles, fecha_inicio, fecha_fin))
                conn.commit()
                flash('Promoción registrada con éxito', 'success')
        except Exception as e:
            flash(f'Error al registrar la promoción: {str(e)}', 'danger')

        return redirect(url_for('registro_promocion'))

    return render_template('registro_promocion.html')


@app.route('/editar_promocion/<int:promocion_id>', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def editar_promocion(promocion_id):
    if request.method == 'POST':
        nombre_promocion = request.form['nombre_promocion']
        detalles = request.form['detalles']
        fecha_inicio_str = request.form['fecha_inicio']
        fecha_fin_str = request.form['fecha_fin']

        # Convertir cadenas a datetime
        try:
            # Asegúrate de que el formato de las fechas esté correcto
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M')
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Error: Las fechas deben estar en el formato correcto (YYYY-MM-DDTHH:MM).', 'danger')
            return redirect(url_for('editar_promocion', promocion_id=promocion_id))

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""UPDATE Promociones 
                                  SET nombre_promocion = ?, detalles = ?, fecha_inicio = ?, fecha_fin = ?
                                  WHERE promocion_id = ?""",
                               (nombre_promocion, detalles, fecha_inicio, fecha_fin, promocion_id))
                conn.commit()
                flash('Promoción actualizada con éxito', 'success')
        except Exception as e:
            flash(f'Error al actualizar la promoción: {str(e)}', 'danger')

        return redirect(url_for('listar_promociones'))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_promocion, detalles, fecha_inicio, fecha_fin FROM Promociones WHERE promocion_id = ?", (promocion_id,))
            promocion = cursor.fetchone()
    except Exception as e:
        flash(f'Error al obtener la promoción: {str(e)}', 'danger')
        return redirect(url_for('listar_promociones'))

    return render_template('editar_promocion.html', promocion=promocion, promocion_id=promocion_id)


@app.route('/eliminar_promocion/<int:promocion_id>')
@requiere_rol(['Administrador', 'Gerente'])
def eliminar_promocion(promocion_id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Promociones WHERE promocion_id = ?", (promocion_id,))
            conn.commit()
            flash('Promoción eliminada con éxito', 'success')
    except Exception as e:
        flash(f'Error al eliminar la promoción: {str(e)}', 'danger')

    return redirect(url_for('listar_promociones'))

#proveedor

@app.route('/registro_proveedor', methods=['GET', 'POST'])
def registro_proveedor():
    if request.method == 'POST':
        nombre_proveedor = request.form['nombre_proveedor']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        email = request.form['email']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO proveedores (nombre_proveedor, contacto, telefono, email) VALUES (?, ?, ?, ?)',
                       (nombre_proveedor, contacto, telefono, email))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor registrado exitosamente', 'success')
        return redirect(url_for('listar_proveedores'))

    return render_template('registro_proveedor.html')

@app.route('/listar_proveedores')
def listar_proveedores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM proveedores')
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('listar_proveedores.html', proveedores=proveedores)

@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre_proveedor = request.form['nombre_proveedor']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        email = request.form['email']

        cursor.execute('UPDATE proveedores SET nombre_proveedor = ?, contacto = ?, telefono = ?, email = ? WHERE id = ?',
                       (nombre_proveedor, contacto, telefono, email, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Proveedor actualizado exitosamente', 'success')
        return redirect(url_for('listar_proveedores'))

    cursor.execute('SELECT * FROM proveedores WHERE id = ?', (id,))
    proveedor = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('editar_proveedor.html', proveedor=proveedor)

@app.route('/eliminar_proveedor/<int:id>', methods=['POST'])
def eliminar_proveedor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM proveedores WHERE id = ?', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Proveedor eliminado exitosamente', 'success')
    return redirect(url_for('listar_proveedores'))

#rutas

@app.route('/actualizar_precio_producto')
def actualizar_precio_producto():
    return render_template('actualizar_precio_producto.html')

@app.route('/generate_report')
def generate_report():
    return render_template('generate_report.html')

@app.route('/configure_payment_method')
def configure_payment_method():
    return render_template('configure_payment_method.html')



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
                              VALUES (?, ?, 'Administrador', 'Activo')''', (username, hashed_password))
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
