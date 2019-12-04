# Despliegue en Heroku

> Nota: se ha escogido heroku por cuatro motivos: es gratis, es sencillo de utilizar, su documentación es excelente y tenía curiosidad por trabajar con él.

Una vez instalada la herramienta de comandos de interfaz de heroku (`Heroku CLI`) y tras habernos logueado en nuestra cuenta, el proceso de despliegue en heroku es sencillo:

1. Crear una aplicación de heroku tecleando `heroku create openevents`. Esto añadirá a nuestro repositorio de Git un nuevo `remote` llamado heroku. A su vez, creará la aplicación de Heroku bajo el nombre `openevents`.
2. Crear el fichero `heroku.yml`, un manifest que contiene la definición de nuestra aplicación y commitearlo al repositorio. Para más información sobre su contenido, consulte el propio [**fichero**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/heroku.yml), el cual contiene comentarios explicativos.
3. Establecer el stack *(la imagen del SO)* de la aplicación a `container` con el siguiente comando: `heroku stack:set container`. Con esto indicamos que se utilizará docker.
4. Pushear la imagen a heroku con el comando `git push heroku master`.

Y listo. Con esto, la aplicación estará deplegada en la dirección especificada en el `README.md`.

El siguiente paso es, desde la página web de Heroku, conectar la aplicación al repositorio de GitHub que contiene el código de la aplicación. De esta forma, Heroku se encargará de automatizar el despliegue cada vez que se realice un nuevo push al repositorio. Las siguientes capturas muestran el proceso:

1. Conectar Github y el repositorio a la aplicación de Heroku:

![](imgs/resources3/herokuGithub.png)

2. Activamos la casilla *Wait for CI to pass before deploy* (de esta forma nos aseguramos de que la apliación no se despliega hasta que no se pasan todos los tests de integración continua) y activamos los depliegues automáticos.

![](imgs/resources3/herokuTestCI.png)

3. Y listo, con esto el despliegue automático en Heroku estaría configurado:

![](imgs/resources3/herokuAutomatedDeploy.png)

