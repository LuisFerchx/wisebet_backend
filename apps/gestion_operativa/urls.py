from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DistribuidoraViewSet, CasaApuestasViewSet, AgenciaViewSet,
    PerfilOperativoViewSet, ConfiguracionOperativaViewSet,
    TransaccionFinancieraViewSet, PlanificacionRotacionViewSet,
    AlertaOperativaViewSet, BitacoraMandoViewSet
)

router = DefaultRouter()
router.register(r'distribuidoras', DistribuidoraViewSet)
router.register(r'casas-apuestas', CasaApuestasViewSet)
router.register(r'agencias', AgenciaViewSet)
router.register(r'perfiles-operativos', PerfilOperativoViewSet)
router.register(r'configuracion-operativa', ConfiguracionOperativaViewSet)
router.register(r'transacciones', TransaccionFinancieraViewSet)
router.register(r'planificacion-rotacion', PlanificacionRotacionViewSet)
router.register(r'alertas-operativas', AlertaOperativaViewSet)
router.register(r'bitacoras-mando', BitacoraMandoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
