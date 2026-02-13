# Proyecto Ciudad Inteligente - Big Data - Colegio Universitario de Cartago

# Tecnologías usadas
## Apache Spark 
Motor de procesamiento distribuido, para evitar procesar todo en una sola máquina Spark divide los datos en chunks o pedazos más  pequeños y los distribuye entre múltiples computadoras (clusters) para procesarlos en paralelo. 

Escrito en Scala y corre en la Máquina Virtual de Java.

## PySpark
API de python para Apache Spark. Permite escribir código en Python, que controla y ejecuta operaciones 
en Spark 

Spark es increíblemente poderoso, configurarlo y mantenerlo es bastante complicado. Necesita configurar un clúster de computadoras instalar todas las dependencias correctas, manejar la red entre ellas, monitorear su desempeño, escalar  más recursos, etc.

## Databricks
Un servicio completo que proporciona todo lo que se necesita para trabajar con Spark sin preocuparse por la infraestructura técnica detrás.

Ofrece: 
- Clústeres de Spark preconfigurados, se puede iniciar con un clic. 
- Notebooks interactivos se escribe y ejecuta código de PySpark de manera visual y colaborativa, similar a Jupyter.
- Administración automática de recursos, donde el clúster puede crecer o disminuir según tus necesidades.
- Herramientas para orquestar trabajos, visualizar datos, colaborar con tu equipo, gestionar todo el ciclo de vida de tus proyectos datos



## Estándares de Código

Este proyecto sigue [PEP 8](https://pep8.org/) y nuestras [convenciones internas](docs/CODING_STANDARDS.md).

**Antes de hacer commit:**
- Revisar naming conventions
- Agregar docstrings a funciones nuevas
- Comentar decisiones de diseño no obvias
