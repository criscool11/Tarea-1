import matplotlib.pyplot as plt
from pywaffle import Waffle

# Datos extraídos de IHME VizHub (GBD 2023)
data_proportions = {
    '10-14 años': [49, 530],
    '15-19 años': [50, 1063],
    '20-24 años': [35, 585]
}

def get_blocks_and_labels(age):
    vals = data_proportions[age]
    total = sum(vals)
    
    pcts = [(v / total) * 100 for v in vals]
    print(pcts)
    
    blocks = [round(p) for p in pcts]
    diff = 100 - sum(blocks)
    blocks[1] += diff
    
    labels = [f"Anorexia: {vals[0]} casos ({pcts[0]:.1f}%)", 
              f"Bulimia: {vals[1]} casos ({pcts[1]:.1f}%)"]
    return blocks, labels

# Generamos los datos procesados por edad
b10, l10 = get_blocks_and_labels('10-14 años')
b15, l15 = get_blocks_and_labels('15-19 años')
b20, l20 = get_blocks_and_labels('20-24 años')

# Configuración de la figura
fig = plt.figure(
    FigureClass=Waffle,
    plots={
        311: {
            'values': b10,
            'labels': l10,
            'legend': {'loc': 'center left', 'bbox_to_anchor': (1.02, 0.5), 'fontsize': 10, 'frameon': False},
            'title': {'label': 'Pacientes de 10-14 años', 'loc': 'left', 'fontsize': 12, 'fontweight': 'bold'}
        },
        312: {
            'values': b15,
            'labels': l15,
            'legend': {'loc': 'center left', 'bbox_to_anchor': (1.02, 0.5), 'fontsize': 10, 'frameon': False},
            'title': {'label': 'Pacientes de 15-19 años', 'loc': 'left', 'fontsize': 12, 'fontweight': 'bold'}
        },
        313: {
            'values': b20,
            'labels': l20,
            'legend': {'loc': 'center left', 'bbox_to_anchor': (1.02, 0.5), 'fontsize': 10, 'frameon': False},
            'title': {'label': 'Pacientes de 20-24 años', 'loc': 'left', 'fontsize': 12, 'fontweight': 'bold'}
        },
    },
    rows=5,
    columns=20, 
    colors=["#FF4C4C", "#3498DB"],
    figsize=(11, 7.5),
    interval_ratio_x=0.2,
    interval_ratio_y=0.2, 
    facecolor='#FAFAFA'
)

plt.suptitle("Proporción Relativa de Incidencia: Anorexia vs Bulimia\n(Casos por cada 100k habitantes)", 
             fontsize=14, fontweight='bold', y=0.96)

fig.text(0.02, 0.02, "Fuente: Global Burden of Disease Study 2023 (GBD 2023) - IHME", 
         fontsize=9, color='#555555')

plt.subplots_adjust(right=0.72, top=0.85, bottom=0.08, hspace=0.35)

plt.show()