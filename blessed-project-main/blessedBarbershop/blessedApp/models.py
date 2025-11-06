from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class Estado(models.Model):
    estado = models.CharField(max_length=25)

    def __str__(self):
        return self.estado


class Servicio(models.Model):
    servicio = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()

    def __str__(self):
        return self.servicio


class Rol(models.Model):
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.rol


class Usuario(models.Model):
    usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField()
    telefono = models.IntegerField()
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Solo hashea la contraseña si no está ya hasheada
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.usuario


class Disponibilidad(models.Model):
    barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='disponibilidades')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.barbero.usuario} - {self.fecha} ({self.hora_inicio} - {self.hora_fin})"


class Reserva(models.Model):
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cliente')
    barbero = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='barbero')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def clean(self):
        """Valida que el barbero esté disponible en ese horario."""
        if not self.barbero_id or not self.fecha or not self.hora_inicio or not self.hora_fin:
            return  # Evita validar si faltan datos

        disponibilidad = Disponibilidad.objects.filter(
            barbero=self.barbero,
            fecha=self.fecha,
            hora_inicio__lte=self.hora_inicio,
            hora_fin__gte=self.hora_fin,
            disponible=True
        ).first()

        if not disponibilidad:
            raise ValidationError("El barbero no está disponible en el horario seleccionado.")

    def save(self, *args, **kwargs):
        """Guarda la reserva y gestiona la disponibilidad automáticamente."""
        self.clean()

        # Detectar si ya existía antes (para saber si se está editando)
        reserva_existente = None
        if self.pk:
            reserva_existente = Reserva.objects.filter(pk=self.pk).first()

        super().save(*args, **kwargs)

        #  Si la reserva es nueva o su horario cambió → actualizar disponibilidad
        if not reserva_existente or (
            reserva_existente.hora_inicio != self.hora_inicio or 
            reserva_existente.hora_fin != self.hora_fin
        ):
            disponibilidad = Disponibilidad.objects.filter(
                barbero=self.barbero,
                fecha=self.fecha,
                hora_inicio__lte=self.hora_inicio,
                hora_fin__gte=self.hora_fin,
                disponible=True
            ).first()

            if disponibilidad:
                original_inicio = disponibilidad.hora_inicio
                original_fin = disponibilidad.hora_fin
                disponibilidad.delete()

                # Antes del tramo reservado
                if self.hora_inicio > original_inicio:
                    Disponibilidad.objects.create(
                        barbero=self.barbero,
                        fecha=self.fecha,
                        hora_inicio=original_inicio,
                        hora_fin=self.hora_inicio,
                        disponible=True
                    )

                # Después del tramo reservado
                if self.hora_fin < original_fin:
                    Disponibilidad.objects.create(
                        barbero=self.barbero,
                        fecha=self.fecha,
                        hora_inicio=self.hora_fin,
                        hora_fin=original_fin,
                        disponible=True
                    )

        #  Si la reserva pasa a "Finalizado" → liberar la franja horaria
        if self.estado.estado.lower() == "finalizado":
            self.liberar_disponibilidad()

    def liberar_disponibilidad(self):
        """Libera el horario reservado creando un nuevo bloque de disponibilidad."""
        # Evita duplicados: solo crea si no hay disponibilidad igual
        existe = Disponibilidad.objects.filter(
            barbero=self.barbero,
            fecha=self.fecha,
            hora_inicio=self.hora_inicio,
            hora_fin=self.hora_fin
        ).exists()

        if not existe:
            Disponibilidad.objects.create(
                barbero=self.barbero,
                fecha=self.fecha,
                hora_inicio=self.hora_inicio,
                hora_fin=self.hora_fin,
                disponible=True
            )

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.usuario} con {self.barbero.usuario}"
