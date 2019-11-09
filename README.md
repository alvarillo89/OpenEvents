[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/alvarillo89/UGR-CC-Project.svg?branch=master)](https://travis-ci.com/alvarillo89/UGR-CC-Project)
[![codecov](https://codecov.io/gh/alvarillo89/UGR-CC-Project/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarillo89/UGR-CC-Project)

# Proyecto de la asignatura Cloud Computing (UGR)

Puede consultar cómo se configuró Git y Github para el proyecto en [este enlace.](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/hito0.md)

## OpenEvent

`OpenEvent` es una aplicación open source que permite a organizadores de cualquier tipo publicar información sobre sus eventos y vender entradas para los mismos mediante pagos electrónicos. Todo ello a través de la nube.

### Arquitectura e Infraestructura

La aplicación se implementará siguiendo una arquitectura basada en microservicios. Puede consultar con mayor detalle la *Arquitectura e Infraestructura* del proyecto en el [siguiente enlace](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/hito1.md).

---

### Prerrequisitos y versiones

+ Mínima versión de Python compatible:  3.4 
+ Máxima versión de Python compatible:  3.8 (incluída la versión en desarrollo)

> *Nota: en Windows solo se ha comprobado hasta la versión 3.7, se desconoce el comportamiento para la versión 3.8*.

Adicionalmente, deberá disponerse de la herramienta `Makefile`.

---

### Herramienta de construcción

`buildtool: Makefile`

Este proyecto utiliza `Makefile` como herramienta de construcción. Los objetivos configurados son los siguientes:

```
make install
```

*Instala todos los requisitos necesarios para la aplicación. Alternativamente a esto puede ejecutar `pip install -r requirements.txt`*.

```
make test
```

*Ejecuta los tests del proyecto, tanto tests unitarios como de cobertura.*

```
make clean
```

*Limpia el directorio del proyecto, eliminando los directorios `__pycache__` y el archivo `.coverage` resultante de los test de cobertura.*

Para más detalles, consulte el [fichero Makefile](https://github.com/alvarillo89/UGR-CC-Project/blob/master/Makefile), el cual contiene comentarios explicativos. 