# Alembic Migrations - Business Security

## 📚 Comandos básicos

### Crear una nueva migración (autogenerar)
```bash
# Detecta automáticamente cambios en los modelos
alembic revision --autogenerate -m "descripción del cambio"

# Ejemplo:
alembic revision --autogenerate -m "agregar tabla clientes"
```

### Crear migración manual (vacía)
```bash
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

### Información
```bash
# Ver historial de migraciones
alembic history

# Ver migración actual
alembic current

# Ver migraciones pendientes
alembic show head
```

## 🔄 Flujo de trabajo típico

1. **Modificar modelos** en `app/db/models/`
2. **Generar migración**:
   ```bash
   alembic revision --autogenerate -m "descripción"
   ```
3. **Revisar archivo generado** en `alembic/versions/`
4. **Aplicar migración**:
   ```bash
   alembic upgrade head
   ```

## 📝 Ejemplo de modificación de modelo

```python
# app/db/models/usuarios.py
class Usuario(Base):
    __tablename__ = "usuarios"
    
    # Agregar nueva columna
    ultimo_acceso = Column(DateTime, nullable=True)
```

Luego:
```bash
alembic revision --autogenerate -m "agregar campo ultimo_acceso a usuarios"
alembic upgrade head
```

## ⚠️ Notas importantes

- Siempre revisa el código generado antes de aplicar
- Alembic no detecta cambios en constraints, indices o cambios de nombre
- Para cambios complejos, edita manualmente el archivo de migración
- Haz backup de la BD antes de migraciones en producción

## 🗃️ Estructura

```
alembic/
├── versions/           # Archivos de migración
├── env.py             # Configuración de Alembic
└── script.py.mako     # Template para nuevas migraciones
```
