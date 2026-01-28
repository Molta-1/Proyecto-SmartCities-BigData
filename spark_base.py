"""
Configuración base de Spark para el proyecto Smart Cities
Este archivo contiene la configuración correcta para que PySpark
funcione en Windows con Python 3.11.9
"""
import os
import sys

# CRÍTICO: Configurar qué Python debe usar Spark
# Esto evita problemas de compatibilidad de versiones
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

def crear_sesion_spark(app_name="SmartCities", log_level="WARN"):
    """
    Crea una sesión de Spark configurada correctamente para Windows.
    
    Parámetros:
        app_name: Nombre de la aplicación Spark
        log_level: Nivel de logging (WARN, INFO, ERROR, DEBUG)
    
    Retorna:
        SparkSession configurada y lista para usar
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .master("local[*]") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    
    # Configurar nivel de logging
    spark.sparkContext.setLogLevel(log_level)
    
    print(f"✅ Sesión Spark '{app_name}' creada exitosamente")
    print(f"   Spark version: {spark.version}")
    print(f"   Python: {sys.version.split()[0]}")
    
    return spark

# Ejemplo de uso si ejecutas este archivo directamente
if __name__ == "__main__":
    # Crear sesión de prueba
    spark = crear_sesion_spark("TestBase")
    
    # Probar con datos de ejemplo
    data = [("Sensor_001", 100), ("Sensor_002", 150)]
    df = spark.createDataFrame(data, ["sensor_id", "num_vehiculos"])
    df.show()
    
    # Cerrar sesión
    spark.stop()
    print("✅ Test completado")