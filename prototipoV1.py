import time
import matplotlib.pyplot as plt

def busqueda_lineal(arr, objetivo):
    for i, v in enumerate(arr):
        if v == objetivo:
            return i
    return -1

def busqueda_binaria(arr, objetivo):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == objetivo:
            return mid
        elif arr[mid] < objetivo:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

def medir_tiempo(func, arr, objetivo, repeticiones=2000):
    tiempos = []
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        func(arr, objetivo)
        tiempos.append(time.perf_counter() - inicio)
    return min(tiempos)

def analizar(tamanos):
    t_lineal, t_binaria = [], []
    for n in tamanos:
        arr = list(range(n))
        objetivo = arr[-1]
        t_lineal.append(medir_tiempo(busqueda_lineal, arr, objetivo))
        t_binaria.append(medir_tiempo(busqueda_binaria, arr, objetivo))
    return t_lineal, t_binaria

def punto_quiebre(tamanos, t_lineal, t_binaria):
    for i in range(len(tamanos)):
        if t_binaria[i] < t_lineal[i]:
            return tamanos[i]
    return None

def graficar(tamanos, t_lineal, t_binaria, quiebre):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(tamanos, t_lineal, label="Búsqueda lineal", color="tab:blue")
    ax1.plot(tamanos, t_binaria, label="Búsqueda binaria", color="tab:orange")
    if quiebre:
        ax1.axvline(quiebre, color="red", linestyle="--", label=f"Quiebre n≈{quiebre}")
    ax1.set_xlabel("Tamaño del dataset (n)")
    ax1.set_ylabel("Tiempo mínimo (s)")
    ax1.set_title("Escala normal")
    ax1.legend()

    ax2.plot(tamanos, t_lineal, label="Búsqueda lineal", color="tab:blue")
    ax2.plot(tamanos, t_binaria, label="Búsqueda binaria", color="tab:orange")
    ax2.set_yscale("log")
    ax2.set_xlabel("Tamaño del dataset (n)")
    ax2.set_ylabel("Tiempo mínimo (s) — log")
    ax2.set_title("Escala logarítmica")
    ax2.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    n_max = int(input("Tamaño máximo del dataset: "))
    paso = int(input("Paso entre tamaños: "))
    tamanos = list(range(paso, n_max + 1, paso))

    t_lineal, t_binaria = analizar(tamanos)
    quiebre = punto_quiebre(tamanos, t_lineal, t_binaria)

    print(f"\n{'n':<10}{'lineal (s)':<15}{'binaria (s)':<15}")
    for n, tl, tb in zip(tamanos, t_lineal, t_binaria):
        print(f"{n:<10}{tl:.8f}      {tb:.8f}")
    print(f"\nQuiebre detectado en n = {quiebre}")

    graficar(tamanos, t_lineal, t_binaria, quiebre)