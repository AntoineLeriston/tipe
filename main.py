import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

def initialisation(nx: int, ny: int, T_initiale: float, T_aux_bords: int):
    """
    nx et ny: dimensions de la plaque.
    T_initiale: température initiale de la plaque.
    T_aux_bords: La température que l'on souhaite appliquer aux bords.
    sortie la plaque ainsi construite.
    """
    plaque = np.full((nx, ny), T_initiale) # crée une matrice remplie de T_initiale
    plaque[0, :] = T_aux_bords # Bord haut
    plaque[-1, :] = T_aux_bords # Bord bas
    plaque[:, 0] = T_aux_bords # Bord gauche
    plaque[:, -1] = T_aux_bords # Bord droit
    return plaque

def actualisation(plaque, D, dx, dy, dt):
    nouvelle_plaque = plaque.copy()
    nx, ny = plaque.shape # On récupère les dimensions de la plaque
    for i in range(1, nx-1):
        for j in range(1, ny-1):
            d2Tdx2 = (plaque[i+1, j] - 2 * plaque[i, j] + plaque[i-1, j]) / dx**2
            d2Tdy2 = (plaque[i, j+1] - 2 * plaque[i, j] + plaque[i, j-1]) / dy**2
            nouvelle_plaque[i, j] = plaque[i, j] + D * dt * (d2Tdx2 + d2Tdy2)
    return nouvelle_plaque

def simulation(nx, ny, alpha, dx, dy, dt, T_initial, T_boundary, steps):
    plate = initialisation(nx, ny, T_initial, T_boundary)
    fig, ax = plt.subplots()
    cax = ax.imshow(plate, cmap='turbo', interpolation='nearest', vmin=T_initial, vmax=T_boundary)
    cb = fig.colorbar(cax, ax=ax, orientation='vertical')

    def update(frame):
        nonlocal plate
        plate = actualisation(plate, alpha, dx, dy, dt)
        cax.set_data(plate)
        return cax,

    ani = animation.FuncAnimation(fig, update, frames=steps, interval=50, blit=False)
    plt.show()

# Paramètres
nx, ny = 20, 20 # Taille de la grille
dx = dy = 0.01 # Discrétisation spatiale
dt = 0.01 # Pas de temps

# Pour de l'acier (ou vitrocéramique selon le commentaire)
MU = 2520 # masse volumique de la vitrocéramique en kg/m^3
C = 790 # capacité thermique de la vitrocéramique en J/kg/K
LAMBDA = 1.5 # conductivité thermique de la vitrocéramique en W/m/K

D = LAMBDA / (MU * C) # Coefficient de diffusion thermique
print(D)

T_aux_bords = 250.0 # Température aux bords
T_initiale = 20.0 # Température initiale
nombre_instants = 100 # Nombre d'itérations

# Lancer la simulation
simulation(nx, ny, D, dx, dy, dt, T_initiale, T_aux_bords, nombre_instants)
