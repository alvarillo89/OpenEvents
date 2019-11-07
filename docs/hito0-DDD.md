# Entidades del dominio del problema:

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
