from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

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

        return Response(eventos)

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
