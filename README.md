# ph2019-tp2

## Dominio del TP:

Para el TP pensamos hacer un sistema al cual le podemos dar una instrucción para que reproduzca una canción dada por nombre o que reproduzca alguna dada por grupo/cantante.
La idea sería tener una especie de base de datos con nombre de canción y grupo/cantante.

El usuario puede decir algo como "Reproducir canción X" o "Reproducir canciones de Y". Si no encuentra ninguna, informa que no tiene "esa canción X o ese grupo Y". Si encuentra va a responder algo como "Reproduciendo canción X" o "Reproduciendo canciones de Y". En cualquier momento se le puede indicar al sistema que pause la canción.

Como funcionalidades adicionales a explorar, se podría pensar en comandos para listar canciones, comandos para alterar la forma de reproducción (pasar a la próxima/anterior, reproducir aleatorio), controlar volumen, cambiar velocidad de reproducción, etc.


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





