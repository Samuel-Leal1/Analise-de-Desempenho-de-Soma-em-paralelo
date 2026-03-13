"""
Solução Paralela - Soma de Números em Arquivo
Disciplina: Computação Paralela e Distribuída

Descrição:
  Lê um arquivo com um número inteiro por linha e calcula a soma total
  de forma paralela, dividindo o arquivo em chunks entre os processos.
  Suporta 2, 4, 8 ou 12 threads (processos).

Estratégia de paralelização:
  - O arquivo é dividido em N partes por bytes (byte-range splitting),
    garantindo que cada processo leia apenas sua fatia do disco.
  - Cada processo soma seus números de forma independente.
  - O processo principal reduz (soma) os resultados parciais.

Uso:
  python soma_paralela.py <caminho_do_arquivo> <num_threads>

Exemplos:
  python soma_paralela.py numero2.txt 2
  python soma_paralela.py numero2.txt 4
  python soma_paralela.py numero2.txt 8
  python soma_paralela.py numero2.txt 12
"""

import sys
import os
import time
import multiprocessing


# ─────────────────────────────────────────────
# Funções auxiliares
# ─────────────────────────────────────────────

def calcular_offsets(filepath: str, n: int) -> list[tuple[int, int]]:
    """
    Divide o arquivo em N fatias por posição de bytes.
    Cada fatia começa e termina em uma quebra de linha completa.

    Args:
        filepath: caminho do arquivo
        n: número de fatias

    Returns:
        lista de tuplas (byte_inicio, byte_fim)
    """
    tamanho = os.path.getsize(filepath)
    tamanho_chunk = tamanho // n
    offsets = []

    with open(filepath, "rb") as f:
        inicio = 0
        for i in range(n):
            if i == n - 1:
                offsets.append((inicio, tamanho))
            else:
                pos = (i + 1) * tamanho_chunk
                f.seek(pos)
                f.readline()           # avança até o próximo \n para não cortar número
                fim = f.tell()
                offsets.append((inicio, fim))
                inicio = fim

    return offsets


def soma_chunk(args: tuple) -> int:
    """
    Função executada por cada processo worker.
    Lê o intervalo de bytes atribuído e soma os números.

    Args:
        args: (filepath, byte_inicio, byte_fim)

    Returns:
        soma parcial dos números no intervalo
    """
    filepath, byte_inicio, byte_fim = args

    soma = 0
    with open(filepath, "rb") as f:
        f.seek(byte_inicio)
        dados = f.read(byte_fim - byte_inicio)

    for linha in dados.split(b"\n"):
        linha = linha.strip()
        if linha:
            try:
                soma += int(linha)
            except ValueError:
                pass  # ignora linhas malformadas

    return soma


# ─────────────────────────────────────────────
# Função principal paralela
# ─────────────────────────────────────────────

def soma_paralela(filepath: str, num_threads: int) -> tuple[int, float]:
    """
    Soma os números do arquivo usando múltiplos processos.

    Args:
        filepath: caminho para o arquivo de entrada
        num_threads: número de processos paralelos (2, 4, 8 ou 12)

    Returns:
        (soma_total, tempo_segundos)
    """
    offsets = calcular_offsets(filepath, num_threads)
    args = [(filepath, inicio, fim) for inicio, fim in offsets]

    inicio_tempo = time.perf_counter()

    with multiprocessing.Pool(processes=num_threads) as pool:
        somas_parciais = pool.map(soma_chunk, args)

    fim_tempo = time.perf_counter()
    tempo = fim_tempo - inicio_tempo

    soma_total = sum(somas_parciais)
    return soma_total, tempo


# ─────────────────────────────────────────────
# Ponto de entrada
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # ↓ Altere o caminho abaixo se necessário
    filepath = r"C:\Users\aluno\Documents\Visual Studio 2017\numero2.txt"

    for num_threads in [2, 4, 8, 12]:
        print("=" * 50)
        print(f"  SOMA PARALELA — {num_threads} THREADS")
        print("=" * 50)
        print(f"Arquivo:    {filepath}")
        print(f"CPUs disp.: {multiprocessing.cpu_count()}")
        print("Processando...\n")

        soma, tempo = soma_paralela(filepath, num_threads)

        print(f"Soma total:             {soma}")
        print(f"Tempo de processamento: {tempo:.6f} segundos")
        print()