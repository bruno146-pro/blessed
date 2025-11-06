from . import forms
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario
from .decorators import rol_requerido

from django.http import HttpResponseRedirect
from django.urls import reverse

from blessedApp.models import *
from blessedApp.forms import *
# La siguiente línea está duplicada en tu código original, la mantengo si la necesitas:
# from .forms import RolForm


# --- VISTAS DE AUTENTICACIÓN Y PANELES ---

def login(request):
    """Maneja el inicio de sesión y redirecciona según el rol."""
    if request.method == 'POST':
        nombre_usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(usuario=nombre_usuario)
        except Usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            # Asegúrate de que tu template login.html esté en la ruta correcta
            return render(request, 'registration/login.html') 

        # Comparación de contraseñas (usando check_password de Django)
        if check_password(password, usuario.password):
            # Guardar datos de sesión
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.usuario
            request.session['rol'] = usuario.rol.rol

            # Redirección según rol
            if usuario.rol.rol.lower() == 'administrador':
                return redirect('panel_admin')
            elif usuario.rol.rol.lower() == 'barbero':
                return redirect('panel_barbero')
            else:
                return redirect('panel_cliente')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return render(request, 'registration/login.html') 
            
    # Si es GET, muestra el formulario de login.
    # He corregido la ruta del template a 'login.html' ya que lo subiste ahí,
    # en lugar de 'registration/login.html'.
    return render(request, 'registration/login.html')


@rol_requerido(['Administrador'])
def panel_admin(request):
    """Panel para el rol Administrador."""
    return render(request, 'panel_admin.html')

@rol_requerido(['Barbero'])
def panel_barbero(request):
    """Panel para el rol Barbero (aún no definido)."""
    # Puedes añadir lógica aquí para mostrar sólo sus reservas
    return render(request, 'panel_barbero.html')

@rol_requerido(['Cliente'])
def panel_cliente(request):
    """Panel para el rol Cliente."""
    # Puedes añadir lógica aquí para mostrar sus propias reservas
    return render(request, 'panel_cliente.html')

# --- VISTAS CRUD DE ROLES ---

@rol_requerido(['Administrador'])
def mostrarRoles(request):
    roles = Rol.objects.all()
    data = {
        'roles': roles,
        'titulo': 'Roles Disponibles'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render (request, 'ver_roles.html',data)

@rol_requerido(['Administrador'])
def crearRol(request):
    formRol = RolForm()

    if request.method == 'POST':
        formRol = RolForm(request.POST)
        if formRol.is_valid():
            print("Formulario válido")
            formRol.save()
            return HttpResponseRedirect(reverse('verRoles'))
    data = {
        'formRol': formRol,
        'titulo': 'Crear Rol'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_roles.html', data)
    
@rol_requerido(['Administrador'])
def editarRol(request, id):
    rol = Rol.objects.get(id=id)
    formRol = RolForm(instance=rol)
    if (request.method == 'POST'):
        formRol = RolForm(request.POST, instance=rol)
        if formRol.is_valid():
            print("Formulario válido")
            formRol.save()
            return HttpResponseRedirect(reverse('verRoles'))
        else:
            print("Formulario inválido", formRol.errors)
    data = {
        'formRol': formRol,
        'titulo': 'Editar Rol'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_roles.html', data)

@rol_requerido(['Administrador'])
def eliminarRol(request, id):
    rol = Rol.objects.get(id=id)
    rol.delete()
    return HttpResponseRedirect(reverse('verRoles'))
            
# --- VISTAS CRUD DE SERVICIOS ---

@rol_requerido(['Administrador'])
def mostrarServicios(request):
    servicios = Servicio.objects.all()
    data = {
        'servicios': servicios,
        'titulo': 'Servicios Disponibles'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render (request, 'ver_servicios.html',data)

@rol_requerido(['Administrador'])
def crearServicio(request):
    servicioForm = ServicioForm()

    if request.method == 'POST':
        servicioForm = ServicioForm(request.POST)
        if servicioForm.is_valid():
            print("Formulario válido")
            servicioForm.save()
            return HttpResponseRedirect(reverse('verServicios'))
    data = {
        'servicioForm': servicioForm,
        'titulo': 'Crear Servicio'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_servicios.html', data)

@rol_requerido(['Administrador'])
def editarServicio(request, id):
    servicio = Servicio.objects.get(id=id)
    servicioForm = ServicioForm(instance=servicio)
    if (request.method == 'POST'):
        servicioForm = ServicioForm(request.POST, instance=servicio)
        if servicioForm.is_valid():
            print("Formulario válido")
            servicioForm.save()
            return HttpResponseRedirect(reverse('verServicios'))
        else:
            print("Formulario inválido", servicioForm.errors)
    data = {
        'servicioForm': servicioForm,
        'titulo': 'Editar Servicio'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_servicios.html', data)

@rol_requerido(['Administrador'])
def eliminarServicio(request, id):
    servicio = Servicio.objects.get(id=id)
    servicio.delete()
    return HttpResponseRedirect(reverse('verServicios'))

# --- VISTAS CRUD DE USUARIOS ---

@rol_requerido(['Administrador'])
def mostrarUsuarios(request):
    usuarios = Usuario.objects.all()
    data = {
        'usuarios': usuarios,
        'titulo': 'Usuarios Disponibles'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render (request, 'ver_usuarios.html',data)

# Nota: La vista 'crearUsuario' fue modificada en nuestra conversación anterior
# para manejar el registro de clientes. Aquí la mantienes genérica para uso de Admin.

@rol_requerido(['Administrador'])
def crearUsuario(request):
    usuarioForm = UsuarioForm()

    if request.method == 'POST':
        usuarioForm = UsuarioForm(request.POST)
        if usuarioForm.is_valid():
            print("Formulario válido")
            usuarioForm.save() # La función save del modelo Usuario hashea la contraseña
            return HttpResponseRedirect(reverse('verUsuarios'))
    data = {
        'usuarioForm': usuarioForm,
        'titulo': 'Crear Usuario'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_usuarios.html', data)

@rol_requerido(['Administrador'])
def editarUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    # Importante: al editar, la contraseña no debe mostrarse ni forzarse a hashearse de nuevo si no se cambia.
    # Aquí uso la instancia original.
    usuarioForm = UsuarioForm(instance=usuario) 
    if (request.method == 'POST'):
        # Aquí deberías manejar la contraseña cuidadosamente si se permite editar,
        # para no hashear una contraseña ya hasheada si el campo queda vacío.
        usuarioForm = UsuarioForm(request.POST, instance=usuario)
        if usuarioForm.is_valid():
            print("Formulario válido")
            usuarioForm.save()
            return HttpResponseRedirect(reverse('verUsuarios'))
        else:
            print("Formulario inválido", usuarioForm.errors)
    data = {
        'usuarioForm': usuarioForm,
        'titulo': 'Editar Usuario'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_usuarios.html', data)

@rol_requerido(['Administrador'])
def eliminarUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return HttpResponseRedirect(reverse('verUsuarios'))


# --- VISTAS CRUD DE DISPONIBILIDADES ---

@rol_requerido(['Administrador', 'Barbero']) # Asumo que el barbero también puede ver/editar
def mostrarDisponibilidades(request):
    disponibilidades = Disponibilidad.objects.all()
    # Si es Barbero, filtrar por su ID
    if request.session.get('rol', '').lower() == 'barbero':
        disponibilidades = disponibilidades.filter(barbero_id=request.session.get('usuario_id'))

    data = {
        'disponibilidades': disponibilidades,
        'titulo': 'Disponibilidades Disponibles'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render (request, 'ver_disponibilidades.html',data)

@rol_requerido(['Administrador', 'Barbero'])
def crearDisponibilidad(request):
    disponibilidadForm = DisponibilidadForm()

    if request.method == 'POST':
        disponibilidadForm = DisponibilidadForm(request.POST)
        if disponibilidadForm.is_valid():
            print("Formulario válido")
            disponibilidadForm.save()
            return HttpResponseRedirect(reverse('verDisponibilidades'))
    data = {
        'disponibilidadForm': disponibilidadForm,
        'titulo': 'Crear Disponbilidad'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_disponibilidades.html', data)

@rol_requerido(['Administrador', 'Barbero'])
def editarDisponibilidad(request, id):
    disponibilidad = Disponibilidad.objects.get(id=id)
    disponibilidadForm = DisponibilidadForm(instance=disponibilidad) 
    if (request.method == 'POST'):
        disponibilidadForm = DisponibilidadForm(request.POST, instance=disponibilidad)
        if disponibilidadForm.is_valid():
            print("Formulario válido")
            disponibilidadForm.save()
            return HttpResponseRedirect(reverse('verDisponibilidades'))
        else:
            print("Formulario inválido", disponibilidadForm.errors)
    data = {
        'disponibilidadForm': disponibilidadForm,
        'titulo': 'Editar Disponibilidad'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_disponibilidades.html', data)

@rol_requerido(['Administrador', 'Barbero'])
def eliminarDisponibilidad(request, id):
    disponibilidad = Disponibilidad.objects.get(id=id)
    disponibilidad.delete()
    return HttpResponseRedirect(reverse('verDisponibilidades'))


# --- VISTAS CRUD DE RESERVAS ---

@rol_requerido(['Administrador', 'Barbero']) 
def mostrarReservas(request):
    reservas = Reserva.objects.all()
    # Si es Barbero, filtrar solo sus reservas
    if request.session.get('rol', '').lower() == 'barbero':
        reservas = reservas.filter(barbero_id=request.session.get('usuario_id'))

    data = {
        'reservas': reservas,
        'titulo': 'Reservas Disponibles'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render (request, 'ver_reservas.html',data)

@rol_requerido(['Cliente']) # Solo los clientes crean reservas (o el Admin desde su panel, pero este es el flujo de cliente)
def crearReserva(request):
    usuario_id = request.session.get('usuario_id')
    # Este check ya está manejado por @rol_requerido(['Cliente']), pero lo dejo para el mensaje explícito.
    if not usuario_id:
        messages.error(request, "Debe iniciar sesión para crear una reserva.")
        return redirect('login')

    cliente = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        # La forma ReservaForm está definida para no pedir 'cliente' ni 'estado' por defecto
        # en tu forms.py (si no está en modo 'editar').
        reservaForm = ReservaForm(request.POST) 
        if reservaForm.is_valid():
            reserva = reservaForm.save(commit=False)
            reserva.cliente = cliente

            # 🔹 Verificar disponibilidad del barbero en la hora seleccionada
            # Busca si hay UN BLOQUE DISPONIBLE que cubra la hora de inicio de la reserva
            disponibilidad_bloque = Disponibilidad.objects.filter(
                barbero=reserva.barbero,
                fecha=reserva.fecha,
                hora_inicio__lte=reserva.hora_inicio,
                hora_fin__gte=reserva.hora_inicio,
                disponible=True
            ).first()

            if not disponibilidad_bloque:
                messages.error(request, "⚠️ El barbero no tiene disponibilidad para esa fecha y hora.")
                data = {
                    'reservaForm': reservaForm,
                    'titulo': 'Crear Reserva'
                }
                return render(request, 'crear_reservas.html', data)

            # 🔹 Asignar estado "Pendiente" automáticamente
            estado_pendiente, _ = Estado.objects.get_or_create(estado="Pendiente")
            reserva.estado = estado_pendiente

            reserva.save()
            messages.success(request, "✅ Reserva creada exitosamente. Esperando aprobación.")
            return HttpResponseRedirect(reverse('panel_cliente')) # Redirigir al panel del cliente
        else:
            print(reservaForm.errors)
    else:
        reservaForm = ReservaForm()

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Crear Reserva'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_reservas.html', data)

@rol_requerido(['Administrador', 'Barbero']) 
def editarReserva(request, id):
    reserva = get_object_or_404(Reserva, id=id) # Usar get_object_or_404 por buena práctica
    
    # Solo si el usuario es un Barbero, asegurar que solo edite sus propias reservas
    if request.session.get('rol', '').lower() == 'barbero' and reserva.barbero_id != request.session.get('usuario_id'):
        messages.error(request, "No tienes permiso para editar esta reserva.")
        return redirect('verReservas')

    reservaForm = ReservaForm(instance=reserva, editar=True)

    if request.method == 'POST':
        reservaForm = ReservaForm(request.POST, instance=reserva, editar=True)
        if reservaForm.is_valid():
            print("Formulario válido")
            reserva_actualizada = reservaForm.save(commit=False)

            # Lógica para liberar disponibilidad si el estado cambia a 'Finalizado' o 'Cancelado'
            estado_finalizado = Estado.objects.filter(estado__iexact="Finalizado").first()
            estado_cancelado = Estado.objects.filter(estado__iexact="Cancelado").first()
            
            # Solo si el nuevo estado es Finalizado O Cancelado.
            if estado_finalizado and reserva_actualizada.estado == estado_finalizado or \
               estado_cancelado and reserva_actualizada.estado == estado_cancelado:
                
                # 🔓 Liberar disponibilidad (creando un nuevo bloque si es necesario)
                # Esta lógica debería ser manejada en el método save() del modelo Reserva,
                # pero si no lo está, se hace aquí:
                try:
                    reserva_actualizada.liberar_disponibilidad() # Asumiendo que esta función existe en Reserva
                except:
                     # Fallback si el método no existe o falla, solo marcar como disponible en Disponibilidad
                     Disponibilidad.objects.filter(
                         barbero=reserva_actualizada.barbero,
                         fecha=reserva_actualizada.fecha,
                         hora_inicio__lte=reserva_actualizada.hora_fin, # Esto es una aproximación simple
                         hora_fin__gte=reserva_actualizada.hora_inicio
                     ).update(disponible=True)

                print("✅ Disponibilidad liberada.")
            
            reserva_actualizada.save()
            return HttpResponseRedirect(reverse('verReservas'))
        else:
            print("Formulario inválido", reservaForm.errors)

    data = {
        'reservaForm': reservaForm,
        'titulo': 'Editar Reserva'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_reservas.html', data)

@rol_requerido(['Administrador'])
def eliminarReserva(request, id):
    reserva = get_object_or_404(Reserva, id=id) 
    # Antes de eliminar, liberar disponibilidad
    try:
        reserva.liberar_disponibilidad()
    except:
        pass # Si falla la liberación (p.ej. ya se liberó), no se detiene la eliminación
    
    reserva.delete()
    return HttpResponseRedirect(reverse('verReservas'))


# --- VISTAS CRUD DE ESTADOS ---

@rol_requerido(['Administrador'])
def mostrarEstados(request):
    estados = Estado.objects.all()
    data = {
        'estados': estados,
        'titulo': 'Estados Disponibles'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render (request, 'ver_estados.html',data)

@rol_requerido(['Administrador'])
def crearEstado(request):
    estadoForm = EstadoForm()

    if request.method == 'POST':
        estadoForm = EstadoForm(request.POST)
        if estadoForm.is_valid():
            print("Formulario válido")
            estadoForm.save()
            return HttpResponseRedirect(reverse('verEstados'))
    data = {
        'estadoForm': estadoForm,
        'titulo': 'Crear Estado'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_estados.html', data)
    
@rol_requerido(['Administrador'])
def editarEstado(request, id):
    estado = Estado.objects.get(id=id)
    estadoForm = EstadoForm(instance=estado)
    if (request.method == 'POST'):
        estadoForm = EstadoForm(request.POST, instance=estado)
        if estadoForm.is_valid():
            print("Formulario válido")
            estadoForm.save()
            return HttpResponseRedirect(reverse('verEstados'))
        else:
            print("Formulario inválido", estadoForm.errors)
    data = {
        'estadoForm': estadoForm,
        'titulo': 'Editar Estado'
    }
    # He corregido la ruta del template quitando 'blessedApp/'
    return render(request, 'crear_estados.html', data)

@rol_requerido(['Administrador'])
def eliminarEstado(request, id):
    estado = Estado.objects.get(id=id)
    estado.delete()
    return HttpResponseRedirect(reverse('verEstados'))


# --- VISTAS ADICIONALES ---

def cerrar_sesion(request):
    """Cierra la sesión del usuario y lo redirige al login con un mensaje."""
    request.session.flush() # Elimina todos los datos de la sesión actual
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')