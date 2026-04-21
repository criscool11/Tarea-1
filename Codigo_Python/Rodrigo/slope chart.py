import matplotlib.pyplot as plt
import pandas as pd

# ============================================================
# DATOS — porcentaje de obesidad en adultos (BMI >= 30)
# Formato: (Entity, Year, valor%)
# ============================================================

raw_data = [
    ("China",1990,1.14259),
    ("China",2022,8.21126),
    ("United States", 1990, 18.52077),
    ("United States", 2022, 42.86787),
    ("France",        1990, 11.2928),
    ("France",        2022, 10.92481),
    ("South Africa",  1990, 14.05956),
    ("South Africa",  2022, 30.03376),
    ("Australia",     1990, 12.83769),
    ("Australia",     2022, 31.82415),
]

# ============================================================
# CONFIGURACIÓN
# ============================================================

COLORS = [
    "#378ADD",  # azul       — Chile
    "#1D9E75",  # teal       — United States
    "#D85A30",  # coral      — France
    "#7F77DD",  # purple     — South Africa
    "#BA7517",  # amber      — Australia
]

# ============================================================
# FUNCIÓN DE AJUSTE DE ETIQUETAS
# ============================================================

def adjust_labels(positions, min_gap):
    pos      = sorted(range(len(positions)), key=lambda i: positions[i])
    adjusted = list(positions)

    for _ in range(1000):
        moved = False
        for i in range(len(pos) - 1):
            a   = pos[i]
            b   = pos[i + 1]
            gap = adjusted[b] - adjusted[a]
            if gap < min_gap:
                push        = (min_gap - gap) / 2
                adjusted[a] -= push
                adjusted[b] += push
                moved = True
        if not moved:
            break

    return adjusted

# ============================================================
# PROCESAMIENTO
# ============================================================

df = pd.DataFrame(raw_data, columns=["Entity", "Year", "Value"])

years      = sorted(df["Year"].unique())
YEAR_LEFT  = years[0]
YEAR_RIGHT = years[1]

countries  = df["Entity"].unique()
left_data  = df[df["Year"] == YEAR_LEFT].set_index("Entity")["Value"]
right_data = df[df["Year"] == YEAR_RIGHT].set_index("Entity")["Value"]

all_values    = list(left_data.values) + list(right_data.values)
data_range    = max(all_values) - min(all_values)

# MIN_GAP relativo al rango de los datos (8% del rango)
MIN_GAP = data_range * 0.08

left_original  = [left_data[c]  for c in countries]
right_original = [right_data[c] for c in countries]

left_adjusted  = adjust_labels(left_original,  MIN_GAP)
right_adjusted = adjust_labels(right_original, MIN_GAP)

# ============================================================
# GRÁFICO
# ============================================================

fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor("#FAFAF8")
ax.set_facecolor("#FAFAF8")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# margen vertical generoso para separar bien las líneas
y_min = min(all_values) - data_range * 0.25
y_max = max(all_values) + data_range * 0.25
ax.set_xlim(-0.45, 1.45)
ax.set_ylim(y_min, y_max)

# líneas verticales
for x in [0, 1]:
    ax.axvline(x=x, color="#CCCCCC", linewidth=1.2, zorder=0)

# etiquetas de años
ax.text(0, y_max, str(YEAR_LEFT),  ha="center", va="bottom",
        fontsize=13, fontweight="bold", color="#444441")
ax.text(1, y_max, str(YEAR_RIGHT), ha="center", va="bottom",
        fontsize=13, fontweight="bold", color="#444441")

# dibujar cada país
for i, country in enumerate(countries):
    color  = COLORS[i % len(COLORS)]
    y0     = left_data[country]
    y1     = right_data[country]
    y0_adj = left_adjusted[i]
    y1_adj = right_adjusted[i]
    change = y1 - y0
    sign   = "+" if change >= 0 else ""

    # línea principal entre puntos reales
    ax.plot([0, 1], [y0, y1],
            color=color, linewidth=2.2, solid_capstyle="round", zorder=2)

    # puntos en posición real
    ax.scatter([0, 1], [y0, y1],
               color=color, s=60, zorder=3)

    # línea guía izquierda
    if abs(y0_adj - y0) > 0.3:
        ax.plot([-0.01, -0.07], [y0, y0_adj],
                color=color, linewidth=0.8, alpha=0.5, zorder=1)

    # línea guía derecha
    if abs(y1_adj - y1) > 0.3:
        ax.plot([1.01, 1.07], [y1, y1_adj],
                color=color, linewidth=0.8, alpha=0.5, zorder=1)

    # etiqueta izquierda
    ax.text(-0.08, y0_adj,
            f"{country}  {y0:.1f}%",
            ha="right", va="center",
            fontsize=9.5, color=color, fontweight="bold")

    # etiqueta derecha
    ax.text(1.08, y1_adj,
            f"{y1:.1f}%  {sign}{change:.1f}%",
            ha="left", va="center",
            fontsize=9.5, color=color, fontweight="bold")

# título y subtítulo
fig.text(0.5, 0.97,
         "Prevalencia de obesidad en adultos",
         ha="center", va="top",
         fontsize=15, fontweight="bold", color="#2C2C2A")
fig.text(0.5, 0.93,
         f"Comparación {YEAR_LEFT} vs {YEAR_RIGHT} · % adultos con BMI ≥ 30 · Fuente: WHO / Our World in Data",
         ha="center", va="top",
         fontsize=9, color="#888780")

plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("slope_chart_obesidad.png", dpi=150, bbox_inches="tight")
plt.show()
print("Gráfico guardado como slope_chart_obesidad.png")