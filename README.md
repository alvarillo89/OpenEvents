# Proyecto de la asignatura Cloud Computing (UGR)

Puede consultar cómo se configuró Git y Github para el proyecto en [este enlace.](https://github.com/alvarillo89/UGR-CC-Project/blob/master/doc/hito0.md)

## OpenEvent

`OpenEvent` es una aplicación open source que permite a organizadores de cualquier tipo publicar información sobre sus eventos y vender entradas para los mismos mediante pagos electrónicos. Todo ello a través de la nube.

#### Entidades del dominio del problema:

Las entidades en las que se puede dividir el dominio del problema son las siguientes:

+ Evento: un evento es un suceso social, artístico o deportivo que se encuentra previamente programado. Está formado por un organizador, un título, la fecha y hora en la que se producirá, su dirección, una descripción, el número de entradas disponibles, el coste de las mismas y los datos de pago del organizador. A su vez, las funcionalidades asociadas a esta entidad son: 
    - Creación de un nuevo evento.
    - Modificación, por parte del organizador, de algunos datos de un evento existente.
    - Eliminación de un evento existente.
    - Consulta de los datos de un evento.
+ Entrada: una entrada es el documento que acredita a una persona para el acceso a un determinado evento. Está formada por el título del evento al que pertenece, el nombre del propietario de la entrada y un código de validación. Las funcionalidades asociadas son:
    + Comprar una entrada, procesando el pago correspondiente.
    + Generar el documento que representa la entrada y que deberá ser presentado en el evento. Incluye el código de validación.
    + Consultar si una entrada es válida o no, a partir de su código de validación.


#### Arquitectura:

La aplicación se implementará siguiendo una arquitectura basada en microservicios. Cada una de las entidades del dominio del problema extraídas en el apartado anterior se asociarán a un microservicio diferente: 

+ `EventManager`: este microservicio implementará todas las funcionalidades asociadas con la entidad `Evento`.
+ `TicketManager`: se encargará de procesar el pago de una determinada entrada y generar el documento asociado. Al mismo tiempo, almacenará el registro de pago y el código de validación de la misma para futuras comprobaciones. 

Aquí se muestra un grafo con la arquitectura de la aplicación:

![](doc/imgs/Hito0/Arquitectura.png)

Como puede observarse, se empleará una API Gateway que actúe como enrutador entre los distintos microservicios. Además, cada uno de ellos dispondrá de su propia API Rest para las comunicaciones.

#### Tecnologías y lenguajes:

Se plantea realizar una implementación políglota, es decir, cada microservicio empleará un lenguaje diferente:

+ `EventManager`: se implementará en `Ruby`.
+ `TicketManager`: se implementará en `Python`, el cual proporciona módulos que facilitan la realización de las funcionalidades que proporciona este microservicio, tales como generar códigos y PDFs.

Por último, para el sistema de configuración distribuida se utilizará [etcd](https://etcd.io/).

#### Almacenes de datos:

Se necesita almacenar lo siguiente:

- Datos de Eventos.
- Registros de pago de las entradas y códigos de validación para futuras comprobaciones.

Puesto que lo que nos interesa es recuperar eficientemente información (ya sea de eventos o de pagos realizados) a partir de identificadores (como puede ser el identificador del evento o el código de validación de una entrada) utilizaremos almacenes de datos basados en clave-valor, como por ejemplo [Apache Cassandra](http://cassandra.apache.org/).