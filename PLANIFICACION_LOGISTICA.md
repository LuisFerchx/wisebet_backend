# Sistema de Planificación Logística - Red Viva

## 📋 Descripción General

Se ha implementado un sistema completo de planificación logística que evoluciona de una "meta estática" a un "sistema de calendario interactivo" para la creación de perfiles operativos. El sistema permite gestionar tareas individuales con fechas específicas, responsables asignados y seguimiento granular del progreso.

## 🆕 Nuevos Modelos

### 1. TareaPlanificada

Representa una tarea individual de creación de perfil dentro de un objetivo.

**Campos principales:**
- `objetivo`: ForeignKey a ObjetivoCreacionPerfiles
- `fecha_programada`: DateField (null=True para Backlog)
- `estado`: CharField (PENDIENTE, COMPLETADA, VENCIDA)
- `perfil_real`: OneToOneField a PerfilOperativo (vinculado al completar)
- `usuario_asignado`: ForeignKey a User
- `completada_en`: DateTimeField

**Propiedades calculadas:**
- `esta_vencida`: Verifica si la tarea está vencida
- `dias_hasta_vencimiento`: Calcula días hasta el vencimiento

**Tabla:** `tareas_planificadas`

### 2. CapacidadEquipo

Define la capacidad diaria de cada usuario para crear perfiles.

**Campos principales:**
- `usuario`: OneToOneField a User
- `capacidad_diaria`: PositiveIntegerField (default: 5)
- `activo`: BooleanField
- `notas`: TextField

**Métodos:**
- `tareas_asignadas_fecha(fecha)`: Cantidad de tareas asignadas para una fecha
- `capacidad_disponible_fecha(fecha)`: Capacidad disponible para una fecha

**Tabla:** `capacidad_equipo`

## 🔄 Lógica de Automatización (Signals)

### Signal 1: Auto-generación de Tareas
**Trigger:** Al crear un `ObjetivoCreacionPerfiles`

**Acción:**
- Crea automáticamente N registros de `TareaPlanificada` (donde N = cantidad_objetivo)
- Todas las tareas se crean con `fecha_programada=NULL` (Backlog)
- Estado inicial: `PENDIENTE`

### Signal 2: Vinculación Automática
**Trigger:** Al crear un `PerfilOperativo`

**Acción:**
1. Busca la `TareaPlanificada` más antigua PENDIENTE de esa agencia
2. Prioriza tareas con fecha programada sobre las de backlog
3. Vincula el perfil a la tarea
4. Marca la tarea como `COMPLETADA`
5. Actualiza el contador del `ObjetivoCreacionPerfiles`

**Compatibilidad:** Si no hay tarea disponible, actualiza el objetivo directamente (mantiene compatibilidad con el sistema anterior)

## 📡 Nuevos Endpoints API

### TareaPlanificada Endpoints

#### GET /api/tareas-planificadas/
Lista todas las tareas planificadas con filtros:
- `?estado=PENDIENTE|COMPLETADA|VENCIDA`
- `?agencia_id=<ID>`
- `?usuario_id=<ID>`
- `?fecha=YYYY-MM-DD`
- `?backlog=true` (solo tareas sin fecha)

#### GET /api/tareas-planificadas/calendario/
Retorna tareas en formato de calendario para un rango de fechas.

**Query Params:**
- `fecha_inicio`: YYYY-MM-DD
- `fecha_fin`: YYYY-MM-DD

**Response:**
```json
[
  {
    "id": 1,
    "tipo": "tarea_planificada",
    "titulo": "Perfil - Agencia Norte",
    "fecha": "2024-01-25",
    "estado": "PENDIENTE",
    "color": "blue",
    "agencia_id": 5,
    "agencia_nombre": "Agencia Norte",
    "usuario_asignado": "Juan Pérez"
  }
]
```

**Colores por Estado:**
- `PENDIENTE`: blue
- `COMPLETADA`: green
- `VENCIDA`: red

### Red Viva Endpoints (Sistema Central)

#### GET /api/redviva/resumen/
Resumen de planificación por agencia con métricas clave.

**Response:**
```json
[
  {
    "agencia_id": 5,
    "agencia_nombre": "Agencia Norte",
    "total_objetivo": 50,
    "planificados": 30,
    "completados": 10,
    "backlog": 20,
    "vencidos": 2,
    "urgency_score": 45.5,
    "dias_restantes": 15,
    "fecha_limite": "2024-02-10"
  }
]
```

**Urgency Score (0-100):**
- Calcula: `(perfiles_restantes / dias_restantes) * 10`
- 100 = Máxima urgencia (ya venció o muy cerca)
- Ordenado descendente por urgencia

#### GET /api/redviva/alertas/
Identifica problemas de planificación.

**Tipos de Alertas:**

1. **planificacion_pendiente** (severidad: alta)
   - Objetivos con todas las tareas en Backlog sin fecha

2. **tareas_vencidas** (severidad: critica)
   - Agencias con tareas vencidas sin completar

**Response:**
```json
[
  {
    "tipo": "planificacion_pendiente",
    "severidad": "alta",
    "agencia_id": 3,
    "agencia_nombre": "Agencia Centro",
    "mensaje": "Todas las 25 tareas están en Backlog sin fecha asignada"
  },
  {
    "tipo": "tareas_vencidas",
    "severidad": "critica",
    "agencia_id": 5,
    "agencia_nombre": "Agencia Norte",
    "mensaje": "5 tareas vencidas sin completar"
  }
]
```

### Agencia Endpoints (Extendidos)

#### POST /api/agencias/{id}/planificar/
Asigna fechas masivamente a tareas del backlog.

**Request Body:**
```json
{
  "fecha": "2024-01-25",
  "cantidad": 3,
  "usuario_id": 1  // opcional
}
```

**Response:**
```json
{
  "mensaje": "3 tareas planificadas exitosamente",
  "fecha": "2024-01-25",
  "tareas_ids": [15, 16, 17]
}
```

**Validaciones:**
- Cantidad debe ser positiva
- Debe haber suficientes tareas en backlog
- La fecha no puede ser pasada

### CapacidadEquipo Endpoints

#### GET /api/capacidad-equipo/
Lista capacidades del equipo.

**Filtros:**
- `?activo=true|false`

**Response:**
```json
[
  {
    "id_capacidad": 1,
    "usuario": 5,
    "usuario_nombre": "Juan Pérez",
    "capacidad_diaria": 8,
    "activo": true,
    "notas": "Disponible tiempo completo",
    "tareas_pendientes_hoy": 3
  }
]
```

## 🔍 Validaciones Implementadas

### TareaPlanificada
- No se puede programar en el pasado
- La fecha programada no puede exceder la fecha límite del objetivo
- Auto-actualización de estado según condiciones:
  - Si tiene perfil vinculado → `COMPLETADA`
  - Si fecha pasó y está pendiente → `VENCIDA`

### ObjetivoCreacionPerfiles (Mantenido)
- cantidad_objetivo: 1-100
- plazo_dias: 1-365
- Auto-cálculo de fecha_limite
- Auto-marcado como completado al alcanzar objetivo

## 📊 Cambios en Models Existentes

### ObjetivoCreacionPerfiles
Se mantiene intacto pero ahora tiene:
- `related_name="tareas"` para acceder a TareaPlanificada
- Funciona en conjunto con el nuevo sistema de tareas

### PerfilOperativo
- Ahora puede tener `related_name="tarea_origen"` (OneToOne con TareaPlanificada)
- Mantiene toda la funcionalidad anterior

## 🎨 Panel de Administración

Se agregaron interfaces de administración para:

### TareaPlanificadaAdmin
- Vista de lista con estado, agencia, fecha, usuario asignado
- Filtros por estado, fecha, agencia
- Campos calculados: vencida, días hasta vencimiento
- Fieldsets organizados

### CapacidadEquipoAdmin
- Vista de lista con usuario, capacidad, estado
- Filtros por activo
- Búsqueda por usuario

## 🚀 Flujo de Trabajo Recomendado

### 1. Crear Objetivo
```bash
POST /api/objetivos-perfiles/
{
  "agencia": 5,
  "cantidad_objetivo": 50,
  "plazo_dias": 30
}
```
→ Se crean automáticamente 50 tareas en Backlog

### 2. Planificar Tareas
```bash
POST /api/agencias/5/planificar/
{
  "fecha": "2024-01-25",
  "cantidad": 10,
  "usuario_id": 3
}
```
→ 10 tareas del backlog reciben fecha y responsable

### 3. Ver Calendario
```bash
GET /api/tareas-planificadas/calendario/?fecha_inicio=2024-01-20&fecha_fin=2024-01-31
```
→ Vista de calendario con todas las tareas programadas

### 4. Crear Perfil
```bash
POST /api/perfiles-operativos/
{
  "agencia": 5,
  "nombre_usuario": "player123",
  ...
}
```
→ Se vincula automáticamente a la tarea más antigua pendiente
→ Se marca como completada
→ Se actualiza el contador del objetivo

### 5. Monitorear Progreso
```bash
GET /api/redviva/resumen/
```
→ Vista general de todas las agencias con urgency_score

### 6. Revisar Alertas
```bash
GET /api/redviva/alertas/
```
→ Identificar problemas de planificación

## 📈 Métricas y KPIs

### Por Agencia (Resumen)
- **Total Objetivo**: Cantidad total de perfiles a crear
- **Planificados**: Tareas con fecha asignada
- **Completados**: Tareas finalizadas
- **Backlog**: Tareas sin fecha
- **Vencidos**: Tareas vencidas pendientes
- **Urgency Score**: Indicador de urgencia (0-100)
- **Días Restantes**: Días hasta fecha límite

### Por Usuario (Capacidad)
- **Capacidad Diaria**: Perfiles que puede crear por día
- **Tareas Pendientes Hoy**: Carga actual

## 🔐 Permisos

Todos los endpoints requieren autenticación:
- `IsAuthenticated` para operaciones de escritura
- `IsAuthenticatedOrReadOnly` para catálogos

## ⚙️ Configuración de Timezone

El sistema usa `America/Guayaquil` como timezone principal (definido en settings.py).

## 📦 Migración

**Archivo:** `0020_capacidadequipo_tareaplanificada.py`

**Cambios:**
- Crea tabla `tareas_planificadas`
- Crea tabla `capacidad_equipo`
- Agrega índices para optimización

**Aplicar:**
```bash
python manage.py migrate gestion_operativa
```

## 🔄 Compatibilidad con Sistema Anterior

El sistema mantiene **100% compatibilidad** con el flujo anterior:
- Si se crea un perfil sin tareas vinculadas, se actualiza el objetivo directamente
- Los objetivos existentes siguen funcionando
- No se requiere migración de datos

## 🛠️ Mantenimiento

### Tareas Automáticas Recomendadas

1. **Actualizar Estados Vencidos** (Cron diario)
```python
# Se actualiza automáticamente en el método save()
# Pero puede ejecutarse manualmente:
TareaPlanificada.objects.filter(
    fecha_programada__lt=timezone.now().date(),
    estado='PENDIENTE'
).update(estado='VENCIDA')
```

2. **Limpieza de Objetivos Completados** (Opcional)
```python
# Archivar objetivos completados antiguos
ObjetivoCreacionPerfiles.objects.filter(
    completado=True,
    fecha_actualizacion__lt=timezone.now() - timedelta(days=90)
).update(activo=False)
```

## 📝 Notas Técnicas

- **Bulk Create**: Se usa para crear múltiples tareas eficientemente
- **Select Related**: Optimización de queries en ViewSets
- **Indexes**: Agregados en campos de búsqueda frecuente
- **OneToOne**: Entre TareaPlanificada y PerfilOperativo para evitar duplicados
- **Signals**: Desacoplados y documentados para mantenibilidad

## 🎯 Próximos Pasos Sugeridos

1. **Dashboard Visual**: Crear vista gráfica del calendario en el frontend
2. **Notificaciones**: Sistema de alertas push para tareas vencidas
3. **Reportes**: Generación de reportes PDF de productividad
4. **IA/ML**: Predicción de capacidad óptima por usuario
5. **Integración**: Webhooks para notificar a sistemas externos

---

**Versión:** 1.0.0  
**Fecha:** 2026-01-24  
**Autor:** Sistema WiseBet Backend  
**Timezone:** America/Guayaquil
