from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'f6d7d98e9a2b7f4a35f4b5e7d6a7c8e9'

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

@app.route('/autenticacion')
def autentificacion():
    return render_template('autentificacion.html')

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

@app.route('/empleados/evaluar_desempeno', methods=['GET', 'POST'])
def evaluar_desempeno():
    if request.method == 'POST':
        return render_template('evaluar_desempeno.html', mensaje='Evaluación de desempeño completada exitosamente.')
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

@app.route('/tienda/reportes_financieros', methods=['GET', 'POST'])
def reportes_financieros():
    if request.method == 'POST':
        mes = request.form.get('mes')
        formato = request.form.get('formato')

        if not mes or not formato:
            flash('Por favor seleccione un mes y un formato.', 'error')
            return redirect(url_for('reportes_financieros'))

        flash('Reporte generado exitosamente.', 'success')
        return redirect(url_for('reportes_financieros'))

    return render_template('reportes_financieros.html')

@app.route('/tienda/gestion_productos')
def gestion_productos():
    return render_template('gestion_productos.html')

@app.route('/tienda/registro_producto', methods=['GET', 'POST'])
def registro_producto():
    if request.method == 'POST':
        nombre_producto = request.form.get('nombre_producto')
        cantidad = request.form.get('cantidad')
        precio = request.form.get('precio')

        if not nombre_producto or not cantidad or not precio:
            error = "Todos los campos son obligatorios."
            return render_template('registro_producto.html', error=error)

        success = "Producto registrado exitosamente."
        return render_template('registro_producto.html', success=success)

    return render_template('registro_producto.html')

@app.route('/tienda/registro_proveedor', methods=['GET', 'POST'])
def registro_proveedor():
    if request.method == 'POST':
        nombre_proveedor = request.form.get('nombre_proveedor')
        contacto = request.form.get('contacto')
        productos_suministrados = request.form.get('productos_suministrados')

        proveedor_existente = False  

        if proveedor_existente:
            error = "Error: el proveedor ya está registrado."
            return render_template('registro_proveedor.html', error=error)

        if not nombre_proveedor or not contacto or not productos_suministrados:
            error = "Todos los campos son obligatorios."
            return render_template('registro_proveedor.html', error=error)

        success = "Proveedor registrado exitosamente."
        return render_template('registro_proveedor.html', success=success)

    return render_template('registro_proveedor.html')

@app.route('/tienda/crear_promocion', methods=['GET', 'POST'])
def crear_promocion():
    if request.method == 'POST':
        nombre_promocion = request.form.get('nombre_promocion')
        producto = request.form.get('producto')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        descuento = request.form.get('descuento')

        if fecha_inicio > fecha_fin:
            error = "Error: Las fechas de la promoción son inválidas."
            return render_template('crear_promocion.html', error=error)

        error_de_servidor = False  

        if error_de_servidor:
            error = "Error del servidor. Por favor, inténtelo de nuevo más tarde."
            return render_template('crear_promocion.html', error=error)

        success = "Promoción creada exitosamente."
        return render_template('crear_promocion.html', success=success)

    return render_template('crear_promocion.html')

@app.route('/tienda/actualizar_precio_producto', methods=['GET', 'POST'])
def actualizar_precio_producto():
    if request.method == 'POST':
        nombre_producto = request.form.get('nombre_producto')
        nuevo_precio = request.form.get('nuevo_precio')

        if not nombre_producto or not nuevo_precio:
            error = "Todos los campos son obligatorios."
            return render_template('actualizar_precio_producto.html', error=error)

        try:
            nuevo_precio = float(nuevo_precio)
            if nuevo_precio < 0:
                raise ValueError("El precio no puede ser negativo.")
        except ValueError as e:
            error = f"Error: Precio inválido. {str(e)}"
            return render_template('actualizar_precio_producto.html', error=error)

        success = "Precio actualizado exitosamente."
        return render_template('actualizar_precio_producto.html', success=success)

    return render_template('actualizar_precio_producto.html')

@app.route('/tienda/gestion_devoluciones', methods=['GET', 'POST'])
def gestion_devoluciones():
    if request.method == 'POST':
        producto = request.form.get('producto')
        motivo = request.form.get('motivo')
        cantidad = request.form.get('cantidad')

        if not producto or not motivo or not cantidad:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('gestion_devoluciones'))

        razones_validas = ["Producto defectuoso", "Fecha de caducidad cercana", "Otro"]
        if motivo not in razones_validas:
            flash('Error: Razón de devolución no válida', 'error')
            return redirect(url_for('gestion_devoluciones'))


        try:

            flash('Devolución registrada exitosamente.', 'success')
        except:
            flash('Error del servidor. Por favor, inténtelo de nuevo más tarde.', 'error')
        
        return redirect(url_for('gestion_devoluciones'))

    return render_template('gestion_devoluciones.html')

##################################


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/ADT')
def ADT():
    return render_template('adt_index.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')

@app.route('/emisiones')
def emisiones():
    return render_template('emisiones.html')

@app.route('/configurar_alertas')
def configurar_alertas():
    return render_template('configurar_alertas.html')

if __name__ == '__main__':
    app.run(debug=True)
