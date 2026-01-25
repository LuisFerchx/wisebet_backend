# 🚀 Guía Rápida - Sistema de Planificación Logística

## Inicio Rápido (5 minutos)

### 1. Preparar Datos de Prueba

```bash
# Aplicar migraciones
python manage.py migrate

# Crear superusuario (si no existe)
python manage.py createsuperuser

# Poblar datos de prueba
python test_planificacion_logistica.py
```

### 2. Iniciar Servidor

```bash
python manage.py runserver
```

### 3. Endpoints Principales

#### 📊 Ver Resumen General
```http
GET http://localhost:8000/api/redviva/resumen/
```

**Respuesta:**
```json
[
  {
    "agencia_id": 1,
    "agencia_nombre": "Agencia Centro",
    "total_objetivo": 20,
    "planificados": 10,
    "completados": 0,
    "backlog": 10,
    "urgency_score": 33.33,
    "dias_restantes": 30
  }
]
```

#### ⚠️ Ver Alertas
```http
GET http://localhost:8000/api/redviva/alertas/
```

#### 📅 Ver Calendario
```http
GET http://localhost:8000/api/tareas-planificadas/calendario/?fecha_inicio=2026-01-24&fecha_fin=2026-01-31
```

#### 📝 Planificar Tareas del Backlog
```http
POST http://localhost:8000/api/agencias/1/planificar/
Content-Type: application/json

{
  "fecha": "2026-01-25",
  "cantidad": 5,
  "usuario_id": 1
}
```

#### ✅ Crear Perfil (Auto-completa Tarea)
```http
POST http://localhost:8000/api/perfiles-operativos/
Content-Type: application/json

{
  "agencia": 1,
  "nombre_usuario": "player_test_001",
  "tipo_jugador": "RECREATIVO",
  "deporte_dna": 1,
  "ip_operativa": "192.168.1.100",
  "nivel_cuenta": "BASICO",
  "persona": 1,
  "stake_minimo": "10.00",
  "stake_maximo": "100.00"
}
```

## 📱 Flujos de Trabajo Comunes

### Flujo 1: Crear Nuevo Objetivo

```bash
# 1. Crear objetivo
POST /api/objetivos-perfiles/
{
  "agencia": 1,
  "cantidad_objetivo": 50,
  "plazo_dias": 30
}

# 2. Verificar tareas creadas (deben ser 50 en backlog)
GET /api/tareas-planificadas/?agencia_id=1&backlog=true

# 3. Ver resumen
GET /api/redviva/resumen/
```

### Flujo 2: Planificar Semana

```bash
# 1. Ver alertas de planificación pendiente
GET /api/redviva/alertas/

# 2. Planificar lunes
POST /api/agencias/1/planificar/
{
  "fecha": "2026-01-27",
  "cantidad": 8,
  "usuario_id": 1
}

# 3. Planificar martes
POST /api/agencias/1/planificar/
{
  "fecha": "2026-01-28",
  "cantidad": 8,
  "usuario_id": 1
}

# 4. Ver calendario de la semana
GET /api/tareas-planificadas/calendario/?fecha_inicio=2026-01-27&fecha_fin=2026-01-31
```

### Flujo 3: Completar Tareas

```bash
# 1. Ver tareas pendientes de hoy
GET /api/tareas-planificadas/?fecha=2026-01-24&estado=PENDIENTE

# 2. Crear perfil (auto-completa la tarea más antigua)
POST /api/perfiles-operativos/
{...}

# 3. Verificar tarea completada
GET /api/tareas-planificadas/?estado=COMPLETADA

# 4. Ver progreso del objetivo
GET /api/objetivos-perfiles/{id}/
```

### Flujo 4: Monitorear Equipo

```bash
# 1. Ver capacidades del equipo
GET /api/capacidad-equipo/?activo=true

# 2. Ver carga de trabajo por usuario
GET /api/tareas-planificadas/?usuario_id=1&estado=PENDIENTE

# 3. Ajustar capacidad si es necesario
PATCH /api/capacidad-equipo/1/
{
  "capacidad_diaria": 10
}
```

## 🎨 Colores del Calendario

Para el frontend, usar estos colores según el estado:

```javascript
const colorPorEstado = {
  'PENDIENTE': '#3498db',  // Azul
  'COMPLETADA': '#2ecc71', // Verde
  'VENCIDA': '#e74c3c'     // Rojo
};
```

## 🔍 Filtros Útiles

### Tareas Planificadas

```bash
# Todas las tareas pendientes
GET /api/tareas-planificadas/?estado=PENDIENTE

# Tareas de una agencia específica
GET /api/tareas-planificadas/?agencia_id=1

# Tareas de un usuario
GET /api/tareas-planificadas/?usuario_id=1

# Tareas de una fecha
GET /api/tareas-planificadas/?fecha=2026-01-25

# Solo backlog
GET /api/tareas-planificadas/?backlog=true

# Combinar filtros
GET /api/tareas-planificadas/?agencia_id=1&estado=PENDIENTE&usuario_id=1
```

### Objetivos

```bash
# Objetivos activos (no completados)
GET /api/objetivos-perfiles/?completado=false

# Objetivos de una agencia
GET /api/objetivos-perfiles/?agencia_id=1

# Ver calendario de eventos de objetivos
GET /api/objetivos-perfiles/calendario_eventos/?fecha_inicio=2026-01-01&fecha_fin=2026-01-31
```

## 📊 Interpretación de Métricas

### Urgency Score

- **0-30**: Baja urgencia (ritmo normal)
- **31-60**: Urgencia media (acelerar un poco)
- **61-85**: Alta urgencia (requiere atención)
- **86-100**: Urgencia crítica (acción inmediata)

### Estados de Tarea

- **PENDIENTE**: Esperando ser completada
- **COMPLETADA**: Perfil creado y vinculado
- **VENCIDA**: Fecha pasó sin completar

## 🛠️ Admin Django

Accede al panel de administración en: `http://localhost:8000/admin/`

### Modelos Disponibles

- **Tareas Planificadas**: Ver y editar tareas individuales
- **Capacidad Equipo**: Configurar capacidades de usuarios
- **Objetivos Creación Perfiles**: Ver progreso de objetivos

### Vistas Útiles en Admin

1. **Filtrar tareas vencidas**:
   - Ir a Tareas Planificadas
   - Filtrar por Estado = "VENCIDA"

2. **Ver backlog de una agencia**:
   - Ir a Tareas Planificadas
   - Filtrar por Agencia + Estado "PENDIENTE"
   - Buscar las que tienen fecha_programada vacía

3. **Monitorear productividad**:
   - Ver tareas completadas por usuario
   - Filtrar por Usuario Asignado + Estado "COMPLETADA"

## 🔗 Integración Frontend

### React/Vue/Angular

```javascript
// Obtener resumen
const resumen = await fetch('/api/redviva/resumen/')
  .then(r => r.json());

// Planificar tareas
const planificar = async (agenciaId, fecha, cantidad, usuarioId) => {
  const response = await fetch(`/api/agencias/${agenciaId}/planificar/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`
    },
    body: JSON.stringify({ fecha, cantidad, usuario_id: usuarioId })
  });
  return response.json();
};

// Obtener calendario
const calendario = await fetch(
  '/api/tareas-planificadas/calendario/?' +
  'fecha_inicio=2026-01-24&fecha_fin=2026-01-31'
).then(r => r.json());

// Mostrar en FullCalendar
calendar.addEventSource(calendario);
```

## 📞 Soporte

Para más información consulta:
- **Documentación completa**: `PLANIFICACION_LOGISTICA.md`
- **Ejemplos de API**: `API_EXAMPLES.py`
- **Schema de DB**: `SCHEMA.md`

## 🎯 Tips de Productividad

1. **Planifica por lotes**: Usa el endpoint `/agencias/{id}/planificar/` para asignar múltiples tareas a la vez

2. **Monitorea urgency_score**: Revisa diariamente las agencias con score > 60

3. **Revisa alertas**: Consulta `/redviva/alertas/` cada mañana

4. **Ajusta capacidades**: Actualiza `CapacidadEquipo` según el rendimiento real

5. **Usa el calendario**: El endpoint `/calendario/` es perfecto para visualizaciones

---

¡Listo para planificar! 🎉
