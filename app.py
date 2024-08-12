from flask import Flask, render_template, request, redirect, url_for

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

# EMP

@app.route('/EMP')
def EMP():
    return render_template('emp_index.html')

# EMP

@app.route('/EMP')
def EMP():
    return render_template('emp_index.html')

@app.route('/empleados')
def empleados():
    return render_template('empleados.html')

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

@app.route('/empleados/revision_nomina/pdf')
def revision_nomina_pdf():
    return render_template('revision_nomina_pdf.html')

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


###############################################################

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

@app.route('/configurar_alertas')
def configurar_alertas():
    return render_template('configurar_alertas.html')

if __name__ == '__main__':
    app.run(debug=True)
    