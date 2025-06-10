import pandas as pd
import numpy as np
import random
from datetime import datetime

# Setup
random.seed(42)
np.random.seed(42)

# Parâmetros
usuarios_iniciais = 500
crescimento_anual = 1.10  # 10% de crescimento ao ano
num_meses = 12  # Janeiro a Dezembro
anos = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

# Listas de opções
plataformas = ['Netflix', 'Prime Video', 'Disney+', 'HBO Max', 'Apple TV+']
plataforma_pesos = [0.35, 0.25, 0.2, 0.15, 0.05]

paises = ['Brasil', 'EUA', 'Reino Unido', 'Alemanha', 'Índia']
pais_pesos = [0.3, 0.25, 0.15, 0.15, 0.15]

generos = ['Ação', 'Comédia', 'Drama', 'Terror', 'Romance', 'Documentário', 'Ficção Científica']
genero_pesos = [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1]

# Lista para armazenar os dados
dados = []

# Dicionário para armazenar os usuários e seus atributos fixos
usuarios = {}
usuario_id_atual = 1

# Crescimento cumulativo com usuários antigos permanecendo ativos
for ano_idx, ano in enumerate(anos):
    total_usuarios_ano = int(usuarios_iniciais * (crescimento_anual ** ano_idx))
    novos_usuarios = total_usuarios_ano - len(usuarios)

    # Criar novos usuários
    for _ in range(novos_usuarios):
        plataforma = random.choices(plataformas, weights=plataforma_pesos, k=1)[0]
        pais = random.choices(paises, weights=pais_pesos, k=1)[0]
        genero_favorito = random.choices(generos, weights=genero_pesos, k=1)[0]
        usuarios[usuario_id_atual] = {
            'plataforma': plataforma,
            'pais': pais,
            'genero_favorito': genero_favorito,
            'ano_entrada': ano
        }
        usuario_id_atual += 1

    # Gerar dados mensais para todos os usuários ativos neste ano
    for usuario_id, info in usuarios.items():
        if info['ano_entrada'] > ano:
            continue  # Usuário ainda não existe neste ano

        for mes in range(1, num_meses + 1):
            # Dias no mês
            if mes in [4, 6, 9, 11]:
                dias_no_mes = 30
            elif mes == 2:
                dias_no_mes = 28
            else:
                dias_no_mes = 31

            dia = random.randint(1, dias_no_mes)
            data = datetime(ano, mes, dia).strftime('%Y-%m-%d')

            # Tempo assistido depende da plataforma
            if info['plataforma'] == 'Netflix':
                tempo = np.random.normal(60, 15)
            elif info['plataforma'] == 'Prime Video':
                tempo = np.random.normal(45, 10)
            elif info['plataforma'] == 'Disney+':
                tempo = np.random.normal(40, 12)
            elif info['plataforma'] == 'HBO Max':
                tempo = np.random.normal(35, 15)
            else:
                tempo = np.random.normal(25, 10)

            tempo = max(0, round(tempo, 1))
            qtd_titulos = int(tempo / np.random.uniform(1.3, 1.8))
            nota_base = 3.5 + (tempo / 100) + np.random.normal(0, 0.4)
            avaliacao = round(min(max(nota_base, 1), 5), 1)

            dados.append([
                usuario_id,
                data,
                info['plataforma'],
                info['pais'],
                tempo,
                qtd_titulos,
                info['genero_favorito'],
                avaliacao
            ])

# Criar DataFrame
df = pd.DataFrame(dados, columns=[
    'usuario_id', 'data', 'plataforma', 'pais',
    'tempo_assistido_mensal', 'qtd_titulos_assistidos',
    'genero_favorito', 'avaliacao_usuario'
])

# Exportar CSV
df.to_csv("dados_streaming_realista_2018_2024.csv", index=False)
print("✅ Dataset com crescimento de usuários salvo como 'dados_streaming_realista_2018_2024.csv'")
