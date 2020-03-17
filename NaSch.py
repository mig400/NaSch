# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:54:09 2020

@author: Miguel_Ángel
"""

# =============================================================================
# prueba modelos NaSch orientada a objetos
# tipo rotonda , sin semaforos , sin incorporaciones , vehiculos del mismo tipo , un carril
# =============================================================================


import numpy as np
import matplotlib.pyplot as plt


class carretera:
    def __init__(self,longitud,densidad):   # 
        self.longitud = longitud            # nº casillas  4metros/casilla
        self.densidad = densidad            # densiad de coches en la calzada


    def generar_casillas(self):
        vector_espacio = np.linspace( 0 , self.longitud-1 , num= self.longitud , dtype = int)  
        return vector_espacio



class tiempo:
    def __init__(self,tiempo_simulacion) :
        self.tiempo_simulacion = tiempo_simulacion


    def linea_tiempo(self):
        vector_tiempo = np.linspace(0 , self.tiempo_simulacion , num = self.tiempo_simulacion + 1)
        return vector_tiempo    


class coche:
    def __init__(self, nombre , v , vmax , pos):   # cada coche es un obleto
        self.nombre = nombre
        self.v = v
        self.vmax = vmax
        self.pos = pos


class simulacion(coche):
  
    def crear_carretera(longitud,densidad):      # crea vector carretera 
        carretera1 = carretera(longitud , densidad ) 
        vector_espacio = carretera1.generar_casillas()
        return vector_espacio


    
    def crear_linea_tiempo (tiempo_simulacion) :  #crea vector tiempo
        tiempo1 = tiempo(tiempo_simulacion)
        vector_tiempo = tiempo1.linea_tiempo()
        return vector_tiempo


    def estado_inicial (vector_espacio , densidad , vmax):      # setea v y pos de cada coche inicial

        N = round(densidad*len(vector_espacio))                               # obtenemos el numero de coches
        pos_coches = np.random.choice(vector_espacio, size = N , replace = False)# N huecos de la carretera aletorios 
        pos_coches.sort()                                                     # asegura que el coche0 tendra siempre
        info_coches_inicial = {}                                              # diccionario que almacena los objetos cochee
        for i in range(0,N):                                                  # crea los objetos coche
             info_coches_inicial['Coche'+str(i)] = coche('Coche'+str(i) , 0 , vmax , pos_coches[i])
        return info_coches_inicial     

        
    def situacion_instantanea (info_coches , longitud , vmax):  # mueve los coches segun las reglas


        pos_coche0 = info_coches['Coche'+str(0)].pos # guarda info del 1er coche para que el ultimo decida
        vector_velocidad = [0]*len(info_coches)       # resetea vectores
        vector_posicion = [0]*len(info_coches)
        
        
        for i in range(0,len(info_coches)-1) :      # bucle para cada coche (ultimo no)
            
            
            v = info_coches['Coche'+str(i)].v
            pos = info_coches['Coche'+str(i)].pos
            pos_delante = info_coches['Coche'+str(i+1)].pos
            vector_velocidad[i] = v                             # para representar datos
            vector_posicion[i] = pos
            
            v = min(v + 1 , vmax)                               # PASO 1 : si v no es max el condctr acelera
            if pos < pos_delante :                              # PASO 2 : v < que distancia con el de delante (NO CHOCAR)
                v = min(v , pos_delante - pos - 1)              # si el vehiculo i es el ultimo en la carretera
            else:
                v = min(v , longitud - pos - 1 + pos_delante)
            if np.random.randint(1,10)>8 and v > 0:             # PASO 3 : frenado aleatorio de probabilidad 'p' si v>0(evita march atras)    
                v = v - 1
            if pos + v <= longitud-1 :                          # PASO 4: movimiento del coche
                pos = pos + v                                        # NOTA ; Esta funcion pensada para paso de t=unidad
            else:                                               # si llega al final  aplicar Cond.C periodicas
                pos = pos + v - longitud
            
            info_coches['Coche'+str(i)].v = v                   # objeto coche nuevas variables
            info_coches['Coche'+str(i)].pos = pos
           
       
        vector_velocidad[i] = v                                 # los cambios se actlz en el sig bucle 
        vector_posicion[i] = pos                                # aqui los cmbs del ultim paso
       
        v = info_coches['Coche'+str(i+1)].v                     # solo nos queda mover al ultimo coche 
        pos = info_coches['Coche'+str(i+1)].pos
        pos_delante = pos_coche0
        vector_velocidad[i+1] = v
        vector_posicion[i+1] = pos
        
        v = min(v + 1 , vmax)
        if pos < pos_delante :  
            v = min(v , pos_delante - pos - 1)
        else:
            v = min(v , longitud - pos - 1 + pos_delante)
        if np.random.randint(1,10)>8 and v > 0: 
            v = v - 1
        if pos + v <= longitud-1 :
            pos = pos +  v
        else:
            pos = pos + v - longitud            
        info_coches['Coche'+str(i+1)].v = v
        info_coches['Coche'+str(i+1)].pos = pos
        
        
        return info_coches , vector_velocidad , vector_posicion  # todas las nuevas variables del trafico actualizadas
    
    
    def lanzar_simulacion(longitud,densidad,tiempo_simulacion,vmax):       # metodo que lanza la iteracion temporal
       
        vector_espacio   = simulacion.crear_carretera(longitud,densidad)          # inicializamos los elementos de simulac
        info_coches      = simulacion.estado_inicial(vector_espacio,densidad,vmax)
        matriz_velocidad = np.zeros((tiempo_simulacion, len(info_coches)),dtype=int)
        matriz_posicion  = np.zeros((tiempo_simulacion, longitud),dtype=int)

        for i in range(0,tiempo_simulacion):                                    # ejecutamos en el tiempo
            info_coches , matriz_velocidad[i,:] , vector_posicion = simulacion.situacion_instantanea(info_coches,longitud,vmax)
            
            for idx, val in enumerate(vector_posicion):              # rellena  matriz posicion-->con los datos de velociad
                    matriz_posicion[i,val]=matriz_velocidad[i,idx]+5    

        return  matriz_posicion  ,  matriz_velocidad


class analisis:
    
    def grafica_posicion (matriz_posicion):
       
        plt.imshow(matriz_posicion, interpolation = 'nearest' , cmap = 'Blues_r' , rasterized=True)
        cbar = plt.colorbar()
        cbar.set_label('Velocidad')
        plt.xlabel = 'Espacio'
        plt.ylabel ='Tiempo'
        plt.tight_layout()
        plt.show()

    def grafica_v_med(longitud,tiempo_simulacion,vmax):
        v_media = [0]*10
        for densidad in range (1,11):
            Mp , Mv = simulacion.lanzar_simulacion(longitud,densidad/10,tiempo_simulacion,vmax)
            v_media[densidad-1] = np.mean(Mv, dtype = int)
        x_axis = np.arange(0.0,1.,0.1)
        plt.plot(x_axis,v_media)
        plt.xlabel = 'density' 
        plt.ylabel = 'average velocity'
        plt.style.use('ggplot')
        plt.show()





# =============================================================================
# PROGRAMA MAIN
# =============================================================================
Mp , Mv = simulacion.lanzar_simulacion(10000,0.3,1000,5)
analisis.grafica_posicion(Mp)
#analisis.grafica_v_med(100,100,5)
 

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            