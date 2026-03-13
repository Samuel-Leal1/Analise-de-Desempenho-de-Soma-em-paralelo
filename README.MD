# Relatório de Computação Paralela

## Soma Paralela de Números em Arquivo

---

| Campo      | Informação                        |
|------------|-----------------------------------|
| Disciplina | Computação Paralela e Distribuída |
| Aluno      | Samuel Leal de Araujo             |
| Professor  | Rafael Marconi Ramos              |
| Data       | 13/03/2026                        |

---

## 1. Descrição do Problema

Calcular a soma de todos os inteiros de um arquivo de texto (um número por linha), comparando as versões serial e paralela.

**Algoritmo utilizado:**
- **Serial:** leitura linha a linha com acumulação sequencial
- **Paralelo:** divisão do arquivo em N fatias por bytes, processamento simultâneo e soma dos resultados parciais

**Entradas utilizadas:**
- `numero1.txt` — 1.000.000 de números (desenvolvimento)
- `numero2.txt` — 10.000.000 de números (análise de desempenho)

**Complexidade:** O(n) serial — O(n/p) por processo na versão paralela

Objetivo da paralelização:
Reduzir o tempo de leitura e processamento do arquivo distribuindo a carga entre múltiplos processos, aproveitando os núcleos disponíveis no processador. O gargalo principal é a leitura sequencial de disco, que pode ser aliviada com leitura paralela em diferentes regiões do arquivo.
Complexidade aproximada do algoritmo:
O(n) — linear em relação ao número de linhas do arquivo, tanto na versão serial quanto na paralela. Na versão paralela, a complexidade por processo é O(n/p), onde p é o número de processos.

## 2. Ambiente Experimental

| Item | Descrição |
|------|-----------|
| Processador | Intel Core i5-12500 (12ª Geração) |
| Número de núcleos | 12 núcleos lógicos (6 P-cores + 4 E-cores) |
| Memória RAM | 16 GB |
| Sistema Operacional | Windows 11 |
| Linguagem utilizada | Python 3.14 |
| Biblioteca de paralelização | multiprocessing (módulo padrão do Python) |
| Versão do interpretador | Python 3.14 (CPython) |


3. Metodologia de Testes
Medição do tempo:

Utilizada a função time.perf_counter() do Python, que fornece alta resolução de tempo em segundos.
O tempo medido compreende apenas a fase de processamento (leitura + soma), excluindo inicialização do programa.

Número de execuções:

Cada configuração foi executada uma vez, registrando o tempo obtido diretamente.

Configurações testadas:

1 thread/processo — versão serial
2 threads/processos
4 threads/processos
8 threads/processos
12 threads/processos

Condições de execução:

Máquina com uso normal do sistema operacional Windows 11.
Módulo multiprocessing do Python utilizado para criação e gerenciamento dos processos.
A divisão do arquivo foi feita por posição de bytes com alinhamento em quebras de linha para evitar cortes em números.


## 4. Resultados Experimentais

### 4.1 numero1.txt — 1 milhão de números (Soma: -88)

| Threads/Processos | Tempo (s) | Speedup | Eficiência |
|:-----------------:|:---------:|:-------:|:----------:|
| 1 (serial)        | 0.091277  | 1.0000  | 1.0000     |
| 2                 | 0.159302  | 0.5730  | 0.2865     |
| 4                 | 0.126728  | 0.7202  | 0.1800     |
| 8                 | 0.145154  | 0.6289  | 0.0786     |
| 12                | 0.167955  | 0.5435  | 0.0453     |

### 4.2 numero2.txt — 10 milhões de números (Soma: 5384)

| Threads/Processos | Tempo (s) | Speedup | Eficiência |
|:-----------------:|:---------:|:-------:|:----------:|
| 1 (serial)        | 0.914836  | 1.0000  | 1.0000     |
| 2                 | 0.787704  | 1.1615  | 0.5808     |
| 4                 | 0.582052  | 1.5717  | 0.3929     |
| 8                 | 0.504109  | 1.8148  | 0.2269     |
| 12                | 0.478660  | 1.9112  | 0.1593     |

## 5. Cálculo de Speedup e Eficiência

**Speedup:** `Speedup(p) = T(1) / T(p)`

Onde T(1) é o tempo da execução serial e T(p) é o tempo com p threads/processos.

**Eficiência:** `Eficiência(p) = Speedup(p) / p`

Onde p é o número de threads ou processos.

---

## 6. Análise dos Resultados

### 6.1 numero1.txt (1 milhão de números)

Com 1 milhão de números, o tempo serial foi de 0,091 segundos. A versão paralela foi **mais lenta que o serial** em todas as configurações — o overhead de criação dos processos supera o ganho. Paralelismo só é vantajoso quando o volume de trabalho é grande o suficiente para amortizar os custos de coordenação.

### 6.2 numero2.txt (10 milhões de números)

Com 10 milhões de números, o tempo serial foi 0,914s e com 12 threads caiu para 0,478s, resultando em **speedup de 1,91**. O ganho cresceu consistentemente de 2 para 12 threads, mas de forma sub-linear.

**Análise do Speedup:**
- Positivo e crescente, mas muito abaixo do ideal (ideal seria 12 com 12 threads)
- Gargalo principal: leitura do disco compartilhada entre os processos
- A **Lei de Amdahl** limita o speedup máximo pois parte do trabalho é inerentemente serial

**Análise da Eficiência:**
- 2 threads: **58%** — relativamente boa
- 4 threads: **39%** — queda significativa
- 8 threads: **23%** — processos extras contribuem pouco
- 12 threads: **16%** — overhead de paralelização domina

**Causas da perda de eficiência:**
- Contenção de I/O: múltiplos processos competindo pelo mesmo disco
- Overhead de criação/destruição do `multiprocessing.Pool`
- Custo de comunicação entre processos via IPC
- 12 threads excede os 6 P-cores físicos, introduzindo contenção adicional

---

## 7. Conclusão

Para 1 milhão de números o paralelismo foi contraproducente; para 10 milhões houve melhora consistente, atingindo **speedup de 1,91 com 12 processos**. O melhor custo-benefício foi com **2 threads** (eficiência de 58%).

Melhorias possíveis:
- Usar `numpy` para leitura e soma vetorizada
- Pré-carregar o arquivo em memória antes de dividir entre processos
- Testar com `numerogigante.txt` (1 bilhão de números), onde os ganhos seriam muito mais expressivos

A eficácia do paralelismo depende do tamanho da entrada, da natureza do gargalo (CPU vs. I/O) e do custo de coordenação entre processos.

