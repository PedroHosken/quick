# Trabalho Prático — QuickSort: Original vs. Aleatorizado

## Contexto

Este trabalho é baseado no artigo científico:
> JaJa, J. *"A Perspective on Quicksort"*. Computing in Science & Engineering, IEEE, Jan/Feb 2000.

O artigo apresenta o QuickSort clássico, sua análise de complexidade (pior caso e caso médio), uma versão aleatorizada que evita o pior caso, e extensões para processamento paralelo e geometria computacional.

---

## O que precisa ser implementado e executado

### Dependências necessárias

```bash
pip install numpy matplotlib
```

Adicione também no início do script:

```python
import sys
sys.setrecursionlimit(1_000_000)
```

---

### PARTE 1 — QuickSort Original (pivô fixo no primeiro elemento)

Implemente o QuickSort com o particionamento de Hoare/Sedgewick exatamente como descrito no artigo (Figura 1):

```
procedure partition(A, l, r)
  pivot = A[l]
  i = l,  j = r + 1
  while true:
    while A[++i] < pivot  →  incrementa i
    while A[--j] > pivot  →  decrementa j
    if i < j: troca A[i] e A[j]
    else: break
  A[l] = A[j]
  A[j] = pivot
  retorna j
```

**Instrumente o código para contar comparações:** cada avaliação de `A[i] < pivot` e `A[j] > pivot` deve ser contada, incluindo a comparação que encerra cada laço interno.

**Experimento:**
- Tamanhos: `n = 2^10, 2^11, 2^12, ..., 2^20` (11 valores)
- Para cada `n`: execute **1000 vezes** com vetores de inteiros distintos gerados aleatoriamente (`random.sample`)
- Calcule a **média das comparações** para cada `n`
- Calcule `X = média / (n * log2(n))` para cada `n` e tire a média geral de X
- O valor teórico é `2 * ln(2) ≈ 1.3863`

---

### PARTE 2 — QuickSort Aleatorizado (pivô aleatório)

Modifique o particionamento: **antes** de executar o procedimento acima, sorteia um índice aleatório no subarray atual e troca com `A[l]`. O restante do particionamento é idêntico.

```python
rand_idx = random.randint(l, r)
A[l], A[rand_idx] = A[rand_idx], A[l]
# ... mesmo particionamento do original
```

Isso evita o pior caso O(n²) para qualquer entrada (ex.: vetor já ordenado), garantindo O(n log n) com alta probabilidade independentemente da distribuição da entrada.

**Repita o mesmo experimento da Parte 1** com esta versão.

---

### PARTE 3 — Comparação e Gráficos

Gere **dois gráficos** salvos como `grafico_quicksort.png`:

**Gráfico 1 — Comparações médias vs. tamanho:**
- Eixo X: n em escala log₂
- Eixo Y: número médio de comparações (escala log)
- Duas curvas: Original e Aleatorizado
- Duas curvas pontilhadas: `X_medio * n * log2(n)` para cada versão

**Gráfico 2 — Constante X empírica por tamanho:**
- Eixo X: n em escala log₂
- Eixo Y: X = comparações / (n · lg n)
- Duas curvas: Original e Aleatorizado
- Linha horizontal: valor teórico `2 * ln(2) ≈ 1.3863`

---

### PARTE 4 — Saída esperada no terminal

Imprima uma tabela no seguinte formato:

```
========================================================
EXPERIMENTO 1 – QuickSort Original (pivô fixo)
========================================================
  n =    1024  (1000 execuções)...  média = XXXXX.X   (Xs)
  n =    2048  (1000 execuções)...  média = XXXXX.X   (Xs)
  ...

========================================================
EXPERIMENTO 2 – QuickSort Aleatorizado
========================================================
  n =    1024  (1000 execuções)...  média = XXXXX.X   (Xs)
  ...

── Valores de X = média / (n·lg n) ──
       n      X_orig      X_rand
    1024      X.XXXX      X.XXXX
    2048      X.XXXX      X.XXXX
    ...

X médio (original)     = X.XXXX
X médio (aleatorizado) = X.XXXX
Valor teórico (2·ln2)  = 1.3863
```

---

### PARTE 5 — Salvar resultados em JSON

Ao final, salve um arquivo `results.json` com a seguinte estrutura:

```json
{
  "sizes": [1024, 2048, 4096, ..., 1048576],
  "avg_orig": [...],
  "avg_rand": [...],
  "X_orig": [...],
  "X_rand": [...],
  "X_orig_mean": 1.XXXX,
  "X_rand_mean": 1.XXXX
}
```

---

## Arquivos de saída esperados

| Arquivo | Conteúdo |
|---|---|
| `grafico_quicksort.png` | Dois gráficos lado a lado |
| `results.json` | Todos os dados numéricos dos experimentos |

---

## Observações importantes

- Use `random.sample(range(n * 10), n)` para gerar vetores com inteiros distintos
- O limite de recursão deve ser aumentado: `sys.setrecursionlimit(1_000_000)`
- Para n = 2^20 com pivô fixo em entradas aleatórias, a recursão não deve ser problema, mas se houver stack overflow, avise
- Os dois algoritmos devem usar **exatamente o mesmo conjunto de vetores** não — cada execução sorteia um vetor novo para cada versão independentemente (isso é correto para médias empíricas)
- Quando terminar, me envie o `results.json` e o `grafico_quicksort.png` para eu montar o relatório PDF final

---

## Questões para discussão (responda no terminal ou num arquivo txt)

1. O valor empírico de X convergiu para `2·ln(2) ≈ 1.3863`? A que velocidade?
2. A versão aleatorizada apresentou X maior, menor ou igual ao original? O que isso implica?
3. Evitar o pior caso com aleatorização **melhora também o caso médio**? Por quê?
