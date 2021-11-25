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
#### ¿Cómo se calcula la ruta para el robot?: 
  > Cada robot tiene como atributo la posición de la base. En la función move con caja se calcula la distancia hacia "x" y "y", si ambas distancias son cero significa que llegó al lugar. Si no, se crea una lista de prioridad llamada directions. La primera posición es dirijirse a la dirección que le quede más distancia por recorrer, por ende, la última prioridad es dirijirse al lado contrario. El indice uno es dirijirse a la dirección a donde quede menos distancia y el indice dos es el lado contario de la dirección a donde quede menos distancia. 
#### Ejemplo: 


![This is an image](https://github.com/didimelor/Integradora-1-Mesa/blob/main/(-1%2C0).png)

Se itera por la lista de direcciones, se mueve el agente a la primera posición en donde no haya obstáculo.
___
#### Unity: 
#### ¿Cómo funciona?
Para esta parte, lo primero que se hace es instanciar todo el ambiente (paredes, piso, agentes y cajas) de acuerdo a los parámetros dados en el editor de Unity. Una vez que se tiene todo configurado, se le mandan los parámetros al modelo de Python por medio de un web request de Unity. Una vez con el los parámetros dados, se reciben las posiciones iniciales del modelo para empezar a correrlo, éstos se reciben por medio de los endpoints en el servidor de Flask.

De igual manera, cada llamada del update hace un request a los diferentes endpoints del servidor de Flask, que reportan las posiciones de los agentes, así como el estado de la simulación. En base a esta información, representan los movimientos dentro de Unity por medio de cambios en el transform.position de cada agente (robots y cajas), para los robots también se toma en cuenta a qué dirección se dirige para rotarlos hacia donde van.

#### Mejoras
Una de las mejoras que se puede hacer a esta parte es la interpolación de los movimientos, para que no se vea tan irreal, pues con la implementación actual hay ocasiones donde la interpolación se realiza entre las posiciones de dos agentes diferentes, gracias a la manera en la que se va iterando sobre el grid para obtener sus posiciones y la manera en la que se les asignan a las instancias de los robots y las cajas.

Por otro lado, se pueden poner animaciones a los robots para cuando recogen las cajas, que las tengan sobre ellos, por ejemplo, así como subir la coordenada en Y de las cajas para que concuerden con la animación de cargar. Sobre el mismo tema, la animación de caminar se podría ajustar a la par de la interpolación para dar una mejor ilusión de movimiento.


Otros detalles que se pueden agregar, pero que no son vitales podrían ser: agregar una pantalla de finalización que contenga los datos generados durante el tiempo de ejecución del modelo (sugerencia del profe Gil), tener la opción de seguir a distintos robots con otras cámaras, detallar más la escena para dar una mejor apariencia de acuerdo a la temática (almacén, calle, casa, etc.).
