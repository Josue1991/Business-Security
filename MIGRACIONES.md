# Guía de Migraciones con Alembic

## 🚀 Configuración inicial (Ya está hecho)

Alembic ya está configurado y listo para usar en este proyecto.

## 📝 Comandos comunes

### Ver estado actual
```bash
# Ver revisión actual de la BD
alembic current

# Ver historial completo
alembic history --verbose

# Ver migraciones pendientes
alembic show head
```

### Crear migraciones

```bash
# Autogenerar migración detectando cambios en modelos
alembic revision --autogenerate -m "descripción del cambio"

# Crear migración vacía (manual)
alembic revision -m "descripción"
```

### Aplicar migraciones

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una revisión específica
alembic upgrade <revision_id>

# Aplicar siguiente migración
alembic upgrade +1
```

### Revertir migraciones

```bash
# Revertir última migración
alembic downgrade -1

# Revertir a revisión específica
alembic downgrade <revision_id>

# Revertir todas
alembic downgrade base
```

## 🔄 Flujo de trabajo completo

### 1. Modificar un modelo

```python
# Ejemplo: app/db/models/usuarios.py
class Usuario(Base):
    __tablename__ = "usuarios"
    
    # ... campos existentes ...
    
    # ➕ Agregar nuevo campo
    ultimo_acceso = Column(DateTime, nullable=True)
```

### 2. Generar migración

```bash
alembic revision --autogenerate -m "agregar campo ultimo_acceso a usuarios"
```

Esto crea un archivo en `alembic/versions/` como:
```
20251126_1600-abc123def456_agregar_campo_ultimo_acceso_a_usuarios.py
```

### 3. Revisar el archivo generado

⚠️ **IMPORTANTE**: Siempre revisa el código generado antes de aplicar.

```python
def upgrade() -> None:
    op.add_column('usuarios', sa.Column('ultimo_acceso', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('usuarios', 'ultimo_acceso')
```

### 4. Aplicar migración

```bash
alembic upgrade head
```

### 5. Si algo sale mal, revertir

```bash
alembic downgrade -1
```

## 🎯 Casos de uso comunes

### Agregar nueva tabla

1. Crear modelo en `app/db/models/nueva_tabla.py`
2. Importarlo en `alembic/env.py`
3. Generar migración:
   ```bash
   alembic revision --autogenerate -m "agregar tabla nueva_tabla"
   ```
4. Aplicar:
   ```bash
   alembic upgrade head
   ```

### Modificar columna existente

```python
# En la migración generada:
def upgrade():
    op.alter_column('usuarios', 'email',
        existing_type=sa.String(255),
        type_=sa.String(320),  # Nuevo tamaño
        existing_nullable=True)
```

### Agregar índice

```python
def upgrade():
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
```

### Agregar constraint

```python
def upgrade():
    op.create_check_constraint(
        'check_edad_positiva',
        'empleados',
        'edad > 0'
    )

def downgrade():
    op.drop_constraint('check_edad_positiva', 'empleados')
```

## ⚠️ Limitaciones de autogenerate

Alembic NO detecta automáticamente:
- Cambios de nombre de tablas o columnas
- Cambios en constraints (check, unique)
- Cambios en índices
- Cambios en tipos enum

Para estos casos, edita manualmente el archivo de migración.

## 🗄️ Cambiar entre SQLite y PostgreSQL

### Desarrollo con SQLite
```env
# .env
DATABASE_URL=sqlite:///./business_security.db
```

```bash
alembic upgrade head
python seed_db.py
```

### Producción con PostgreSQL
```env
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/business_security
```

```bash
alembic upgrade head
python seed_db.py
```

⚠️ Las migraciones son compatibles entre ambas BD.

## 🔧 Problemas comunes

### Error: "Can't locate revision identified by '...'"
```bash
# Ver estado
alembic current

# Si está desincronizado, marcar como aplicada manualmente
alembic stamp head
```

### Error: "Target database is not up to date"
```bash
alembic upgrade head
```

### Regenerar BD desde cero
```bash
# ⚠️ CUIDADO: Esto borra todos los datos
rm business_security.db
alembic upgrade head
python seed_db.py
```

## 📚 Recursos adicionales

- [Documentación oficial de Alembic](https://alembic.sqlalchemy.org/)
- [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [Operaciones de migración](https://alembic.sqlalchemy.org/en/latest/ops.html)
