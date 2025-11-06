"""
URL configuration for blessedBarbershop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from blessedApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'), 
    path('login/', login, name='login'),
    path('panelAdmin/', panel_admin, name='panel_admin'),
    path('panelBarbero/', panel_barbero, name='panel_barbero'),
    path('panelCliente/', panel_cliente, name='panel_cliente'),

    # Rutas para Roles (se añadió la ruta de detalle: verRol)
    path('verRoles/', mostrarRoles, name='verRoles'),
    path('crearRol/', crearRol, name='crearRol'),
    path('verRol/<int:id>/', Rol, name='verRol'), 
    path('editarRol/<int:id>/', editarRol, name='editarRol'),
    path('eliminarRol/<int:id>/', eliminarRol, name='eliminarRol'),

    # Rutas para Servicios (se añadió la ruta de detalle: verServicio)
    path('verServicios/', mostrarServicios, name='verServicios'),
    path('crearServicio/', crearServicio, name='crearServicio'),
    path('verServicio/<int:id>/', Servicio, name='verServicio'), 
    path('editarServicio/<int:id>/', editarServicio, name='editarServicio'),
    path('eliminarServicio/<int:id>/', eliminarServicio, name='eliminarServicio'),

    # Rutas para Usuarios (se añadió la ruta de detalle: verUsuario)
    path('verUsuarios/', mostrarUsuarios, name='verUsuarios'),
    path('crearUsuario/', crearUsuario, name='crearUsuario'),
    path('verUsuario/<int:id>/', Usuario, name='verUsuario'),
    path('editarUsuario/<int:id>/', editarUsuario, name='editarUsuario'),
    path('eliminarUsuario/<int:id>/', eliminarUsuario, name='eliminarUsuario'),

    # Rutas para Disponibilidades (se añadió la ruta de detalle: verDisponibilidad)
    path('verDisponibilidades/', mostrarDisponibilidades, name='verDisponibilidades'),
    path('crearDisponibilidad/', crearDisponibilidad, name='crearDisponibilidad'),
    path('verDisponibilidad/<int:id>/', Disponibilidad, name='verDisponibilidad'), 
    path('editarDisponibilidad/<int:id>/', editarDisponibilidad, name='editarDisponibilidad'),
    path('eliminarDisponibilidad/<int:id>/', eliminarDisponibilidad, name='eliminarDisponibilidad'),

    # Rutas para Reservas (se añadió la ruta de detalle: verReserva)
    path('verReservas/', mostrarReservas, name='verReservas'),
    path('crearReserva/', crearReserva, name='crearReserva'),
    path('verReserva/<int:id>/', Reserva, name='verReserva'), 
    path('editarReserva/<int:id>/', editarReserva, name='editarReserva'),
    path('eliminarReserva/<int:id>/', eliminarReserva, name='eliminarReserva'),

    # Rutas para Estados (se añadió la ruta de detalle: verEstado)
    path('verEstados/', mostrarEstados, name='verEstados'),
    path('crearEstado/', crearEstado, name='crearEstado'),
    path('verEstado/<int:id>/', Estado, name='verEstado'), 
    path('editarEstado/<int:id>/', editarEstado, name='editarEstado'),
    path('eliminarEstado/<int:id>/', eliminarEstado, name='eliminarEstado'),

    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
]
