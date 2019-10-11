# Proyecto de la asignatura Cloud Computing (UGR)

Puede consultar la documentación adicional a la entrega del hito 0 en [este enlace.](https://github.com/alvarillo89/UGR-CC-Project/blob/master/doc/hito0.md)

## Virtual Safe Box

#### Descripción:

Se plantea la creación de una aplicación de almacenamiento en la nube, con la particularidad
de que esta actuará como una *"Caja Fuerte Virtual"*, es decir, todos aquellos archivos y
documentos que se almacenen remotamente permanecerán encriptados para brindar una seguridad 
extra al usuario. Está pensada como un lugar seguro en el que almacenar ficheros sensibles.

#### Funcionalidad:

Los usuarios deberán registrarse con un nombre de usuario y una contraseña. Además,
podrán establecer una clave maestra para desencriptar todos sus archivos o especificar
una clave concreta para cada uno de ellos. Por supuesto, las comunicaciones entre los
distintos servicios deberán realizarse también de forma segura.

#### Arquitectura:

La aplicación se implementará siguiendo un patrón (o arquitectura) basado en microservicios, cuyo núcleo será un API (en principio basado en REST) y empleando comunicación mediante mensajería asíncrona.

A priori, serán necesarios los siguientes servicios, aunque esta lista puede variar:

- Registro y login de usuarios.
- Recepción, encriptado y almacenamiento de ficheros.
- Recuperación, desencriptado y envío de ficheros. 

#### Lenguajes:

En principio, el lenguaje principal de la aplicación será `Ruby`. No obstante, no se descarta
realizar una implementación políglota, especialmente si se encuentra algún lenguaje que aporte buenas herramientas para todo lo relacionado con la criptografía.

#### Almacenes de datos:

Se necesita almacenar lo siguiente:

- Datos de usuarios (login, contraseña y claves).
- Ficheros/archivos subidos a la plataforma por cada usuario.

Puesto que no todos los archivos que almacenarán los usuarios tendrán la misma estructura, para esta aplicación resulta más útil utilizar una base de datos NoSQL.