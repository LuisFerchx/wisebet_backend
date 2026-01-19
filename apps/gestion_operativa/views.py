from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

from .models import (
    Deporte,
    Distribuidora,
    CasaApuestas,
    Ubicacion,
    Persona,
    Agencia,
    PerfilOperativo,
    ConfiguracionOperativa,
    ProtocoloAuditoria,
    TransaccionFinanciera,
    PlanificacionRotacion,
    AlertaOperativa,
    BitacoraMando,
    Operacion,
)
from .serializers import (
    DeporteSerializer,
    DistribuidoraSerializer,
    DistribuidoraExpandedSerializer,
    CasaApuestasSerializer,
    UbicacionSerializer,
    PersonaSerializer,
    AgenciaSerializer,
    PerfilOperativoSerializer,
    ConfiguracionOperativaSerializer,
    ProtocoloAuditoriaSerializer,
    TransaccionFinancieraSerializer,
    PlanificacionRotacionSerializer,
    AlertaOperativaSerializer,
    BitacoraMandoSerializer,
    OperacionSerializer,
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
# DEPORTES VIEWSET
# ============================================================================


class DeporteViewSet(viewsets.ModelViewSet):
    """ViewSet para catálogo de deportes."""

    queryset = Deporte.objects.all()
    serializer_class = DeporteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination


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

    def get_queryset(self):
        """Filtra por distribuidora si se especifica."""
        queryset = super().get_queryset()
        distribuidora_id = self.request.query_params.get("distribuidora")

        if distribuidora_id:
            queryset = queryset.filter(distribuidora_id=distribuidora_id)

        return queryset.order_by("nombre")


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
# PERSONAS VIEWSET
# ============================================================================


class PersonaViewSet(viewsets.ModelViewSet):
    """ViewSet para datos de identidad de personas."""

    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]
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
        "usuario", "casa", "agencia"
    ).all()
    serializer_class = PerfilOperativoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination


# ============================================================================
# CONFIGURACIÓN OPERATIVA VIEWSET
# ============================================================================


class ConfiguracionOperativaViewSet(viewsets.ModelViewSet):
    """ViewSet para métricas operativas diarias (singleton)."""

    queryset = ConfiguracionOperativa.objects.all()
    serializer_class = ConfiguracionOperativaSerializer
    permission_classes = [IsAuthenticated]


# ============================================================================
# PROTOCOLO DE AUDITORÍA VIEWSET
# ============================================================================


class ProtocoloAuditoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para umbrales de auditoría (singleton)."""

    queryset = ProtocoloAuditoria.objects.all()
    serializer_class = ProtocoloAuditoriaSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Registra quién modificó el protocolo."""
        serializer.save(updated_by=self.request.user)


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
