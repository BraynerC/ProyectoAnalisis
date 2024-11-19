from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from flask import jsonify
import pyodbc  


app = Flask(__name__)
app.secret_key = 'Hola'

def get_db_connection():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=ServicentroCorazonDB;'
        'Trusted_Connection=yes;' 
    )

def execute_query(query, params=(), fetch=True):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch and query.strip().upper().startswith('SELECT'):
                return cursor.fetchall() 

            conn.commit()  

    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return None

def requiere_autenticacion(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor inicia sesión para continuar.')
            return redirect(url_for('autenticacion'))
        return f(*args, **kwargs)
    return decorada

def obtener_roles(usuario_id):
    roles = execute_query("SELECT rol FROM Usuarios WHERE usuario_id = ?", (usuario_id,))
    return [rol[0] for rol in roles] if roles else []

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

@app.route('/ADT')
def ADT():
    return render_template('adt_index.html')

@app.route('/pre_ventas')
def pre_ventas():
    return render_template('pre_ventas.html')

@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

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

@app.route('/configure_promotion')
def configure_promotion():
    return render_template('configure_promotion.html')

@app.route('/technical_functions')
def technical_functions():
    # Obtener los parámetros actuales de la DB
    query = "SELECT pressure_limit, temperature_limit, fuel_level_limit, fecha_actualizacion FROM Parametros_Mantenimiento WHERE id = 1"
    parameters = execute_query(query)
    
    if parameters:
        pressure_limit, temperature_limit, fuel_level_limit, last_update = parameters[0]
    else:
        pressure_limit, temperature_limit, fuel_level_limit, last_update = 0, 0, 0, None

    return render_template('technical_functions.html', 
                           pressure_limit=pressure_limit,
                           temperature_limit=temperature_limit,
                           fuel_level_limit=fuel_level_limit,
                           last_update=last_update)


@app.route('/update_parameters', methods=['POST'])
def update_parameters():
    try:
        pressure_limit = request.form['pressure_limit']
        temperature_limit = request.form['temperature_limit']
        fuel_level_limit = request.form['fuel_level_limit']
        
        query_check = "SELECT COUNT(*) FROM Parametros_Mantenimiento WHERE id = 1"
        result = execute_query(query_check, fetch=True)
        count = result[0][0] if result else 0
        
        if count == 0:
            query_insert = """
            INSERT INTO Parametros_Mantenimiento (pressure_limit, temperature_limit, fuel_level_limit, fecha_actualizacion)
            VALUES (?, ?, ?, GETDATE())
            """
            execute_query(query_insert, (pressure_limit, temperature_limit, fuel_level_limit), fetch=False)
            flash("Parámetros guardados exitosamente.", "success")
        else:
            query_update = """
            UPDATE Parametros_Mantenimiento
            SET pressure_limit = ?, temperature_limit = ?, fuel_level_limit = ?, fecha_actualizacion = GETDATE()
            WHERE id = 1
            """
            execute_query(query_update, (pressure_limit, temperature_limit, fuel_level_limit), fetch=False)
            flash("Parámetros actualizados exitosamente.", "success")
            
    except Exception as e:
        flash(f"Error al actualizar parámetros: {str(e)}", "danger")
    
    return redirect(url_for('technical_functions'))


@app.route('/manual_check', methods=['POST'])
def manual_check():
    try:

        query = "SELECT pressure_limit, temperature_limit, fuel_level_limit FROM Parametros_Mantenimiento WHERE id = 1"
        parameters = execute_query(query)
        
        if parameters:
            pressure_limit, temperature_limit, fuel_level_limit = parameters[0]

            message = f"Verificación exitosa: Presión: {pressure_limit} PSI, Temperatura: {temperature_limit} °C, Combustible: {fuel_level_limit} Litros"
            flash(message, 'success')
        else:
            flash("No se encontraron parámetros en la base de datos.", 'danger')

    except Exception as e:
        flash(f"Error en la verificación manual: {str(e)}", "danger")
    
    return redirect(url_for('technical_functions'))

@app.route('/get_parameters')
def get_parameters():
    try:
        query = "SELECT pressure_limit, temperature_limit, fuel_level_limit, fecha_actualizacion FROM Parametros_Mantenimiento WHERE id = 1"
        parameters = execute_query(query)

        if parameters:
            pressure_limit, temperature_limit, fuel_level_limit, last_update = parameters[0]

            return jsonify({
                'pressure_limit': pressure_limit,
                'temperature_limit': temperature_limit,
                'fuel_level_limit': fuel_level_limit,
                'last_update': last_update.strftime('%d/%b/%Y %I:%M %p')
            })
        else:
            return jsonify({
                'pressure_limit': 0,
                'temperature_limit': 0,
                'fuel_level_limit': 0,
                'last_update': 'No disponible'
            })
    except Exception as e:

        return jsonify({'error': f'Error al obtener los parámetros: {str(e)}'}), 500


@app.route('/actualizar_precio_producto')
def actualizar_precio_producto():
    return render_template('actualizar_precio_producto.html')

@app.route('/generate_report')
def generate_report():
    return render_template('generate_report.html')

@app.route('/configure_payment_method')
def configure_payment_method():
    return render_template('configure_payment_method.html')

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

@app.route('/gestion_servicios')
def gestion_servicios():
    return render_template('gestion_servicios.html')

@app.route('/process_sale', methods=['POST'])
def process_sale():
    product_code = request.form['product_code']
    quantity = int(request.form['quantity'])
    customer_age = request.form.get('customer_age')

    producto = execute_query("""
        SELECT precio, restricciones
        FROM Productos
        WHERE codigo_producto = ?
    """, (product_code,))

    if producto:
        precio, restricciones = producto[0]

        if restricciones and customer_age and int(customer_age) < int(restricciones):
            flash('El cliente no cumple con las restricciones de edad para este producto.', 'danger')
            return redirect(url_for('consultar_ventas'))

        total = precio * quantity
        if quantity > 5:  
            total *= 0.9  

        execute_query("""
            INSERT INTO Ventas (codigo_producto, cantidad, total, fecha)
            VALUES (?, ?, ?, ?)
        """, (product_code, quantity, total, datetime.now()))
        
        execute_query("""
            UPDATE Productos
            SET stock = stock - ?
            WHERE codigo_producto = ?
        """, (quantity, product_code))

        flash('Venta procesada con éxito. Total: ${:.2f}'.format(total), 'success')
    else:
        flash('Producto no encontrado.', 'danger')

    return redirect(url_for('consultar_ventas'))

@app.route('/consultar_servicios')
def consultar_servicios():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Servicios_Adicionales")
        servicios = cursor.fetchall()
        print(servicios)  # Agrega esto para verificar los resultados
        
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        servicios = []

    finally:
        cursor.close()
        conn.close()
    
    return render_template('consultar_servicios.html', servicios=servicios)


@app.route('/registrar_servicio', methods=['GET', 'POST'])
def registrar_servicio():
    if request.method == 'POST':
        tipo_servicio = request.form['tipo_servicio']
        detalles = request.form['detalles']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Servicios_Adicionales (tipo_servicio, descripcion, fecha_servicio) VALUES (?, ?, GETDATE())", 
                       (tipo_servicio, detalles))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('gestion_servicios')) 

    return render_template('registrar_servicio.html')  


@app.route('/editar_servicio/<int:servicio_id>', methods=['GET', 'POST'])
def editar_servicio(servicio_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        tipo_servicio = request.form['tipo_servicio']
        detalles = request.form['detalles']
        cursor.execute('UPDATE Servicios_Adicionales SET tipo_servicio = ?, descripcion = ? WHERE servicio_id = ?',
                       (tipo_servicio, detalles, servicio_id))
        conn.commit()
        conn.close()
        return redirect(url_for('consultar_servicios'))

    cursor.execute('SELECT servicio_id, tipo_servicio, descripcion FROM Servicios_Adicionales WHERE servicio_id = ?', (servicio_id,))
    servicio = cursor.fetchone()
    conn.close()
    return render_template('editar_servicio.html', servicio=servicio)

@app.route('/eliminar_servicio/<int:servicio_id>', methods=['POST'])
def eliminar_servicio(servicio_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Servicios_Adicionales WHERE servicio_id = ?', (servicio_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('consultar_servicios'))

@app.route('/productos')
@requiere_rol(['Administrador','Gerente','Empleado'])  
def listar_productos():
    productos = execute_query("SELECT producto_id, nombre_producto, cantidad, precio_unitario FROM Inventarios")
    return render_template('listar_productos.html', productos=productos)

@app.route('/registro_producto', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def registro_producto():
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        execute_query("""INSERT INTO Inventarios (nombre_producto, cantidad, precio_unitario, fecha_ultima_actualizacion)
                          VALUES (?, ?, ?, GETDATE())""",
                       (nombre_producto, cantidad, precio), fetch=False)
        flash('Producto registrado con éxito', 'success')
        return redirect(url_for('registro_producto'))

    return render_template('registro_producto.html')

@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
@requiere_rol(['Administrador','Gerente','Empleado']) 
def editar_producto(producto_id):
    if request.method == 'POST':
        nombre_producto = request.form['nombre_producto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        execute_query("""UPDATE Inventarios SET nombre_producto = ?, cantidad = ?, precio_unitario = ?, fecha_ultima_actualizacion = GETDATE()
                          WHERE producto_id = ?""",
                       (nombre_producto, cantidad, precio, producto_id), fetch=False)
        flash('Producto actualizado con éxito', 'success')
        return redirect(url_for('listar_productos'))

    producto = execute_query("SELECT nombre_producto, cantidad, precio_unitario FROM Inventarios WHERE producto_id = ?", (producto_id,))

    if not producto:
        flash('Error: Producto no encontrado.', 'danger')
        return redirect(url_for('listar_productos'))

    return render_template('editar_producto.html', producto=producto[0], producto_id=producto_id)

@app.route('/eliminar_producto/<int:producto_id>', methods=['POST'])
@requiere_rol(['Administrador', 'Gerente'])  
def eliminar_producto(producto_id):
    execute_query("DELETE FROM Inventarios WHERE producto_id = ?", (producto_id,), fetch=False)
    flash('Producto eliminado con éxito', 'success')
    return redirect(url_for('listar_productos'))


@app.route('/promociones')
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def listar_promociones():
    promociones = execute_query("""
        SELECT p.id, p.nombre, p.detalles, p.fecha_inicio, p.fecha_fin, p.descuento, i.nombre_producto
        FROM Promociones p
        JOIN Inventarios i ON p.producto_id = i.producto_id
    """)
    return render_template('listar_promociones.html', promociones=promociones)



@app.route('/registro_promocion', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def registro_promocion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        detalles = request.form['detalles']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        descuento = request.form['descuento']
        producto_id = request.form['producto_id']

        # Convierte las fechas a tipo datetime
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M')
        
        # Inserta la nueva promoción en la base de datos
        execute_query("""INSERT INTO Promociones (nombre, detalles, fecha_inicio, fecha_fin, descuento, fecha_creacion, producto_id)
                          VALUES (?, ?, ?, ?, ?, GETDATE(), ?)""",
                       (nombre, detalles, fecha_inicio, fecha_fin, descuento, producto_id))

        flash('Promoción registrada con éxito', 'success')
        return redirect(url_for('listar_promociones'))

    # Obtener todos los productos disponibles
    productos = execute_query("SELECT producto_id, nombre_producto FROM Inventarios")
    return render_template('registro_promocion.html', productos=productos)

@app.route('/editar_promocion/<int:id>', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def editar_promocion(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        detalles = request.form['detalles']
        fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%dT%H:%M')
        fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%dT%H:%M')

        execute_query("""UPDATE Promociones 
                          SET nombre = ?, detalles = ?, 
                              fecha_inicio = ?, fecha_fin = ? 
                          WHERE id = ?""",
                       (nombre, detalles, fecha_inicio, fecha_fin, id))

        flash('Promoción actualizada con éxito', 'success')
        return redirect(url_for('listar_promociones'))

    promocion = execute_query("SELECT nombre, detalles, fecha_inicio, fecha_fin FROM Promociones WHERE id = ?", (id,))
    
    if not promocion:
        flash('Promoción no encontrada', 'danger')
        return redirect(url_for('listar_promociones'))

    return render_template('editar_promocion.html', promocion=promocion[0])

@app.route('/eliminar_promocion/<int:id>')
@requiere_rol(['Administrador', 'Gerente'])
def eliminar_promocion(id):
    execute_query("DELETE FROM Promociones WHERE id = ?", (id,))
    flash('Promoción eliminada con éxito', 'success')
    return redirect(url_for('listar_promociones'))

@app.route('/registro_proveedor', methods=['GET', 'POST'])
def registro_proveedor():
    if request.method == 'POST':
        nombre_proveedor = request.form['nombre_proveedor']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        email = request.form['email']

        execute_query('INSERT INTO proveedores (nombre_proveedor, contacto, telefono, email) VALUES (?, ?, ?, ?)',
                       (nombre_proveedor, contacto, telefono, email), fetch=False)

        flash('Proveedor registrado exitosamente', 'success')
        return redirect(url_for('listar_proveedores'))

    return render_template('registro_proveedor.html')

@app.route('/listar_proveedores')
def listar_proveedores():
    proveedores = execute_query('SELECT * FROM proveedores', fetch=True)
    return render_template('listar_proveedores.html', proveedores=proveedores)

@app.route('/editar_proveedor/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = execute_query('SELECT * FROM proveedores WHERE id = ?', (id,), fetch=True)
    if not proveedor:
        flash('Proveedor no encontrado', 'danger')
        return redirect(url_for('listar_proveedores'))

    if request.method == 'POST':
        nombre_proveedor = request.form['nombre_proveedor']
        contacto = request.form['contacto']
        telefono = request.form['telefono']
        email = request.form['email']

        execute_query('UPDATE proveedores SET nombre_proveedor = ?, contacto = ?, telefono = ?, email = ? WHERE id = ?',
                       (nombre_proveedor, contacto, telefono, email, id), fetch=False)
        flash('Proveedor actualizado exitosamente', 'success')
        return redirect(url_for('listar_proveedores'))

    return render_template('editar_proveedor.html', proveedor=proveedor[0])

@app.route('/eliminar_proveedor/<int:id>', methods=['POST'])
def eliminar_proveedor(id):
    proveedor = execute_query('SELECT * FROM proveedores WHERE id = ?', (id,), fetch=True)
    if not proveedor:
        flash('Proveedor no encontrado', 'danger')
        return redirect(url_for('listar_proveedores'))

    execute_query('DELETE FROM proveedores WHERE id = ?', (id,), fetch=False)
    flash('Proveedor eliminado exitosamente', 'success')
    return redirect(url_for('listar_proveedores'))


@app.route('/autenticacion', methods=['GET', 'POST'])
def autenticacion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = execute_query('SELECT * FROM Usuarios WHERE nombre_usuario = ?', (username,))
        if user is None:
            flash('El nombre de usuario no existe', 'danger')
        elif not check_password_hash(user[0][2], password):
            flash('La contraseña es incorrecta', 'danger')
        else:
            session['usuario_id'] = user[0][0]  
            session['user_roles'] = obtener_roles(user[0][0])          
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

        user = execute_query('SELECT * FROM Usuarios WHERE nombre_usuario = ?', (username,))
        if user:
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        try:
            execute_query('''INSERT INTO Usuarios (nombre_usuario, contrasena, rol, estatus)
                              VALUES (?, ?, 'Administrador', 'Activo')''', (username, hashed_password))
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('autenticacion'))
        except Exception as e:
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/gestion_devoluciones', methods=['GET', 'POST'])
@requiere_rol(['Administrador', 'Gerente', 'Empleado'])
def gestion_devoluciones():
    if request.method == 'POST':
        producto_id = request.form['producto']  
        motivo = request.form['motivo']
        cantidad = request.form['cantidad']

        execute_query("""
            INSERT INTO Devoluciones (producto_id, motivo, cantidad, fecha_devolucion)
            VALUES (?, ?, ?, GETDATE())
        """, (producto_id, motivo, cantidad))
        flash('Devolución registrada con éxito', 'success')
        return redirect(url_for('gestion_devoluciones'))

    devoluciones = execute_query("""
        SELECT devolucion_id, venta_id, producto_id, cantidad, fecha_devolucion, motivo
        FROM Devoluciones
    """)
    return render_template('gestion_devoluciones.html', devoluciones=devoluciones)

@app.route('/listar_devoluciones', methods=['GET'])
def listar_devoluciones():
    devoluciones = execute_query("""
        SELECT devolucion_id, venta_id, producto_id, cantidad, fecha_devolucion, motivo
        FROM Devoluciones
    """)
    return render_template('listar_devoluciones.html', devoluciones=devoluciones)

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

        execute_query("""INSERT INTO Empleados (nombre, apellido, email, telefono, direccion, fecha_contratacion, rol, estatus)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                       (nombre, apellido, email, telefono, direccion, fecha_contratacion, rol, estatus))

        flash('Empleado creado con éxito', 'success')
        return redirect(url_for('detalles_empleado')) 

    return render_template('crear_empleado.html')

@app.route('/empleados/detalles_empleado')
@requiere_rol(['Administrador', 'Gerente'])
def detalles_empleado():
    empleados = execute_query("SELECT empleado_id, nombre, apellido, email, telefono, rol, estatus FROM Empleados")
    return render_template('detalles_empleado.html', empleados=empleados)

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

        execute_query("""UPDATE Empleados
                          SET nombre = ?, apellido = ?, email = ?, telefono = ?, direccion = ?, fecha_contratacion = ?, rol = ?, estatus = ?
                          WHERE empleado_id = ?""",
                       (nombre, apellido, email, telefono, direccion, fecha_contratacion, rol, estatus, empleado_id))

        flash('Empleado actualizado con éxito', 'success')
        return redirect(url_for('detalles_empleado', empleado_id=empleado_id))

    empleado = execute_query("SELECT * FROM Empleados WHERE empleado_id = ?", (empleado_id,))
    return render_template('editar_empleado.html', empleado=empleado[0])

@app.route('/reporte/devoluciones')
def generar_reporte_devoluciones_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("Reporte de Devoluciones")

    fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.drawString(100, 800, "Reporte de Devoluciones - Servicentro Corazón de Jesús")
    pdf.drawString(100, 780, f"Fecha de Generación: {fecha_generacion}")

    devoluciones = execute_query("SELECT * FROM Devoluciones")

    y = 750
    for devolucion in devoluciones:
        pdf.drawString(100, y, f"Devolución ID: {devolucion.devolucion_id}, Producto ID: {devolucion.producto_id}, "
                                f"Cantidad: {devolucion.cantidad}, Fecha: {devolucion.fecha_devolucion}")
        y -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="reporte_devoluciones.pdf", mimetype='application/pdf')

def registrar_reporte(tipo_reporte, usuario_id):
    execute_query("""
        INSERT INTO Reportes (tipo_reporte, usuario_id)
        VALUES (?, ?)
    """, (tipo_reporte, usuario_id))

@app.route('/reporte/ventas')
def generar_reporte_ventas_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("Reporte de Ventas")

    fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.drawString(100, 800, "Reporte de Ventas - Servicentro Corazón de Jesús")
    pdf.drawString(100, 780, f"Fecha de Generación: {fecha_generacion}")

    ventas = execute_query("SELECT * FROM Ventas")

    y = 750
    for venta in ventas:
        pdf.drawString(100, y, f"Venta ID: {venta.venta_id}, Total: {venta.total}, Fecha: {venta.fecha_venta}")
        y -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    
    registrar_reporte("Ventas", usuario_id=session['usuario_id']) 

    return send_file(buffer, as_attachment=True, download_name="reporte_ventas.pdf", mimetype='application/pdf')

@app.route('/reporte/inventario')
def generar_reporte_inventario_pdf():
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("Reporte de Inventario")

    fecha_generacion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.drawString(100, 800, "Reporte de Inventario - Servicentro Corazón de Jesús")
    pdf.drawString(100, 780, f"Fecha de Generación: {fecha_generacion}")

    inventario = execute_query("SELECT * FROM Inventarios")

    y = 750
    for item in inventario:
        pdf.drawString(100, y, f"Producto ID: {item.producto_id}, Nombre: {item.nombre_producto}, Cantidad: {item.cantidad}")
        y -= 20

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    
    registrar_reporte("Inventario", usuario_id=session['usuario_id']) 
    return send_file(buffer, as_attachment=True, download_name="reporte_inventario.pdf", mimetype='application/pdf')

@app.route('/reportes')
def seleccion_reportes():
    return render_template('seleccion_reportes.html')

@app.route('/programar_cita', methods=['GET', 'POST'])
def programar_cita():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        tipo_servicio = request.form['tipo_servicio']
        descripcion = request.form['descripcion']
        fecha_servicio_str = request.form['fecha_servicio']
        cliente_nombre = request.form['cliente_nombre']
        cliente_telefono = request.form['cliente_telefono']
        cliente_email = request.form['cliente_email']

        # Convertir la fecha desde el formato string a datetime
        try:
            fecha_servicio = datetime.strptime(fecha_servicio_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash("La fecha proporcionada no es válida. Intente nuevamente.", 'error')
            return redirect(url_for('programar_cita'))

        # Verificar disponibilidad
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Citas 
            WHERE tipo_servicio = ? AND fecha_servicio = ?;
        """, (tipo_servicio, fecha_servicio))
        disponibilidad = cursor.fetchone()[0]

        if disponibilidad > 0:
            flash('Ya existe una cita programada para ese horario.', 'error')
            return redirect(url_for('programar_cita'))

        # Registrar cita con los datos del cliente
        cursor.execute("""
            INSERT INTO Citas (tipo_servicio, descripcion, fecha_servicio, cliente_nombre, cliente_telefono, cliente_email) 
            VALUES (?, ?, ?, ?, ?, ?);
        """, (tipo_servicio, descripcion, fecha_servicio, cliente_nombre, cliente_telefono, cliente_email))
        conn.commit()

        flash('Cita programada exitosamente.', 'success')
        return redirect(url_for('consultar_citas'))

    cursor.close()
    conn.close()
    return render_template('programar_cita.html')

@app.route('/consultar_citas', methods=['GET'])
def consultar_citas():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener todas las citas programadas
    cursor.execute("""
        SELECT cita_id, tipo_servicio, descripcion, fecha_servicio, estado, cliente_nombre, cliente_telefono, cliente_email
        FROM Citas
        ORDER BY fecha_servicio;
    """)
    citas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('consultar_citas.html', citas=citas)

if __name__ == '__main__':
    app.run(debug=True)