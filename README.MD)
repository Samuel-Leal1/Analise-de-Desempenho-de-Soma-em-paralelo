Relatório de Computação Paralela
Soma Paralela de Números em Arquivo
Disciplina: Computação Paralela e Distribuída
Aluno(s): Samuel Leal de Araujo
Professor: Rafael Marconi Ramos
Data: 13/03/2026

1. Descrição do Problema
O problema consiste em calcular a soma de todos os valores inteiros armazenados em um arquivo de texto, onde cada linha contém um único número inteiro (positivo ou negativo). O objetivo é implementar e comparar versões serial e paralela deste processamento, avaliando os ganhos de desempenho obtidos com a paralelização.
Algoritmo utilizado:

Versão serial: leitura linha a linha do arquivo com acumulação sequencial da soma.
Versão paralela: divisão do arquivo em N fatias por posição de bytes (byte-range splitting), processamento simultâneo de cada fatia em um processo separado e redução final somando os resultados parciais.

Tamanhos de entrada utilizados:

numero1.txt — 1.000.000 de números inteiros (fase de desenvolvimento)
numero2.txt — 10.000.000 de números inteiros (fase de análise de desempenho)

Objetivo da paralelização:
Reduzir o tempo de leitura e processamento do arquivo distribuindo a carga entre múltiplos processos, aproveitando os núcleos disponíveis no processador. O gargalo principal é a leitura sequencial de disco, que pode ser aliviada com leitura paralela em diferentes regiões do arquivo.
Complexidade aproximada do algoritmo:
O(n) — linear em relação ao número de linhas do arquivo, tanto na versão serial quanto na paralela. Na versão paralela, a complexidade por processo é O(n/p), onde p é o número de processos.

2. Ambiente Experimental
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


4. Resultados Experimentais
4.1 numero1.txt — 1 milhão de números (Soma: -88)
| Threads/Processos | Tempo (s) | Speedup | Eficiência |
|:-----------------:|:---------:|:-------:|:----------:|
| 1 (serial)        | 0.091277  | 1.0000  | 1.0000     |
| 2                 | 0.159302  | 0.5730  | 0.2865     |
| 4                 | 0.126728  | 0.7202  | 0.1800     |
| 8                 | 0.145154  | 0.6289  | 0.0786     |
| 12                | 0.167955  | 0.5435  | 0.0453     |

4.2 numero2.txt — 10 milhões de números (Soma: 5384)
| Threads/Processos | Tempo (s) | Speedup | Eficiência |
|:-----------------:|:---------:|:-------:|:----------:|
| 1 (serial)        | 0.914836  | 1.0000  | 1.0000     |
| 2                 | 0.787704  | 1.1615  | 0.5808     |
| 4                 | 0.582052  | 1.5717  | 0.3929     |
| 8                 | 0.504109  | 1.8148  | 0.2269     |
| 12                | 0.478660  | 1.9112  | 0.1593     |

5. Cálculo de Speedup e Eficiência
Speedup:
Speedup(p)=T(1)T(p)Speedup(p) = \frac{T(1)}{T(p)}Speedup(p)=T(p)T(1)​
Onde T(1) é o tempo da execução serial e T(p) é o tempo com p threads/processos.
Eficiência:
Eficiencia(p)=Speedup(p)pEficiência(p) = \frac{Speedup(p)}{p}Eficiencia(p)=pSpeedup(p)​
Onde p é o número de threads ou processos.

6. Análise dos Resultados
6.1 numero1.txt (1 milhão de números)
Com o arquivo de 1 milhão de números, o tempo serial foi de 0,091 segundos — extremamente baixo. A versão paralela apresentou desempenho inferior ao serial em todas as configurações, com speedup abaixo de 1. Isso demonstra que, para entradas pequenas, o overhead de criação dos processos supera qualquer ganho de processamento paralelo. Este comportamento é esperado e confirma que paralelismo só é vantajoso quando o volume de trabalho é suficientemente grande para amortizar os custos de coordenação.
6.2 numero2.txt (10 milhões de números)
Com 10 milhões de números, o tempo serial foi de 0,914 segundos e a versão com 12 threads reduziu para 0,478 segundos, resultando em speedup de 1,91. O ganho cresceu de forma consistente de 2 para 12 threads, ainda que de maneira sub-linear.
Análise do Speedup:

O speedup foi positivo e crescente, mas muito abaixo do ideal (speedup ideal com 12 threads seria 12).
O principal gargalo é a leitura do disco: a largura de banda de I/O é compartilhada entre os processos, limitando o ganho real.
A Lei de Amdahl se aplica: parte do trabalho é inerentemente serial, limitando o speedup máximo alcançável.

Análise da Eficiência:

Com 2 threads: eficiência de 0,5808 (58%) — relativamente boa.
Com 4 threads: eficiência de 0,3929 (39%) — queda significativa.
Com 8 threads: eficiência de 0,2269 (23%) — processos extras contribuem pouco.
Com 12 threads: eficiência de 0,1593 (16%) — overhead de paralelização domina.

Causas da perda de eficiência:

Contenção de I/O: múltiplos processos competindo pelo mesmo disco.
Overhead de criação e destruição do pool de processos (multiprocessing.Pool).
Custo de comunicação entre processos via IPC (Inter-Process Communication).
O número de threads (12) excede o número de P-cores físicos (6), introduzindo contenção adicional.


7. Conclusão
O experimento demonstrou que a paralelização traz ganhos reais para arquivos grandes, mas com limitações. Para 1 milhão de números o paralelismo foi contraproducente; para 10 milhões houve melhora consistente, atingindo speedup de 1,91 com 12 processos.
O melhor custo-benefício foi com 2 threads (eficiência de 58%). Para melhorar os resultados futuras implementações poderiam:

Utilizar numpy para leitura e soma vetorizada.
Pré-carregar o arquivo em memória antes de dividir entre processos.
Testar com numerogigante.txt (1 bilhão de números), onde os ganhos seriam muito mais expressivos.

Conclui-se que a eficácia do paralelismo depende diretamente do tamanho da entrada, da natureza do gargalo (CPU vs. I/O) e do custo de coordenação entre processos.


