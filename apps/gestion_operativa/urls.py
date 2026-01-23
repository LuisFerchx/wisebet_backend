from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DistribuidoraViewSet,
    CasaApuestasViewSet,
    UbicacionViewSet,
    AgenciaViewSet,
    PerfilOperativoViewSet,
    ConfiguracionOperativaViewSet,
    OperacionViewSet,
    TransaccionFinancieraViewSet,
    PlanificacionRotacionViewSet,
    AlertaOperativaViewSet,
    BitacoraMandoViewSet,
    DeporteViewSet,
    PaisViewSet,
    ProvinciaEstadoViewSet,
    CiudadViewSet,
    PersonaViewSet,
    ObjetivoCreacionPerfilesViewSet,
)

router = DefaultRouter()
router.register(r"distribuidoras", DistribuidoraViewSet)
router.register(r"casas-apuestas", CasaApuestasViewSet)
router.register(r"ubicaciones", UbicacionViewSet)
router.register(r"agencias", AgenciaViewSet)
router.register(r"perfiles-operativos", PerfilOperativoViewSet)
router.register(r"operaciones", OperacionViewSet)
router.register(r"configuracion-operativa", ConfiguracionOperativaViewSet)
router.register(r"transacciones", TransaccionFinancieraViewSet)
router.register(r"planificacion-rotacion", PlanificacionRotacionViewSet)
router.register(r"alertas-operativas", AlertaOperativaViewSet)
router.register(r"bitacoras-mando", BitacoraMandoViewSet)
router.register(r"deportes", DeporteViewSet)
router.register(r"paises", PaisViewSet)
router.register(r"provincias", ProvinciaEstadoViewSet)
router.register(r"ciudades", CiudadViewSet)
router.register(r"personas", PersonaViewSet)
router.register(r"objetivos-perfiles", ObjetivoCreacionPerfilesViewSet, basename="objetivos-perfiles")

urlpatterns = [
    path("", include(router.urls)),
]
