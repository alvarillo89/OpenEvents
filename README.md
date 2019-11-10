[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/alvarillo89/UGR-CC-Project.svg?branch=master)](https://travis-ci.com/alvarillo89/UGR-CC-Project)
[![codecov](https://codecov.io/gh/alvarillo89/UGR-CC-Project/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarillo89/UGR-CC-Project)

# Proyecto de la asignatura Cloud Computing (UGR)

Puede consultar cómo se configuró Git y Github para el proyecto en [este enlace.](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/hito0.md)

## OpenEvent

`OpenEvent` es una aplicación open source que permite a organizadores de cualquier tipo publicar información sobre sus eventos y vender entradas para los mismos mediante pagos electrónicos. Todo ello a través de la nube.

### Arquitectura e Infraestructura

La aplicación se implementa siguiendo una arquitectura basada en microservicios. Puede consultar con mayor detalle la *Arquitectura e Infraestructura* del proyecto en el [siguiente enlace](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/hito1.md).

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

---

### Integración contínua

El proyecto utiliza dos sistemas de integración contínua diferentes: `Travis-CI` y `GitHub Actions`. A continuación se describen las funciones que desempeñan cada uno de ellos:

+ Travis-CI: se encarga de ejecutar los tests unitarios y de cobertura para la clase `Events`. Además, comprueba que dichos tests se ejecutan correctamente para las versiones 3.4, 3.5, 3.6, 3.6.8 (la utilizada localmente para el desarrollo), 3.7, 3.8 (estable) y 3.8 (desarrollo) de Python, sobre el sistema operativo Linux. Por último, envía los resultados de los test de cobertura a la plataforma Codecov.

Para más información consulte el [fichero de configuración de Travis](https://github.com/alvarillo89/UGR-CC-Project/blob/master/.travis.yml), el cual incluye comentarios explicativos.

+ GitHub Actions: se ha escogido esta segunda alternativa por ser totalmente novedosa y porque es una herramienta propia de GitHub que no requiere de ningún software de terceros. Se encarga de ejecutar los test unitarios y de cobertura desde la versión 3.4 de Python hasta la 3.7 (la 3.8 aún no cuenta con soporte en el sistema). A diferencia del anterior, ejecuta los test sobre la plataforma Windows para comprobar la compatibilidad con dicho sistema operativo. Este workflow se ejecuta cada vez que se realiza un push al repositorio.

Para más información consulte el [fichero de configuración del workflow](https://github.com/alvarillo89/UGR-CC-Project/blob/master/.github/workflows/WindowsTest.yml), el cual incluye comentarios explicativos.

> **Nota:** para los test unitarios se ha utilizado `unittest`, simplemente porque ya está incorporado en la propia ditribución de Python y no requiere
de la instalación de un módulo externo. Para los test de cobertura se ha utilizado `coverage.py`, que es aquel que recomienda `Codecov` para realizar
test de cobertura conjuntamente con unittest.
