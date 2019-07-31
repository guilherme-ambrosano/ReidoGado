import matplotlib.pyplot as plt
import pandas as pd

def fazer_grafico(df):
    nomes_meses = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",7:"Jul",\
            8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}

    df = df.replace({"Mes": nomes_meses})
    
    fig = plt.figure(figsize=(550/96,330/96), dpi=96)
    ax = fig.add_subplot()
    
    width = 1

    df.plot(x = "Mes", y = "Chuva", kind='bar', color='blue',
            ax=ax, width=width, position=0.5, legend = False,
            rot = 90)

    ax2 = ax.twinx()
    
    df.plot(x = "Mes", y = "Temp", kind='line', color='red',
            ax=ax2, legend = False, rot = 90)
    
    ax.yaxis.tick_right()
    ax2.yaxis.tick_left()
    ax.set_ylabel("Chuva")
    ax2.set_ylabel("Temperatura")
    ax.yaxis.set_label_position("right")
    ax2.yaxis.set_label_position("left")

    ax.set_xlabel("Meses")
    fig.savefig("grafico.png", dpi=96)
    plt.close(fig)
