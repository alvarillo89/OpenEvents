### Integración contínua

El proyecto utiliza dos sistemas de integración contínua diferentes: `Travis-CI` y `GitHub Actions`. A continuación se describen las funciones que desempeñan cada uno de ellos:

+ Travis-CI: se encarga de ejecutar los tests unitarios, de integración y de cobertura sobre ambos microservicios. Además, comprueba que dichos tests se ejecutan correctamente para las versiones 3.5, 3.6, 3.6.8 (la utilizada localmente para el desarrollo), 3.7, 3.8 (estable) y 3.8 (desarrollo) de Python, sobre el sistema operativo Linux. Por último, envía los resultados de los test de cobertura a la plataforma Codecov.

Para más información consulte el [**fichero de configuración de Travis**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/.travis.yml), el cual incluye comentarios explicativos.

+ GitHub Actions: se ha escogido esta segunda alternativa por ser totalmente novedosa y porque es una herramienta propia de GitHub que no requiere de ningún software de terceros. Se encarga de ejecutar los test unitarios y de integración desde la versión 3.5 de Python hasta la 3.7 (la 3.8 aún no cuenta con soporte en el sistema). A diferencia del anterior, ejecuta los test sobre la plataforma Windows para comprobar la compatibilidad con dicho sistema operativo, pero solo sobre el microservicio `Events`, puesto que como ya se mencionó en el `README`, el segundo no es compatible con este sistema operativo. Este workflow se ejecuta cada vez que se realiza un push al repositorio.

Para más información consulte el [**fichero de configuración del workflow**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/.github/workflows/WindowsTest.yml), el cual incluye comentarios explicativos.
