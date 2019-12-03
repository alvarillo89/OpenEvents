# Comparación de prestaciones de diferentes contenedores Docker

A la hora de decidir cuál será el sistema operativo (o imagen base) que utilizaremos para el contenedor del  microservicio, debemos realizar un estudio comparativo entre diferentes alternativas y quedarnos con aquella que proporcione el mejor desempeño para nuestro sistema.

Concretamente, para el microservicio `Events`, se ha probado con las siguientes imágenes:
+ La imagen oficial de `python3.6.8`.
+ `Alpine` como SO y el intérprete de `python3.6.8`.
+ `minideb` (una versión simplificada y ligera de debian) como SO y el intérprete de `python3`.
+ `Fedora` como SO y el intérprete de `python3`.

Los `dockerfiles` de todas ellas son idénticos. Lo único que varía de una a otra es la imagen base y la instalación de `python`:

+ Para `Alpine`:

```dockerfile
FROM python:3.6.8-alpine
# Python ya está instalado.
```

+ Para `python3.6.8`:

```dockerfile
FROM python:3.6.8
```

+ Para `minideb`:

```dockerfile
FROM bitnami/minideb:latest
RUN install_packages python3 python3-pip 
```

+ Para `Fedora`:

```dockerfile
FROM fedora:latest
RUN dnf install python3 python3-pip -y
```

Por último, para evaluar cada una de las alternativas, se han tenido en cuenta dos criterios: el tamaño final de la imagen y las prestaciones a la hora de atender múltiples peticiones.

## Tamaño de las imágenes

Tras construirlas, si ejecutamos el comando `docker images`, podemos consultar el tamaño de cada una de las imágenes presentes en el sistema:

```None
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
fedora-python       latest              3fa4ab7e5af1        7 minutes ago       440MB
minideb-python      latest              c2ae2cfe2722        18 minutes ago      136MB
only-python         latest              cbe6ddfe5193        16 hours ago        954MB
alpine-python       latest              78327180c648        16 hours ago        94.3MB
```

Según este criterio, el claro ganador es `Alpine` (aunque `minideb` es un fuerte competidor). También llama la atención que la imagen oficial de `Python` ocupa más del doble que la imagen de `Fedora`.

## Prestaciones al atender peticiones

Para la evaluación de este criterio, se ha utilizado **Apache Benchmark** (`ab`):

```None
$ ab -n 100 -c 10 http://localhost:8080/event/title/myevent
```
Esto realizará 100 peticiones con una concurrencia de 10 por unidad de tiempo sobre el recurso `myevent`. A continuación se muestran los resultados:

+ Para `Alpine`:

```
Document Path:          /event/title/myevent
Document Length:        17 bytes

Concurrency Level:      10
Time taken for tests:   0.019 seconds
Complete requests:      100
Failed requests:        0
Non-2xx responses:      100
Total transferred:      19100 bytes
HTML transferred:       1700 bytes
Requests per second:    5267.04 [#/sec] (mean)
Time per request:       1.899 [ms] (mean)
Time per request:       0.190 [ms] (mean, across all concurrent requests)
Transfer rate:          982.43 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       0
Processing:     1    2   1.9      1       8
Waiting:        0    2   1.9      1       8
Total:          1    2   2.0      1       8

Percentage of the requests served within a certain time (ms)
  50%      1
  66%      1
  75%      1
  80%      2
  90%      7
  95%      8
  98%      8
  99%      8
 100%      8 (longest request)
```
+ Para `python3.6.8`:

```
Document Path:          /event/title/myevent
Document Length:        17 bytes

Concurrency Level:      10
Time taken for tests:   0.019 seconds
Complete requests:      100
Failed requests:        0
Non-2xx responses:      100
Total transferred:      19100 bytes
HTML transferred:       1700 bytes
Requests per second:    5212.41 [#/sec] (mean)
Time per request:       1.919 [ms] (mean)
Time per request:       0.192 [ms] (mean, across all concurrent requests)
Transfer rate:          972.24 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     1    2   2.1      1       9
Waiting:        1    2   2.1      1       9
Total:          1    2   2.2      1       9

Percentage of the requests served within a certain time (ms)
  50%      1
  66%      1
  75%      1
  80%      2
  90%      8
  95%      8
  98%      9
  99%      9
 100%      9 (longest request)
```

- Para `minideb`:

```
Document Path:          /event/title/myevent
Document Length:        17 bytes

Concurrency Level:      10
Time taken for tests:   0.017 seconds
Complete requests:      100
Failed requests:        0
Non-2xx responses:      100
Total transferred:      19100 bytes
HTML transferred:       1700 bytes
Requests per second:    5750.43 [#/sec] (mean)
Time per request:       1.739 [ms] (mean)
Time per request:       0.174 [ms] (mean, across all concurrent requests)
Transfer rate:          1072.59 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       0
Processing:     0    2   1.7      1       7
Waiting:        0    2   1.7      1       7
Total:          1    2   1.8      1       7

Percentage of the requests served within a certain time (ms)
  50%      1
  66%      1
  75%      1
  80%      2
  90%      6
  95%      7
  98%      7
  99%      7
 100%      7 (longest request)
```

- Para `Fedora`:

```
Document Path:          /event/title/myevent
Document Length:        17 bytes

Concurrency Level:      10
Time taken for tests:   0.017 seconds
Complete requests:      100
Failed requests:        0
Non-2xx responses:      100
Total transferred:      19100 bytes
HTML transferred:       1700 bytes
Requests per second:    5841.46 [#/sec] (mean)
Time per request:       1.712 [ms] (mean)
Time per request:       0.171 [ms] (mean, across all concurrent requests)
Transfer rate:          1089.57 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       1
Processing:     1    1   1.6      1       7
Waiting:        1    1   1.6      1       7
Total:          1    2   1.9      1       8

Percentage of the requests served within a certain time (ms)
  50%      1
  66%      1
  75%      1
  80%      1
  90%      6
  95%      7
  98%      8
  99%      8
 100%      8 (longest request)
```

Para que sea más sencillo realizar la comparativa, en la siguiente tabla se muestran los campos más relevantes de cada uno de los informes:

| Container      | Requests per second | Time per request (mean) | Longest request |
|----------------|---------------------|-------------------------|-----------------|
| alpine-python  | 5267.04 [#/sec]     | 1.899 [ms]              | 8               |
| only-python    | 5212.41 [#/sec]     | 1.919 [ms]              | 9               |
| minideb-python | 5750.43 [#/sec]     | 1.739 [ms]              | 7               |
| fedora-python  | 5841.46 [#/sec]     | 1.712 [ms]              | 8               |

El que peor rendimiento presenta es el contenedor con la imagen oficial de `Python` y el que mejores prestaciones evidencia es `Fedora`.

## Elección final

Por el criterio del tamaño deberíamos elegir `Alpine` y según el criterio del rendimiento deberíamos elegir `Fedora`. No obstante, existe una imagen que presenta un buen equilibrio entre ambas: `minideb`. Tiene un tamaño de 136MB y presenta un rendimiento muy similar al de `Fedora`.

**En definitiva, utilizaremos `minideb` como imagen base para el contenedor del microservicio `Events`.**