# Integradora-1-Mesa

#### Integrantes del Equipo: 
Diana Karen Melo, Miguel Medina y Andrés Briseño.
___
#### Descripción del Reto: 
Este proyecto utiliza Mesa para el modelado multiagente .
___
#### Comportamiento de Agentes Involucrados: 
* Robots - Cargadores de cajas: 
  > El agente tiene caja y esta en la base &rarr; La deja en la base y busca una nueva
  
  > Tiene caja  &rarr; Avanza a la base
  
  > Hay una caja en la misma celda y aun no tiene caja  &rarr; Se le asigna la caja y se dirije a la base.
  
  > No tiene caja y aún no sabe donde hay cajas en el grid -> Se mueve random hasta encontrar una caja a sus alrededores
  
  > No tiene caja y llegó a donde creía que hay una caja (Se le llevo otro robot) &rarr; Recalcula el camino hacia otra caja
  
* Cajas:
  >  Si su posicion es la base &rarr; Cambia su estado a "base"
___
#### Unity: 
