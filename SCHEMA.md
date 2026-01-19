# WiseBet Backend - Database Schema

> Documentación de la estructura de base de datos normalizada.
> Última actualización: 2026-01-17

---

## Diagrama de Relaciones (ERD Simplificado)

```
┌─────────────────┐       ┌─────────────────┐
│  Distribuidora  │──1:N──│  CasaApuestas   │
└─────────────────┘       └────────┬────────┘
                                   │
                          ┌────────┴────────┐
                          │     Agencia     │──N:1──┌─────────────┐
                          └────────┬────────┘       │  Ubicacion  │
                                   │               └─────────────┘
                                   │
┌─────────────┐               ┌────────┴────────┐
│   Persona   │──1:N───────────│ PerfilOperativo │
└─────────────┘               └────────┬────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
     ┌────────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐
     │    Operacion    │  │  Transaccion    │  │  Planificacion  │
     │    (Apuestas)   │  │   Financiera    │  │    Rotacion     │
     └─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Tablas Principales

### 1. Distribuidora (`distribuidoras_datos`)

Entidad raíz que agrupa casas de apuestas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_distribuidora` | PK, AutoField | Identificador único |
| `nombre` | CharField(100) | Nombre de la distribuidora |
| `deportes` | JSONField | Lista de deportes disponibles |
| `descripcion` | TextField | Descripción opcional |
| `activo` | Boolean | Estado activo/inactivo |
| `fecha_creacion` | DateTime | Auto timestamp |
| `fecha_actualizacion` | DateTime | Auto timestamp |

**Relaciones:** 1:N con `CasaApuestas`

---

### 2. CasaApuestas (`casas_apuestas`)

Casas de apuestas pertenecientes a una distribuidora.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_casa` | PK, AutoField | Identificador único |
| `distribuidora` | FK → Distribuidora | Distribuidora padre |
| `nombre` | CharField(100) | Nombre de la casa |
| `nro_perfiles` | Integer | Cantidad de perfiles |
| `url_backoffice` | URLField | Link al backoffice |
| `capital_activo_hoy` | Decimal(12,2) | Capital del día |
| `capital_total` | Decimal(12,2) | Capital acumulado |
| `perfiles_minimos_req` | Integer | Requisito mínimo |
| `activo` | Boolean | Estado |

**Relaciones:** N:1 con `Distribuidora`, 1:N con `PerfilOperativo`, 1:N con `Agencia`

---

### 3. Ubicacion (`ubicaciones`)

Catálogo normalizado de ubicaciones geográficas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_ubicacion` | PK, AutoField | Identificador único |
| `pais` | CharField(100) | País (default: Perú) |
| `provincia_estado` | CharField(100) | Provincia o Estado |
| `ciudad` | CharField(100) | Ciudad |
| `direccion` | CharField(255) | Dirección exacta (calles) |
| `referencia` | CharField(255) | Referencia opcional |
| `link_google_maps` | URLField | Enlace a Google Maps |

**Relaciones:** 1:N con `Agencia`

---

### 4. Persona (`personas`)

Datos de identidad de una persona real para crear cuentas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_persona` | PK, AutoField | Identificador único |
| `primer_nombre` | CharField(100) | Primer nombre |
| `segundo_nombre` | CharField(100) | Segundo nombre (opcional) |
| `primer_apellido` | CharField(100) | Primer apellido |
| `segundo_apellido` | CharField(100) | Segundo apellido (opcional) |
| `tipo_documento` | Enum | CEDULA, PASAPORTE, LICENCIA, DNI, OTRO |
| `numero_documento` | CharField(50) | Número de identificación (**único**) |
| `fecha_nacimiento` | DateField | Fecha de nacimiento |
| `pais` | CharField(100) | País de residencia |
| `telefono` | CharField(20) | Teléfono de contacto |
| `correo_electronico` | EmailField | Email (**único**) |
| `direccion` | CharField(255) | Dirección (opcional) |
| `foto_rostro` | ImageField | Selfie para verificación KYC |
| `documento_frente` | ImageField | Copia documento (frente) |
| `documento_reverso` | ImageField | Copia documento (reverso) |
| `fecha_registro` | DateTime | Auto timestamp |
| `activo` | Boolean | Estado |

**Relaciones:** 1:N con `PerfilOperativo`

---

### 5. Agencia (`agencias`)

Agencias que gestionan perfiles operativos.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_agencia` | PK, AutoField | Identificador único |
| `nombre` | CharField(100) | Nombre de la agencia |
| `ubicacion` | FK → Ubicacion | Ubicación normalizada |
| `responsable` | CharField(100) | Nombre del responsable |
| `contacto` | CharField(100) | Teléfono/Email |
| `casa_madre` | FK → CasaApuestas | Casa principal (opcional) |
| `rake_porcentaje` | Decimal(5,2) | % de Rake |
| `perfiles_minimos` | Integer | Objetivo de perfiles |
| `url_backoffice` | URLField | Link al panel de agente |
| `activo` | Boolean | Estado |
| `fecha_registro` | DateTime | Auto timestamp |

**Relaciones:** N:1 con `Ubicacion`, N:1 con `CasaApuestas`, 1:N con `PerfilOperativo`

---

### 5. PerfilOperativo (`perfiles_operativos`)

Perfiles de operadores/apostadores.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_perfil` | PK, AutoField | Identificador único |
| `usuario` | FK → User | Operador que gestiona el perfil |
| `persona` | FK → Persona | Datos de identidad usados |
| `casa` | FK → CasaApuestas | Casa de apuestas (**opcional**) |
| `agencia` | FK → Agencia | Agencia donde se creó |
| `url_acceso_backoffice` | URLField | Link al backoffice de la cuenta |
| `nombre_usuario` | CharField(100) | Username en la casa |
| `tipo_jugador` | Enum | PROFESIONAL, RECREATIVO, CASUAL, HIGH_ROLLER |
| `deporte_dna` | Enum | Deporte principal |
| `ip_operativa` | IPField | IP de operación |
| `preferencias` | TextField | Notas/preferencias |
| `nivel_cuenta` | Enum | BRONCE, PLATA, ORO, PLATINO, DIAMANTE |
| `meta_ops_semanales` | Integer | Meta configurable |
| `activo` | Boolean | Estado |

**Restricción:** `unique_together = ['persona', 'casa']` (Una persona solo puede tener UNA cuenta por casa)

**Campos Calculados (No almacenados, se obtienen al vuelo):**

- `saldo_real`: Suma de depósitos - retiros desde `TransaccionFinanciera`
- `stake_promedio`: Promedio de `importe` desde `Operacion`
- `ops_semanales`: Count de operaciones de la semana
- `ops_mensuales`: Count de operaciones del mes
- `ops_historicas`: Count total de operaciones

**Relaciones:** N:1 con `User`, N:1 con `Persona`, N:1 con `CasaApuestas`, N:1 con `Agencia`, 1:N con `Operacion`, 1:N con `TransaccionFinanciera`

---

### 6. Operacion (`operaciones`)

Registro detallado de cada apuesta realizada.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_operacion` | PK, AutoField | Identificador único |
| `perfil` | FK → PerfilOperativo | Perfil que realizó la operación |
| `fecha_registro` | DateTime | Timestamp exacto |
| `importe` | Decimal(12,2) | Stake apostado |
| `cuota` | Decimal(6,2) | Odds de la apuesta |
| `estado` | Enum | PENDIENTE, GANADA, PERDIDA, ANULADA |
| `payout` | Decimal(12,2) | Retorno total |
| `profit_loss` | Decimal(12,2) | P&L (calculado automáticamente) |
| `deporte` | CharField(50) | Deporte de la apuesta |
| `mercado` | CharField(100) | Tipo de mercado |

**Relaciones:** N:1 con `PerfilOperativo`

---

### 7. TransaccionFinanciera (`transacciones_financieras`)

Movimientos de dinero (depósitos/retiros).

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_transaccion` | PK, AutoField | Identificador único |
| `perfil` | FK → PerfilOperativo | Perfil asociado |
| `tipo_transaccion` | CharField | DEPOSITO, RETIRO |
| `monto` | Decimal(12,2) | Cantidad |
| `fecha_transaccion` | DateTime | Fecha del movimiento |
| `metodo_pago` | CharField(100) | USDT, Skrill, etc. |
| `estado` | CharField(50) | Completado, Pendiente, etc. |

**Relaciones:** N:1 con `PerfilOperativo`

---

## Tablas Auxiliares

### PlanificacionRotacion (`planificacion_rotacion`)

Calendario de días activos/descanso por perfil.

### AlertaOperativa (`alertas_operativas`)

Sistema de alertas y notificaciones.

### BitacoraMando (`bitacora_mando`)

Log de observaciones por perfil.

### ConfiguracionOperativa (`configuracion_operativa`)

Configuración global del sistema (Singleton).

---

## Principios de Normalización Aplicados

1. **1NF**: Todos los campos son atómicos (no hay arrays en columnas, excepto `deportes` que es JSONField intencional).

2. **2NF**: No hay dependencias parciales. Cada campo depende completamente de la PK.

3. **3NF**: No hay dependencias transitivas.
   - `ciudad_sede` eliminado de `PerfilOperativo` (se obtiene de `agencia.ubicacion.ciudad`)
   - `saldo_real`, `stake_promedio`, `ops_*` eliminados (se calculan desde tablas transaccionales)

---

## API Endpoints

| Recurso | Endpoint | Descripción |
|---------|----------|-------------|
| Distribuidoras | `/api/gestion-operativa/distribuidoras/` | CRUD + `?expand=casas` |
| Casas | `/api/gestion-operativa/casas-apuestas/` | CRUD + `?distribuidora=ID` |
| Ubicaciones | `/api/gestion-operativa/ubicaciones/` | CRUD catálogo |
| Personas | `/api/gestion-operativa/personas/` | CRUD datos de identidad (Auth requerida) |
| Agencias | `/api/gestion-operativa/agencias/` | CRUD |
| Perfiles | `/api/gestion-operativa/perfiles-operativos/` | CRUD con campos calculados |
| Operaciones | `/api/gestion-operativa/operaciones/` | CRUD + `?perfil=ID` |
| Transacciones | `/api/gestion-operativa/transacciones/` | CRUD |
| Planificación | `/api/gestion-operativa/planificacion-rotacion/` | CRUD |
| Alertas | `/api/gestion-operativa/alertas-operativas/` | CRUD |
| Bitácora | `/api/gestion-operativa/bitacoras-mando/` | CRUD |
| Configuración | `/api/gestion-operativa/configuracion-operativa/` | CRUD Singleton |
