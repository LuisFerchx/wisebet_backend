from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

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
