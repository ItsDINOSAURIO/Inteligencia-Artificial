import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def dec_solar(n):
    # return np.radians(23.45)*np.sin(np.radians((360/365)*(284+n))) #delta
    return 23.45*np.sin(np.radians((360/365)*(284+n))) #delta

def horario(h):
    return 15*(h-12) #omega

def cenit_solar(lat,delta,omega):
    delta=np.radians(delta)
    omega=np.radians(omega)
    return np.degrees(np.arccos(np.sin(lat)*np.sin(delta)+np.cos(lat)*np.cos(delta)*np.cos(omega))) #theta_z

def angulo_inc(lat,delta,omega,beta,gamma):
    delta=np.radians(delta) #declinacion
    omega=np.radians(omega) #angulo horario
    beta=np.radians(beta) #Angulo entre el plano y la horizontal
    gamma=np.radians(gamma) #Azimuth
    lat=np.radians(lat)
    cos_thi = (
    np.sin(delta)*np.sin(lat)*np.cos(beta)-np.sin(delta)*np.cos(lat)*np.sin(beta)*np.cos(gamma) +
    np.cos(delta)*np.cos(lat)*np.cos(beta)*np.cos(omega) + np.cos(delta)*np.sin(lat)*np.sin(beta)*np.cos(gamma)*np.cos(omega) +
    np.cos(delta)*np.sin(beta)*np.sin(gamma)*np.sin(omega))
    thi=np.arccos(cos_thi)
    return np.degrees(thi)

def des_Irr(GHI, theta_z):
    Kt = GHI / (1367 * np.maximum(np.cos(np.radians(theta_z)), 0.065))
    Kt = np.clip(Kt, 0, 1)
    df = np.where(Kt <= 0.22, 1 - 0.09 * Kt,
                  np.where(Kt <= 0.8,
                           0.9511 - 0.1604 * Kt + 4.388 * Kt**2 - 16.638 * Kt**3 + 12.336 * Kt**4,
                           0.165))
    Gd = df * GHI
    Gb = GHI - Gd
    return Gb, Gd

def Irr_in(GHI_i, Gb, Gd, Rb, beta, sigma=0.2): #sigma:albedo
    beta_rad = np.radians(beta)
    Gr = sigma * GHI_i * ((1 - np.cos(beta_rad)) / 2)
    Gt = Gb * Rb + Gd * ((1 + np.cos(beta_rad)) / 2) + Gr
    return Gt

def fitness(p, data, lat, Ap):
    theta = p[0]
    beta = p[1]  
    N = int(round(p[2]))  
    A_total = N * Ap 
    if A_total > At:
        return -np.inf 
    E_total = 0.0
    for i, time in enumerate(data['Datetime']):
        hour = time.hour + time.minute / 60
        day = time.timetuple().tm_yday
        delta = dec_solar(day)
        omega = horario(hour)
        theta_z = cenit_solar(lat, delta, omega)
        theta_i = angulo_inc(lat, delta, omega, beta, theta)
        # if theta_z > 90 or theta_i > 90:
        #     continue
        Rb = np.cos(np.radians(theta_i)) / np.maximum(np.cos(np.radians(theta_z)), 0.065)
        Gb, Gd = des_Irr(data['GHI'].iloc[i], theta_z)
        # Gt = Gb * Rb + Gd * ((1 + np.cos(np.radians(beta))) / 2)
        Gt = Irr_in(data['GHI'].iloc[i], Gb, Gd, Rb, beta)
        E_total += eta * A_total * Gt
        # E.append(E_total)
        # print(E_total)

    return E_total

# Leer y procesar los datos
csv_path = r"D:\Upiita\6to\IA\Prácticas\Paneles_Solares\POWER_Point_Hourly_20230101_20231231_019d51N_099d13W_LST.csv"
data = pd.read_csv(csv_path, skiprows=12)
data.columns = ['Year', 'Month', 'Day', 'Hour', 'GHI']
data = data[(data['Year'] == 2023) & (data['Month'] == 1) & (data['Day'] == 1)]
data['Datetime'] = pd.to_datetime(data[['Year', 'Month', 'Day', 'Hour']])

# Parámetros iniciales
latitud = 19.5111
# latitud=35.0
longitud = -99.1283
Ap = 2  
At = 100 
eta = 0.4 
wmax = 0.9 
wmin = 0.4
w=wmax
c1 = c2 = 2.0

num_variables = 3
var_min = [0, -180, 1]
var_max = [90, 180, round(At / Ap)]
poblacion = 30
max_iter = 100

# Inicialización
individuo = [{'posicion': np.random.uniform(var_min, var_max, num_variables),
              'velocidad': np.zeros(num_variables),
              'costo': None,
              'best_posicion': None,
              'best_costo': np.inf} for _ in range(poblacion)]
_global = {'posicion': None, 'costo': -np.inf}

# Evaluación inicial
for i in range(poblacion):
    individuo[i]['costo'] = fitness(individuo[i]['posicion'], data, latitud, Ap)
    individuo[i]['best_posicion'] = individuo[i]['posicion'].copy()
    individuo[i]['best_costo'] = individuo[i]['costo']
    if individuo[i]['costo'] > _global['costo']:
        _global['posicion'] = individuo[i]['posicion'].copy()
        _global['costo'] = individuo[i]['costo']

# Optimización
E=[]
for iter in range(max_iter):
    for i in range(poblacion):
        # Actualización de velocidad
        r1, r2 = np.random.rand(2)
        individuo[i]['velocidad'] = (
            w * individuo[i]['velocidad'] +
            r1 * c1 * (individuo[i]['best_posicion'] - individuo[i]['posicion']) +
            r2 * c2 * (_global['posicion'] - individuo[i]['posicion'])
        )
        # Actualización de posición
        individuo[i]['posicion'] += individuo[i]['velocidad']
        individuo[i]['posicion'] = np.clip(individuo[i]['posicion'], var_min, var_max)
        individuo[i]['posicion'][2] = int(round(individuo[i]['posicion'][2]))  # Asegurar número entero

        # Evaluación de costo
        individuo[i]['costo'] = fitness(individuo[i]['posicion'], data, latitud, Ap)
        if individuo[i]['costo'] > individuo[i]['best_costo']:
            individuo[i]['best_posicion'] = individuo[i]['posicion'].copy()
            individuo[i]['best_costo'] = individuo[i]['costo']
            if individuo[i]['costo'] > _global['costo']:
                _global['posicion'] = individuo[i]['posicion'].copy()
                _global['costo'] = individuo[i]['costo']

    # Actualizar inercia
    w = wmax -((wmax-wmin)/max_iter)*iter

    print(f"Iteración {iter + 1}/{max_iter}, Mejor Costo: {_global['costo']}, Mejor Posición: {_global['posicion']}")
    E.append(_global['costo'])
  
plt.close('all')
plt.figure()
grafica_costo = np.array(E)
plt.semilogy(abs(grafica_costo))
plt.xlabel('Iteraciones')
plt.ylabel('Costo')

print("Mejor posición encontrada:", _global['posicion'])
print("Mejor costo encontrado:", _global['costo'])

plt.show()