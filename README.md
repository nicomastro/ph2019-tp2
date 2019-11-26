# ph2019-tp2

Escribo acá lo que pasaríamos luego al informe en pdf. Me gustó este template de latex :D

https://es.overleaf.com/project/5ddcce4d05f3eb0001935577
## Dominio del TP:

El reconocedor de habla que implementamos está pensado con la intención de ser un "asistente" especializado en la reproducción y control de una biblioteca de archivos de audios, como canciones. 

### Funcionalidades Implementadas:

### Reproducir:
Para interactuar con el sistema, el usuario pronunciará comandos hablados sencillos como "reproducir canción de X" o "reproducir canciones de Y".
Para el segundo caso, se elige alguna canción de la banda Y para reproducir en caso de haber más de una. En cualquier caso se le informará al usuario a través de un audio con voz sintetizada, el resultado de su orden.

### Pausar:

A su vez, en cualquier momento se le puede indicar al sistema que pause la canción o que la reanude.
Actualmente, el sistema es bastante restrictivo y son pocas las variantes de las directivas que puede comprender. Se hablará de esto en la sección correspondiente a la arquitectura.

### Listar:

En caso de querer conocer ciertas canciones disponibles en la biblioteca, se podrá pedir que el sistema sintetice las lista de canciones de una determinada banda para que luego el usuario pueda elegir cual reproducir. En prinicipio, se enunciaran todas pero la intención es que, a futuro, solo se presente una cantidad muy restringida y que el usuario decida si quiere continuar escuchando la lista, recibiendo prompts cada vez más cortos.


### A futuro:

Como funcionalidades adicionales a explorar, se podría pensar en comandos para alterar la forma de reproducción (pasar a la próxima/anterior, reproducir aleatorio), controlar volumen, cambiar velocidad de reproducción, etc.



## Arquitectura del SDH:

Algunos problemas con los que lidiar:

### Reconocimiento del habla:
```
* Familiaridad del usuario con el sistema
* Producción del habla: Acento, edad, sexo
* Medio ambiente: ruido de fondo, interferencias
```

### Comprensión del lenguaje:
```
* Frame semantics: Determinar una gramática semántica
* Problemas de implicaturas
```
### Administrador de diálogo:
```
* System initiative (FSA) vs User initiative, open prompt
* Confirmación implícita, progressive prompting
```
### Generación del Lenguaje:
```
* Elección de la estructura sintáctica y palabras
* Marcadores de discurso (coherencia)
* Prompts cada vez más cortos
* Problemas de implicaturas
```

### Síntesis del habla:
```
* Dominio abierto vs limitado
* Nombres propios
```





