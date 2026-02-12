# Working Directory
cd ~/Documents/BigData/Proyecto

python --version
java -version

# Instalar Java 11 en Linux
# Para Ubuntu/Debian:
sudo apt update
sudo apt install openjdk-11-jdk

# Para Fedora/RHEL:
# sudo dnf install java-11-openjdk-devel

# Verificar instalación
java -version
echo $JAVA_HOME

# Si JAVA_HOME no está configurado:
export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))
export PATH=$JAVA_HOME/bin:$PATH

# Para hacerlo permanente, añade al final de ~/.bashrc:
# echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))' >> ~/.bashrc
# echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
# source ~/.bashrc

# Crear estructura del proyecto
mkdir -p ~/BigData-SmartCities
cd ~/BigData-SmartCities

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Desactivar
# deactivate

# Instalar PySpark y dependencias
# Actualizar pip
python -m pip install --upgrade pip

# Instalar PySpark
pip install pyspark==3.5.0

# Instalar Jupyter
pip install jupyter notebook

# Instalar pandas
pip install pandas

# Instalar pyarrow
pip install pyarrow

# Eliminar venv viejo (si es necesario)
# rm -rf venv

# Crear venv con Python 3.11 específicamente
# Primero instalar Python 3.11 si no lo tienes:
# Ubuntu/Debian:
# sudo apt install python3.11 python3.11-venv

python3.11 -m venv venv

# Activar
source venv/bin/activate

# Verificar versión
python --version
# Debe decir: Python 3.11.x

# Listar versiones de Python instaladas2
ls /usr/bin/python*

# Verificar versión específica
python3.11 --version

# Actualizar pip
python -m pip install --upgrade pip

# Instalar PySpark
pip install pyspark==3.5.0

# Instalar resto de dependencias
pip install jupyter notebook pandas pyarrow

# Verificar instalaciones
pip list