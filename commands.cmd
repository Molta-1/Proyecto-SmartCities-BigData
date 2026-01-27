#WorkingDirectory
cd C:\Users\LENOVO\Documents\Big Data\Big Data\Proyecto

python --version
java -version

#Ve a: https://docs.aws.amazon.com/corretto/latest/corretto-11-ug/downloads-list.html
#Descarga: "Windows x64 JDK MSI installer"
#Ejecuta el instalador (Next, Next, Install)
#IMPORTANTE: Durante instalación, marca la opción "Set JAVA_HOME variable" si aparece

#Crear entorno
# Crear carpeta del proyecto
mkdir C:\BigData-SmartCities
cd C:\BigData-SmartCities
# Crear entorno virtual
python -m venv venv
# Activar entorno virtual
venv\Scripts\activate
#Desactivar
deactivate

#Instalar Pyspark y dependecias
# Actualizar pip
python -m pip install --upgrade pip
# Instalar PySpark (incluye Spark completo)
pip install pyspark==3.5.0
# Instalar Jupyter para notebooks
pip install jupyter notebook
# Instalar pandas (útil para manipulación de datos pequeños)
pip install pandas
# Instalar pyarrow (acelera operaciones Parquet)
pip install pyarrow

