# Estándares de Código - Proyecto Big Data Smart Cities

## Naming Conventions

### Variables y Funciones
- Variables: `snake_case` → `total_registros`, `datos_limpios`
- Funciones: `snake_case` → `procesar_sensores()`, `calcular_metricas()`
- Clases: `PascalCase` → `AnalizadorTrafico`, `ETLSensores`
- Constantes: `UPPER_SNAKE_CASE` → `MAX_PARTICIONES`, `RUTA_DATOS`
- DataFrames Spark: sufijo `_df` → `sensores_df`, `trafico_df`

### Archivos
- Scripts: `etl_sensores_trafico.py`
- Notebooks: `01_exploracion_datos.ipynb`

## Docstrings

Toda función debe documentar:
```python
def procesar_sensores(df_raw, fecha_inicio, fecha_fin):
    """
    Breve descripción de una línea.
    
    Args:
        df_raw (DataFrame): Descripción
        fecha_inicio (str): Formato 'YYYY-MM-DD'
        
    Returns:
        DataFrame: Qué contiene
        
    Example:
        >>> df = procesar_sensores(raw_df, '2024-01-01', '2024-01-31')
    """
```

## Comentarios

Explica el "por qué", no el "qué":
```python
# ✅ Bueno: Decisión de diseño
# Repartir en 100 particiones para optimizar joins posteriores
df = df.repartition(100, "sensor_id")

# ❌ Malo: Obvio
# Crear columna hora
df = df.withColumn("hora", hour(col("timestamp")))
```

## Git Commits

Formato: `<tipo>: <descripción>`
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Documentación
- `refactor:` Mejora de código