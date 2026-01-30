import findspark
import os

findspark.init(r"C:\spark-4.1.1-bin-hadoop3") 

from pyspark.sql import SparkSession

try:
    spark = SparkSession.builder \
        .appName("PruebaVSC") \
        .getOrCreate()
    
    print("---------------------------------")
    print("¡LOGRADO! Spark está funcionando.")
    print("---------------------------------")
    
    spark.stop()
except Exception as e:
    print(f"Aún falta algo: {e}")