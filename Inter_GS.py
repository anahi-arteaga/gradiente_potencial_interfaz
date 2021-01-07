# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 00:03:01 2021

@author: anahi
"""

import numpy as np
import math 
import matplotlib.pyplot as plt
import tkinter as tk 
import pandas as pd

ventana= tk.Tk()
ventana.title("Calculo de voltaje y potencial")
ventana.geometry('700x400')
ventana.configure(background='blue')
var=tk.StringVar()


gs =tk.Label(ventana,text="GRADIENTE SALINO",
             bg="red",fg="yellow")
gs.place(x=10,y=10, width=690, height=50)

Nm =tk.Label(ventana,text="Ingrese el número de membranas pares:",bg="black",fg="white")
Nm.place(x=25,y=70, width=300, height=30)
entrada1=tk.Entry(ventana)
entrada1.place(x=80,y=105, width=200, height=30)

Ari =tk.Label(ventana,text="Ingrese el area de las membranas (m^2):",bg="black",fg="white")
Ari.place(x=380,y=70, width=300, height=30)
entrada2=tk.Entry(ventana)
entrada2.place(x=430,y=105, width=200, height=30)

Conc =tk.Label(ventana,text="Ingrese la concentración concentrada:",bg="black",fg="white")
Conc.place(x=25,y=145, width=300, height=30)
entrada3=tk.Entry(ventana)
entrada3.place(x=80,y=180, width=200, height=30)

Cond =tk.Label(ventana,text="Ingrese la concentración diluida:",bg="black",fg="white")
Cond.place(x=380,y=145, width=300, height=30)
entrada4=tk.Entry(ventana)
entrada4.place(x=430,y=180, width=200, height=30)

#DATOS DE LAS MEMBRANAS
Pcem = float(0.92)
Paem = float(0.92)
Raem = float(0.013)
Rcem = float(0.027)
T = float(25+273.15)   #temperatura en grados Kelvin
R = float(8.314)  #Constante universal de los gases J/molK
CF = float(96485.3365)  #Constante de Faraday C/mol
z = float(1**2)   #valencia
Es = float(0.0005) # Espaciamiento de membranas 
Re =np.array([92,47,22,10,6.8,5.6,4.7,3.3,2.2,1.8,1.2,0.56,0.39,0.22,0.1,0])

# coeficiente de actividad 
ANa = 450 #radio de efectividad del ion hidratado 
ACl = 300

def Ecell():
    
    Ai = float(entrada2.get())
    Cc = float(entrada3.get())
    Cd = float(entrada4.get())
    N = int(entrada1.get())
    gnac = math.exp((-0.5*z*math.sqrt(Cc))/(1+(ANa/305)*math.sqrt(Cc)))
    gnad = math.exp((-0.5*z*math.sqrt(Cd))/(1+(ANa/305)*math.sqrt(Cd)))
    gclc = math.exp((-0.5*z*math.sqrt(Cc))/(1+(ACl/305)*math.sqrt(Cc)))
    gcld = math.exp((-0.5*z*math.sqrt(Cd))/(1+(ACl/305)*math.sqrt(Cd)))

    acem = math.log((gnac*Cc)/(gnad*Cd))
    aaem = math.log((gclc*Cc)/(gcld*Cd))
    
#Calculo de la resistencia 

    fo = 1.8
    Rl = fo*(1/0.7)*(Es/Ai)
    Rh = fo*(1/5.5)*(Es/Ai)
    r = Raem+Rcem+Rh+Rl
    Rel = 0.54
    Ri = N*r+Rel
    
    #calculo de voltaje 
    Ecem = Pcem*((R*T)/(z*CF))*acem
    Eaem = Paem*((R*T)/(z*CF))*aaem
    Ecell = N*(Ecem+Eaem)

# intensidad 
    i = Ri+Re
    I = Ecell/i #corriente electrica 

#Potencia 
    Pgross = (I**2)*Re
    Pd = Pgross/(N*Ai)
#Voltaje 
    Ec = Pgross/I
    
    df = pd.DataFrame({'Ri (ohms)': Ri,'Re (ohms)':Re,'Potencia (W)':Pgross,
                   'DPotencia (W/m^2)':Pd,'CE (A)':I,'Voltaje (V)':Ec})

#Graficas
    fig = plt.figure(figsize=(15,15))
    fig.tight_layout()
    ax1 = fig.add_subplot(1,3,1)
    ax2 = fig.add_subplot(1,3,2)
    ax3 = fig.add_subplot(1,3,3)
    ax1.plot(I,Pgross,'ro')
    ax2.plot(I,Ec,marker='*')
    ax3.plot(I,Pd,'g+')
    ax1.set_xlabel('Intensidad')
    ax1.set_ylabel('Potencia')
    ax2.set_xlabel('Intensidad')
    ax2.set_ylabel('Voltaje')
    ax3.set_xlabel('Intensidad')
    ax3.set_ylabel('potencia/Área')
    ax1.set_title('Potencial maximo')
    ax2.set_title('Intensidad vs Voltaje')
    ax1.grid()
    ax2.grid()
    ax3.grid()

    plt.show()
    
    return var.set(Ecell)

def cerrar ():
    ventana.destroy() 
      
botonaceptar=tk.Button(ventana, text="Aceptar",fg="red",bg="yellow",command=Ecell)
botonaceptar.place(x=310,y=220, width=80, height=30)

Ecellf=tk.Label(ventana,text="Voltaje máxima:",bg="dark turquoise",fg="black")
Ecellf.place(x=100,y=260, width=500, height=30)
Ef=tk.Label(ventana,bg="white",textvariable=var)
Ef.place(x=200,y=300, width=300, height=30)

botoncierra=tk.Button(ventana,text="Cerrar",fg="red",bg="yellow",command=cerrar)
botoncierra.place(x=310,y=340, width=80, height=30)

ventana.mainloop() 

