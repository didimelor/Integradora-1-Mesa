# Integradora-1-Mesa

#### Integrantes del Equipo: 
Diana Karen Melo, Miguel Medina y Andrés Briseño.
___
#### Descripción del Reto: 
Este proyecto utiliza Mesa para el modelado multiagente .
___
#### Agentes Involucrados: 
* Robots - Cargadores de cajas: 
  > El semáforo se encuentra en rojo &rarr; Quedarse en el mismo lugar 
  
  > Hay un coche en la dirección en la que se dirije  &rarr; Quedarse en el mismo lugar 
  
  > Hay un obstáculo en la dirección en la que se dirije  &rarr; Moverse hacia la dirección de la calle y "rodearlo" siempre intentando regresar a la dirección que lo lleve al destino.
  
  > Iteraciones intentando ir a la dirección deseada se excedieron -> ir a dirección random.
* Cajas:
> Pasó el tiempo máximo en estado rojo &rarr; Se cambia a estado verde
