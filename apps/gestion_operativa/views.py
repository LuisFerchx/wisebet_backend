from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import date, timedelta
import pytz

from .models import (
    Distribuidora,
    CasaApuestas,
    Ubicacion,
    Agencia,
    PerfilOperativo,
    ConfiguracionOperativa,
    TransaccionFinanciera,
    PlanificacionRotacion,
    AlertaOperativa,
    BitacoraMando,
    Operacion,
    Deporte,
    Pais,
    ProvinciaEstado,
    Ciudad,
    Persona,
    ObjetivoCreacionPerfiles,
)
from .serializers import (
    DistribuidoraSerializer,
    DistribuidoraExpandedSerializer,
    CasaApuestasSerializer,
    CasaApuestasCreateSerializer,
    UbicacionSerializer,
    AgenciaSerializer,
    PerfilOperativoSerializer,
    ConfiguracionOperativaSerializer,
    TransaccionFinancieraSerializer,
    PlanificacionRotacionSerializer,
    AlertaOperativaSerializer,
    BitacoraMandoSerializer,
    OperacionSerializer,
    DeporteSerializer,
    PaisSerializer,
    ProvinciaEstadoSerializer,
    CiudadSerializer,
    PersonaSerializer,
    ObjetivoCreacionPerfilesSerializer,
)


# ============================================================================
# PAGINATION CLASSES
# ============================================================================


class StandardPagination(PageNumberPagination):
    """Paginación estándar para listas."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# ============================================================================
# CATALOGOS VIEWSETS
# ============================================================================


class DeporteViewSet(viewsets.ModelViewSet):
    queryset = Deporte.objects.all()
    serializer_class = DeporteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination


class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination


class ProvinciaEstadoViewSet(viewsets.ModelViewSet):
    queryset = ProvinciaEstado.objects.select_related("pais").all()
    serializer_class = ProvinciaEstadoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        pais_id = self.request.query_params.get("pais")
        if pais_id:
            queryset = queryset.filter(pais_id=pais_id)
        return queryset


class CiudadViewSet(viewsets.ModelViewSet):
    queryset = Ciudad.objects.select_related("provincia__pais").all()
    serializer_class = CiudadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        provincia_id = self.request.query_params.get("provincia")
        if provincia_id:
            queryset = queryset.filter(provincia_id=provincia_id)
        return queryset


class PersonaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Personas.
    """

    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        """Permite filtrar por documento si es necesario"""
        queryset = super().get_queryset()
        doc = self.request.query_params.get("documento")
        if doc:
            queryset = queryset.filter(numero_documento__icontains=doc)
        return queryset.order_by("primer_apellido")


# ============================================================================
# DISTRIBUIDORAS VIEWSET
# ============================================================================


class DistribuidoraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Distribuidoras (Flotas).

    Soporta:
    - `?expand=casas`: Incluye las casas anidadas
    - Paginación automática
    - Optimización de queries con prefetch_related
    """

    queryset = Distribuidora.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read without auth
    pagination_class = StandardPagination

    def get_queryset(self):
        """Optimiza queries según el parámetro expand."""
        queryset = super().get_queryset()
        expand = self.request.query_params.get("expand", "")

        if "casas" in expand:
            queryset = queryset.prefetch_related("casas")

        return queryset.order_by("nombre")

    def get_serializer_class(self):
        """Retorna serializer expandido si se solicita."""
        expand = self.request.query_params.get("expand", "")

        if "casas" in expand:
            return DistribuidoraExpandedSerializer
        return DistribuidoraSerializer


# ============================================================================
# CASAS DE APUESTAS VIEWSET
# ============================================================================


class CasaApuestasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Casas de Apuestas.

    Soporta:
    - `?distribuidora=ID`: Filtra por distribuidora
    - Paginación automática
    """

    queryset = CasaApuestas.objects.select_related("distribuidora").all()
    serializer_class = CasaApuestasSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow read without auth
    pagination_class = StandardPagination

    def get_serializer_class(self):
        """Usa serializer diferente para creación vs edición."""
        if self.action == "create":
            return CasaApuestasCreateSerializer
        return CasaApuestasSerializer

    def get_queryset(self):
        """Filtra por distribuidora si se especifica."""
        queryset = super().get_queryset()
        distribuidora_id = self.request.query_params.get("distribuidora")

        if distribuidora_id:
            queryset = queryset.filter(distribuidora_id=distribuidora_id)

        return queryset.order_by("nombre")

    def perform_create(self, serializer):
        """Asigna distribuidora desde body o query; valida si falta en ambos."""
        distribuidora_id_body = serializer.validated_data.get("distribuidora")
        distribuidora_id_query = self.request.query_params.get("distribuidora")

        # Prioridad: body > query param
        if distribuidora_id_body:
            serializer.save()
            return

        if distribuidora_id_query:
            serializer.save(distribuidora_id=distribuidora_id_query)
            return

        raise serializers.ValidationError(
            {"distribuidora": "Debe enviarse en el body o como query param ?distribuidora=ID."}
        )


# ============================================================================
# UBICACIONES VIEWSET
# ============================================================================


class UbicacionViewSet(viewsets.ModelViewSet):
    """ViewSet para Ubicaciones normalizadas."""

    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination


# ============================================================================
# AGENCIAS VIEWSET
# ============================================================================


class AgenciaViewSet(viewsets.ModelViewSet):
    """ViewSet para Agencias con ubicación y casa madre."""

    queryset = Agencia.objects.select_related("ubicacion", "casa_madre").all()
    serializer_class = AgenciaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# OPERACIONES VIEWSET
# ============================================================================


class OperacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Operaciones/Apuestas.

    Soporta:
    - `?perfil=ID`: Filtra por perfil
    """

    queryset = Operacion.objects.select_related("perfil").all()
    serializer_class = OperacionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        """Filtra por perfil si se especifica."""
        queryset = super().get_queryset()
        perfil_id = self.request.query_params.get("perfil")

        if perfil_id:
            queryset = queryset.filter(perfil_id=perfil_id)

        return queryset


# ============================================================================
# PERFILES OPERATIVOS VIEWSET
# ============================================================================


class PerfilOperativoViewSet(viewsets.ModelViewSet):
    queryset = PerfilOperativo.objects.select_related(
        "usuario", "agencia__casa_madre"
    ).all()
    serializer_class = PerfilOperativoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# CONFIGURACIÓN OPERATIVA VIEWSET
# ============================================================================


class ConfiguracionOperativaViewSet(viewsets.ModelViewSet):
    queryset = ConfiguracionOperativa.objects.all()
    serializer_class = ConfiguracionOperativaSerializer
    permission_classes = [IsAuthenticated]


# ============================================================================
# TRANSACCIONES FINANCIERAS VIEWSET
# ============================================================================


class TransaccionFinancieraViewSet(viewsets.ModelViewSet):
    queryset = TransaccionFinanciera.objects.select_related("perfil").all()
    serializer_class = TransaccionFinancieraSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# PLANIFICACIÓN ROTACIÓN VIEWSET
# ============================================================================


class PlanificacionRotacionViewSet(viewsets.ModelViewSet):
    queryset = PlanificacionRotacion.objects.select_related("perfil").all()
    serializer_class = PlanificacionRotacionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# ALERTAS OPERATIVAS VIEWSET
# ============================================================================


class AlertaOperativaViewSet(viewsets.ModelViewSet):
    queryset = AlertaOperativa.objects.select_related(
        "perfil_afectado", "casa_afectada"
    ).all()
    serializer_class = AlertaOperativaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# BITÁCORA DE MANDO VIEWSET
# ============================================================================


class BitacoraMandoViewSet(viewsets.ModelViewSet):
    queryset = BitacoraMando.objects.select_related("perfil", "usuario_registro").all()
    serializer_class = BitacoraMandoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# OBJETIVOS CREACIÓN PERFILES VIEWSET
# ============================================================================


class ObjetivoCreacionPerfilesViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar objetivos de creación de perfiles.

    Endpoints disponibles:
    - GET /objetivos-perfiles/ - Listar todos los objetivos
    - POST /objetivos-perfiles/ - Crear nuevo objetivo
    - GET /objetivos-perfiles/{id}/ - Detalle de un objetivo
    - PUT /objetivos-perfiles/{id}/ - Actualizar objetivo
    - DELETE /objetivos-perfiles/{id}/ - Eliminar objetivo
    - GET /objetivos-perfiles/pendientes/ - Solo objetivos no completados
    - GET /objetivos-perfiles/estadisticas/ - Estadísticas generales
    - GET /objetivos-perfiles/calendario_eventos/ - Eventos para calendario
    """

    queryset = ObjetivoCreacionPerfiles.objects.select_related("agencia").all()
    serializer_class = ObjetivoCreacionPerfilesSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        """Filtra por agencia y/o estado de completado."""
        queryset = super().get_queryset()

        # Filtrar por agencia si se especifica
        agencia_id = self.request.query_params.get("agencia", None)
        if agencia_id:
            queryset = queryset.filter(agencia_id=agencia_id)

        # Filtrar por estado de completado
        completado = self.request.query_params.get("completado", None)
        if completado is not None:
            completado_bool = completado.lower() in ["true", "1", "yes"]
            queryset = queryset.filter(completado=completado_bool)

        return queryset

    @action(detail=False, methods=["get"])
    def pendientes(self, request):
        """
        GET /objetivos-perfiles/pendientes/

        Retorna todos los objetivos NO completados, ordenados por fecha límite.
        Ideal para el dashboard de "Perfiles pendientes".
        """
        objetivos = self.get_queryset().filter(completado=False).order_by("fecha_limite")
        serializer = self.get_serializer(objetivos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def estadisticas(self, request):
        """
        GET /objetivos-perfiles/estadisticas/

        Retorna estadísticas generales de objetivos:
        - Total de objetivos
        - Objetivos completados
        - Objetivos pendientes
        - Total de perfiles objetivo
        - Total de perfiles completados
        """
        qs = self.get_queryset()
        stats = {
            "total_objetivos": qs.count(),
            "objetivos_completados": qs.filter(completado=True).count(),
            "objetivos_pendientes": qs.filter(completado=False).count(),
            "total_perfiles_objetivo": qs.aggregate(Sum("cantidad_objetivo"))[
                "cantidad_objetivo__sum"
            ]
            or 0,
            "total_perfiles_completados": qs.aggregate(Sum("cantidad_completada"))[
                "cantidad_completada__sum"
            ]
            or 0,
        }

        return Response(stats)

    @action(detail=False, methods=["get"])
    def calendario_eventos(self, request):
        """
        GET /objetivos-perfiles/calendario_eventos/

        Retorna eventos para calendario gráfico:
        - Fechas límite de objetivos (eventos futuros/pasados)
        - Perfiles creados (eventos históricos)

        Formato de respuesta: Lista de eventos con tipo, fecha, y datos relacionados.
        """
        eventos = []
        objetivos = ObjetivoCreacionPerfiles.objects.select_related("agencia").all()

        for objetivo in objetivos:
            # Evento: fecha límite del objetivo
            eventos.append(
                {
                    "id": f"objetivo-{objetivo.id_objetivo}",
                    "tipo": "fecha_limite",
                    "titulo": f"Límite: {objetivo.agencia.nombre}",
                    "agencia_id": objetivo.agencia.id_agencia,
                    "agencia_nombre": objetivo.agencia.nombre,
                    "fecha": objetivo.fecha_limite.isoformat(),
                    "fecha_inicio": objetivo.fecha_inicio.isoformat(),
                    "cantidad_objetivo": objetivo.cantidad_objetivo,
                    "cantidad_completada": objetivo.cantidad_completada,
                    "perfiles_restantes": objetivo.perfiles_restantes,
                    "completado": objetivo.completado,
                    "color": "green" if objetivo.completado else "red",
                }
            )

            # Obtener perfiles creados para este objetivo (dentro del rango de fechas)
            perfiles = PerfilOperativo.objects.filter(
                agencia=objetivo.agencia,
                fecha_creacion__gte=objetivo.fecha_inicio,
                fecha_creacion__lte=objetivo.fecha_limite,
            ).order_by("fecha_creacion")

            for idx, perfil in enumerate(perfiles, 1):
                if perfil.fecha_creacion:  # Validar que existe el timestamp
                    eventos.append(
                        {
                            "id": f"perfil-{perfil.id_perfil}",
                            "tipo": "perfil_creado",
                            "titulo": f"Perfil #{idx} - {objetivo.agencia.nombre}",
                            "agencia_id": objetivo.agencia.id_agencia,
                            "agencia_nombre": objetivo.agencia.nombre,
                            "fecha": perfil.fecha_creacion.date().isoformat(),
                            "hora": perfil.fecha_creacion.time().isoformat(),
                            "nombre_usuario": perfil.nombre_usuario,
                            "tipo_jugador": perfil.tipo_jugador,
                            "color": "blue",
                        }
                    )

            # Eventos de días planificados
            if objetivo.planificacion:
                tz = pytz.timezone("America/Guayaquil")
                for fecha_str, cantidad in objetivo.planificacion.items():
                    # Contar perfiles creados ese día específico (timezone Ecuador)
                    fecha_plan = date.fromisoformat(fecha_str)
                    
                    # Convertir a rango de datetime con timezone
                    from datetime import datetime, time
                    inicio_dia = tz.localize(datetime.combine(fecha_plan, time.min))
                    fin_dia = tz.localize(datetime.combine(fecha_plan, time.max))
                    
                    creados_ese_dia = PerfilOperativo.objects.filter(
                        agencia=objetivo.agencia,
                        fecha_creacion__gte=inicio_dia,
                        fecha_creacion__lte=fin_dia,
                    ).count()
                    
                    eventos.append(
                        {
                            "id": f"plan-{objetivo.id_objetivo}-{fecha_str}",
                            "tipo": "planificado",
                            "titulo": f"Crear {cantidad} perfiles",
                            "agencia_id": objetivo.agencia.id_agencia,
                            "agencia_nombre": objetivo.agencia.nombre,
                            "fecha": fecha_str,
                            "cantidad_planificada": cantidad,
                            "cantidad_creada": creados_ese_dia,
                            "objetivo_id": objetivo.id_objetivo,
                        }
                    )

        return Response(eventos)

    @action(detail=True, methods=["patch"], url_path="planificar")
    def planificar(self, request, pk=None):
        """
        PATCH /objetivos-perfiles/{id}/planificar/

        Body: {"fecha": "2026-01-28", "cantidad": 2}

        Guarda/actualiza la planificación de creación de perfiles para una fecha.
        Si cantidad=0, elimina esa fecha del JSON.
        """
        objetivo = self.get_object()
        fecha_str = request.data.get("fecha")
        cantidad = request.data.get("cantidad")

        # Validaciones básicas
        if not fecha_str:
            return Response(
                {"error": "Se requiere el campo 'fecha'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if cantidad is None:
            return Response(
                {"error": "Se requiere el campo 'cantidad'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            return Response(
                {"error": "La cantidad debe ser un número entero"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar formato de fecha
        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar que la fecha esté dentro del rango del objetivo
        if fecha < objetivo.fecha_inicio or fecha > objetivo.fecha_limite:
            return Response(
                {
                    "error": f"La fecha debe estar entre {objetivo.fecha_inicio} y {objetivo.fecha_limite}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Obtener planificación actual (copia)
        planificacion = dict(objetivo.planificacion) if objetivo.planificacion else {}

        # Calcular suma actual sin la fecha que estamos modificando
        suma_actual = sum(
            v for k, v in planificacion.items() if k != fecha_str
        )

        # Validar que la suma no supere cantidad_objetivo
        if cantidad > 0 and (suma_actual + cantidad) > objetivo.cantidad_objetivo:
            disponible = objetivo.cantidad_objetivo - suma_actual
            return Response(
                {
                    "error": f"La suma de planificados ({suma_actual + cantidad}) supera el objetivo ({objetivo.cantidad_objetivo}). Disponible: {disponible}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Actualizar planificación
        if cantidad == 0:
            # Eliminar fecha si cantidad es 0
            planificacion.pop(fecha_str, None)
        else:
            planificacion[fecha_str] = cantidad

        objetivo.planificacion = planificacion
        objetivo.save(update_fields=["planificacion", "fecha_actualizacion"])

        return Response(self.get_serializer(objetivo).data)

    @action(detail=True, methods=["patch"], url_path="mover-planificacion")
    def mover_planificacion(self, request, pk=None):
        """
        PATCH /objetivos-perfiles/{id}/mover-planificacion/

        Body: {"fecha_origen": "2026-01-25", "fecha_destino": "2026-01-28"}

        Mueve la planificación de una fecha a otra (drag & drop en calendario).
        Si fecha_destino ya tiene planificación, se SUMA la cantidad.
        """
        objetivo = self.get_object()
        fecha_origen_str = request.data.get("fecha_origen")
        fecha_destino_str = request.data.get("fecha_destino")

        # Validaciones de campos requeridos
        if not fecha_origen_str:
            return Response(
                {"detail": "Se requiere el campo 'fecha_origen'"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not fecha_destino_str:
            return Response(
                {"detail": "Se requiere el campo 'fecha_destino'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validar formato de fechas
        try:
            fecha_origen = date.fromisoformat(fecha_origen_str)
        except ValueError:
            return Response(
                {"detail": "Formato de fecha_origen inválido. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            fecha_destino = date.fromisoformat(fecha_destino_str)
        except ValueError:
            return Response(
                {"detail": "Formato de fecha_destino inválido. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Obtener planificación actual
        planificacion = dict(objetivo.planificacion) if objetivo.planificacion else {}

        # Validación 1: fecha_origen debe existir en planificacion
        if fecha_origen_str not in planificacion:
            return Response(
                {"detail": "No existe planificación para la fecha origen"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validación 2: fecha_destino debe estar entre fecha_inicio y fecha_limite
        if fecha_destino < objetivo.fecha_inicio or fecha_destino > objetivo.fecha_limite:
            return Response(
                {"detail": "Fecha destino fuera del rango permitido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validación 3: fecha_destino >= HOY (timezone Ecuador)
        tz = pytz.timezone("America/Guayaquil")
        from django.utils import timezone
        hoy_ecuador = timezone.now().astimezone(tz).date()
        
        if fecha_destino < hoy_ecuador:
            return Response(
                {"detail": "No se puede mover a una fecha pasada"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Lógica de negocio: Mover planificación
        # 1. Extraer cantidad de fecha_origen
        cantidad = planificacion.pop(fecha_origen_str)

        # 2. Si fecha_destino ya tiene planificación, SUMAR
        if fecha_destino_str in planificacion:
            planificacion[fecha_destino_str] += cantidad
        else:
            planificacion[fecha_destino_str] = cantidad

        # 3. Guardar
        objetivo.planificacion = planificacion
        objetivo.save(update_fields=["planificacion", "fecha_actualizacion"])

        return Response(self.get_serializer(objetivo).data)

    @action(detail=False, methods=["get"])
    def alertas(self, request):
        """
        GET /objetivos-perfiles/alertas/

        Retorna alertas de planificación:
        - SIN_PLANIFICAR: objetivos que no tienen toda la cantidad planificada
        - HOY: perfiles a crear hoy según planificación
        - MAÑANA: perfiles a crear mañana según planificación
        - VENCIDO: objetivos cuya fecha_limite ya pasó
        - FALTAN_3_DIAS: objetivo vence en 3 días
        - FALTAN_2_DIAS: objetivo vence en 2 días
        - FALTAN_1_DIA: objetivo vence mañana
        """
        # Timezone America/Guayaquil
        tz = pytz.timezone("America/Guayaquil")
        from django.utils import timezone
        hoy = timezone.now().astimezone(tz).date()
        manana = hoy + timedelta(days=1)

        alertas = []
        objetivos = ObjetivoCreacionPerfiles.objects.select_related("agencia").filter(
            completado=False
        )

        for objetivo in objetivos:
            planificacion = objetivo.planificacion or {}
            suma_planificada = sum(planificacion.values())

            # Alerta SIN_PLANIFICAR
            if suma_planificada < objetivo.cantidad_objetivo:
                faltantes = objetivo.cantidad_objetivo - suma_planificada
                alertas.append(
                    {
                        "tipo": "SIN_PLANIFICAR",
                        "objetivo_id": objetivo.id_objetivo,
                        "agencia_id": objetivo.agencia.id_agencia,
                        "agencia_nombre": objetivo.agencia.nombre,
                        "mensaje": f"{objetivo.agencia.nombre}: No has planificado los {faltantes} perfiles faltantes",
                        "faltantes_por_planificar": faltantes,
                    }
                )

            # Alerta HOY
            hoy_str = hoy.isoformat()
            if hoy_str in planificacion:
                cantidad_hoy = planificacion[hoy_str]
                # Contar perfiles creados hoy para esta agencia
                creados_hoy = PerfilOperativo.objects.filter(
                    agencia=objetivo.agencia,
                    fecha_creacion__date=hoy,
                ).count()

                if creados_hoy < cantidad_hoy:
                    pendientes = cantidad_hoy - creados_hoy
                    alertas.append(
                        {
                            "tipo": "HOY",
                            "objetivo_id": objetivo.id_objetivo,
                            "agencia_id": objetivo.agencia.id_agencia,
                            "agencia_nombre": objetivo.agencia.nombre,
                            "mensaje": f"Hoy crear {pendientes} perfiles en {objetivo.agencia.nombre}",
                            "fecha": hoy_str,
                            "cantidad": cantidad_hoy,
                            "creados_hoy": creados_hoy,
                            "pendientes": pendientes,
                        }
                    )

            # Alerta MAÑANA
            manana_str = manana.isoformat()
            if manana_str in planificacion:
                cantidad_manana = planificacion[manana_str]
                alertas.append(
                    {
                        "tipo": "MAÑANA",
                        "objetivo_id": objetivo.id_objetivo,
                        "agencia_id": objetivo.agencia.id_agencia,
                        "agencia_nombre": objetivo.agencia.nombre,
                        "mensaje": f"Mañana crear {cantidad_manana} perfiles en {objetivo.agencia.nombre}",
                        "fecha": manana_str,
                        "cantidad": cantidad_manana,
                    }
                )

            # Alertas preventivas por días restantes hasta fecha_limite
            dias_restantes = (objetivo.fecha_limite - hoy).days
            perfiles_restantes = objetivo.perfiles_restantes

            # Alerta VENCIDO (fecha_limite ya pasó)
            if dias_restantes < 0 and perfiles_restantes > 0:
                alertas.append(
                    {
                        "tipo": "VENCIDO",
                        "objetivo_id": objetivo.id_objetivo,
                        "agencia_id": objetivo.agencia.id_agencia,
                        "agencia_nombre": objetivo.agencia.nombre,
                        "mensaje": f"VENCIDO: {objetivo.agencia.nombre} tenía que completar {perfiles_restantes} perfiles",
                        "fecha_limite": objetivo.fecha_limite.isoformat(),
                        "dias_vencido": abs(dias_restantes),
                        "perfiles_restantes": perfiles_restantes,
                    }
                )

            # Alertas FALTAN_X_DIAS (3, 2, 1 días antes del vencimiento)
            elif dias_restantes in [3, 2, 1] and perfiles_restantes > 0:
                tipo_alerta = f"FALTAN_{dias_restantes}_DIAS" if dias_restantes > 1 else "FALTAN_1_DIA"
                dia_texto = "días" if dias_restantes > 1 else "día"
                alertas.append(
                    {
                        "tipo": tipo_alerta,
                        "objetivo_id": objetivo.id_objetivo,
                        "agencia_id": objetivo.agencia.id_agencia,
                        "agencia_nombre": objetivo.agencia.nombre,
                        "mensaje": f"Faltan {dias_restantes} {dia_texto} para completar {perfiles_restantes} perfiles en {objetivo.agencia.nombre}",
                        "fecha_limite": objetivo.fecha_limite.isoformat(),
                        "dias_restantes": dias_restantes,
                        "perfiles_restantes": perfiles_restantes,
                    }
                )

        return Response(alertas)

    @action(detail=False, methods=["get"], url_path="historial-por-agencia")
    def historial_por_agencia(self, request):
        """
        GET /objetivos-perfiles/historial-por-agencia/?agencia_id=<ID>

        Retorna objetivos y perfiles creados de una agencia específica.
        Útil para ver el historial completo de una agencia en una sola request.
        """
        agencia_id = request.query_params.get("agencia_id")
        if not agencia_id:
            return Response(
                {"error": "Se requiere el parámetro agencia_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Obtener objetivos de la agencia
        objetivos = self.get_queryset().filter(agencia_id=agencia_id)

        # Obtener perfiles creados de la agencia
        perfiles = PerfilOperativo.objects.filter(agencia_id=agencia_id).order_by(
            "-fecha_creacion"
        )

        return Response(
            {
                "agencia_id": int(agencia_id),
                "objetivos": self.get_serializer(objetivos, many=True).data,
                "perfiles_creados": [
                    {
                        "id_perfil": p.id_perfil,
                        "nombre_usuario": p.nombre_usuario,
                        "fecha_creacion": p.fecha_creacion.isoformat()
                        if p.fecha_creacion
                        else None,
                        "tipo_jugador": p.tipo_jugador,
                        "nivel_cuenta": p.nivel_cuenta,
                        "activo": p.activo,
                    }
                    for p in perfiles
                ],
            }
        )
