from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DeporteViewSet,
    DistribuidoraViewSet,
    CasaApuestasViewSet,
    UbicacionViewSet,
    PersonaViewSet,
    AgenciaViewSet,
    PerfilOperativoViewSet,
    ConfiguracionOperativaViewSet,
    ProtocoloAuditoriaViewSet,
    OperacionViewSet,
    TransaccionFinancieraViewSet,
    PlanificacionRotacionViewSet,
    AlertaOperativaViewSet,
    BitacoraMandoViewSet,
)

router = DefaultRouter()
router.register(r"deportes", DeporteViewSet)
router.register(r"distribuidoras", DistribuidoraViewSet)
router.register(r"casas-apuestas", CasaApuestasViewSet)
router.register(r"ubicaciones", UbicacionViewSet)
router.register(r"personas", PersonaViewSet)
router.register(r"agencias", AgenciaViewSet)
router.register(r"perfiles-operativos", PerfilOperativoViewSet)
router.register(r"operaciones", OperacionViewSet)
router.register(r"configuracion-operativa", ConfiguracionOperativaViewSet)
router.register(r"protocolo-auditoria", ProtocoloAuditoriaViewSet)
router.register(r"transacciones", TransaccionFinancieraViewSet)
router.register(r"planificacion-rotacion", PlanificacionRotacionViewSet)
router.register(r"alertas-operativas", AlertaOperativaViewSet)
router.register(r"bitacoras-mando", BitacoraMandoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
