import random
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import json
import sys
from multiprocessing import Pool, cpu_count

sys.setrecursionlimit(1_000_000)

# ─────────────────────────────────────────────────────────────
# QuickSort Iterativo
# ─────────────────────────────────────────────────────────────

def partition_original(arr, l, r):
    pivot = arr[l]
    i = l
    j = r + 1
    count = 0
    while True:
        i += 1
        while i <= r and arr[i] < pivot:
            count += 1
            i += 1
        count += 1
        j -= 1
        while j >= l and arr[j] > pivot:
            count += 1
            j -= 1
        count += 1
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            break
    arr[l], arr[j] = arr[j], arr[l]
    return j, count

def partition_randomized(arr, l, r):
    rand_idx = random.randint(l, r)
    arr[l], arr[rand_idx] = arr[rand_idx], arr[l]
    return partition_original(arr, l, r)

def _sort_iterative(arr, partition_fn):
    total = 0
    stack = [(0, len(arr) - 1)]
    while stack:
        l, r = stack.pop()
        if l < r:
            p, cnt = partition_fn(arr, l, r)
            total += cnt
            stack.append((l, p - 1))
            stack.append((p + 1, r))
    return total

def run_quicksort_original(arr):
    a = arr[:]
    return _sort_iterative(a, partition_original)

def run_quicksort_randomized(arr):
    a = arr[:]
    return _sort_iterative(a, partition_randomized)


# ─────────────────────────────────────────────────────────────
# Workers top-level para multiprocessing
# ─────────────────────────────────────────────────────────────

def _worker_orig(n):
    arr = random.sample(range(n * 10), n)
    return run_quicksort_original(arr)

def _worker_rand(n):
    arr = random.sample(range(n * 10), n)
    return run_quicksort_randomized(arr)


# ─────────────────────────────────────────────────────────────
# EXPERIMENTOS
# ─────────────────────────────────────────────────────────────

SIZES = [2**k for k in range(10, 21)]
N_RUNS = 120

def run_experiment(worker_fn, sizes, n_runs, n_proc):
    results = {}
    print(f"  (usando {n_proc} processos paralelos)")
    with Pool(processes=n_proc) as pool:
        for n in sizes:
            print(f"  n = {n:>7}  ({n_runs} execuções)...", end="", flush=True)
            t0 = time.time()
            comps = pool.map(worker_fn, [n] * n_runs)
            avg = np.mean(comps)
            results[n] = avg
            print(f"  média = {avg:,.1f}   ({time.time()-t0:.1f}s)")
    return results


# ─────────────────────────────────────────────────────────────
# Guard obrigatório no macOS para multiprocessing (spawn)
# ─────────────────────────────────────────────────────────────

if __name__ == '__main__':
    N_PROC = cpu_count()

    print("=" * 60)
    print("EXPERIMENTO 1 – QuickSort Original (pivô fixo)")
    print("=" * 60)
    results_orig = run_experiment(_worker_orig, SIZES, N_RUNS, N_PROC)

    print()
    print("=" * 60)
    print("EXPERIMENTO 2 – QuickSort Aleatorizado")
    print("=" * 60)
    results_rand = run_experiment(_worker_rand, SIZES, N_RUNS, N_PROC)

    # ── Cálculo de X ──
    def compute_X(results):
        return {n: avg / (n * math.log2(n)) for n, avg in results.items()}

    X_orig = compute_X(results_orig)
    X_rand = compute_X(results_rand)

    X_orig_mean = np.mean(list(X_orig.values()))
    X_rand_mean = np.mean(list(X_rand.values()))

    print("\n── Valores de X = média / (n·lg n) ──")
    print(f"{'n':>8}  {'X_orig':>10}  {'X_rand':>10}")
    for n in SIZES:
        print(f"{n:>8}  {X_orig[n]:>10.4f}  {X_rand[n]:>10.4f}")

    print(f"\nX médio (original)     = {X_orig_mean:.4f}")
    print(f"X médio (aleatorizado) = {X_rand_mean:.4f}")
    print(f"Valor teórico (2·ln2)  = {2*math.log(2):.4f}")

    # ── Gráficos ──
    ns = np.array(SIZES)
    avg_orig = np.array([results_orig[n] for n in SIZES])
    avg_rand = np.array([results_rand[n] for n in SIZES])
    theo_orig = X_orig_mean * ns * np.log2(ns)
    theo_rand = X_rand_mean * ns * np.log2(ns)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"Análise Empírica do QuickSort (média de {N_RUNS} execuções)",
                 fontsize=13, fontweight='bold')

    ax1 = axes[0]
    ax1.plot(ns, avg_orig, 'o-', color='steelblue', label='Original', linewidth=2, markersize=5)
    ax1.plot(ns, avg_rand, 's--', color='tomato', label='Aleatorizado', linewidth=2, markersize=5)
    ax1.plot(ns, theo_orig, ':', color='steelblue', alpha=0.6, label=f'Curva X={X_orig_mean:.3f}·n·lgn')
    ax1.plot(ns, theo_rand, ':', color='tomato', alpha=0.6, label=f'Curva X={X_rand_mean:.3f}·n·lgn')
    ax1.set_xscale('log', base=2)
    ax1.set_yscale('log', base=10)
    ax1.set_xlabel('n (escala log₂)')
    ax1.set_ylabel('Comparações médias')
    ax1.set_title('Comparações médias vs. tamanho')
    ax1.legend(fontsize=8)
    ax1.grid(True, which='both', linestyle='--', alpha=0.4)

    ax2 = axes[1]
    ax2.plot(ns, [X_orig[n] for n in SIZES], 'o-', color='steelblue', label=f'Original  X̄={X_orig_mean:.4f}', linewidth=2, markersize=5)
    ax2.plot(ns, [X_rand[n] for n in SIZES], 's--', color='tomato', label=f'Aleat.    X̄={X_rand_mean:.4f}', linewidth=2, markersize=5)
    ax2.axhline(2*math.log(2), color='gray', linestyle=':', linewidth=1.5, label=f'Teórico 2·ln2={2*math.log(2):.4f}')
    ax2.set_xscale('log', base=2)
    ax2.set_xlabel('n (escala log₂)')
    ax2.set_ylabel('X = comparações / (n·lgn)')
    ax2.set_title('Constante X empírica por tamanho')
    ax2.legend(fontsize=9)
    ax2.grid(True, which='both', linestyle='--', alpha=0.4)

    plt.tight_layout()
    plt.savefig('grafico_quicksort.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\nGráfico salvo em grafico_quicksort.png")

    # ── JSON ──
    data = {
        "sizes": SIZES,
        "avg_orig": [results_orig[n] for n in SIZES],
        "avg_rand": [results_rand[n] for n in SIZES],
        "X_orig": [X_orig[n] for n in SIZES],
        "X_rand": [X_rand[n] for n in SIZES],
        "X_orig_mean": X_orig_mean,
        "X_rand_mean": X_rand_mean,
    }
    with open('results.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Dados salvos em results.json")
