# -*- coding: utf-8 -*-
"""SCTEC_MINI_PROJ.ipynb
"""

# Montar o drive e transformar o csv em um dataframe
# from google.colab import drive
# drive.mount('/content/drive')
import pandas as pd
# Alterar a linha abaixo de acordo com local de destino do arquivo csv.
df = pd.read_csv('./Base_Varejo.csv', sep= ';')
df.head()
len(df)

# Retirar as colunas que estão completamente nulas
df.drop(columns=['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13'], inplace=True)
df.head()
len(df)

# ================== Loop abaixo para retirar valores nulos, verificar tipo de cada coluna, quantidade de valores únicos e quais são os valores únicos ====================
for coluna in df.columns:
    valores = df[coluna].unique()
    # df[coluna].dropna().unique()
    # print("DF pós tirar valores nulos:", len(df))
    valor = "#N/D"

    df = df[~df.eq(valor).any(axis=1)]
    if pd.api.types.is_numeric_dtype(df[coluna]):
        valores_ordenados = sorted(valores)
    else:
        valores_ordenados = sorted(valores, key=lambda x: str(x).casefold())

    print(f"Coluna: {coluna}")
    print(f"Valores únicos: {valores_ordenados}")
    print("Tipo da coluna:", df[coluna].dtype)
    if df[coluna].dtype == 'object':
        print(df[coluna].apply(type).unique())
    print(f"Quantidade de valores únicos: {df[coluna].nunique()}")
    print("-" * 50)
# ========================= Fim do loop para retirar valores nulos, verificar tipo de cada coluna, quantidade de valores únicos e quais são os valores únicos =========================

print(len(df))

datas = pd.to_datetime(df['DATA'], format='%d/%m/%Y', errors='coerce') # Transforma a coluna DATA para o formato datetime

print(datas.notna().all()) # Todas as linhas com datas válidas e não nulas -> True
print(len(df))

# ======================= Verificação dos diferentes valores de cada coluna ==========================

for coluna in df.columns:
    duplicados = df[coluna][df[coluna].duplicated(keep=False)].unique()

    print(f"Coluna: {coluna}")
    print(f"Valores duplicados: {duplicados}")
    print("-" * 40)

# ================== Verificação e retirada de duplicatas =========================
qtd_antes = len(df)

df_aux = df.reset_index(drop=True)

duplicatas = df_aux[df_aux.duplicated(keep=False)]

duplicatas = duplicatas.sort_values(
    by=df_aux.columns.tolist()
)
from IPython.display import display
display(duplicatas)

df = df.drop_duplicates().reset_index(drop=True)

print("Quantidade de linhas:", len(df))
print("Duplicatas restantes:", df.duplicated().sum())
qtd_agr = len(df)
qtd_rem = qtd_antes - qtd_agr
print('Quantidade removida:', qtd_rem)

# 1. DATA: Data da compra;
# 2. CO_ID: Identificação do número de compra (número da nota fiscal);
# 3. CL_ID: Identificação do cliente (número do cliente);
# 4. CL_GENERO: Sexo biológico informado pelo cliente;
# 5. CL_EC: Estado civil do cliente:
# 1: Casado ou união estával;
# 2: Divorciado;
# 3: Separado;
# 4. Solteiro;
# 5: Viúvo.
# 6. CL_FHL: Número de filhos do cliente;
# 7. CL_SEG: Segmentação econômica do cliente (classe A, B ou C);
# 8. PR_ID: Código do produto (SKU) adquirido;
# 9. PR_CAT: Categoria do produto adquirido;
# 10. PR_NOME: Nome do produto adquirido.

# ========================= Estatísticas descritivas básicas para coluna de número de filhos do cliente =========================

df['CL_FHL'].describe()
print('Média da coluna número de filhos do cliente:', df['CL_FHL'].mean())
print('Mediana da coluna número de filhos do cliente:', df['CL_FHL'].median())
print('Desvio padrão da coluna número de filhos do cliente:', df['CL_FHL'].std())
print('Moda da coluna número de filhos do cliente:', df['CL_FHL'].mode())
print('Máximo da coluna número de filhos do cliente:', df['CL_FHL'].max())
print('Mínimo da coluna número de filhos do cliente:', df['CL_FHL'].min())
print('Quantidade de elementos da coluna número de filhos do cliente:', sum(df['CL_FHL'].value_counts()))
print('Quantidade de cada um dos elementos da coluna número de filhos do cliente:', df['CL_FHL'].value_counts())

# ============================= Bloco de exploração de padrões de agrupamento ===============================

padrao1 = df['CL_GENERO'].value_counts()
print("Quantidade de vendas para cada gênero:", padrao1)


tabela1 = pd.crosstab(df['CL_GENERO'], df['PR_CAT'])
print('Quantidade de produtos comprados por categoria por gênero', '\n', tabela1)

print("Quantidade de produtos adquiridos por categoria por gênero (considerando que cada ocorrência significa a compra de um único elemento daquele tipo):")
tabela1_format = pd.crosstab(df['PR_CAT'], df['CL_GENERO'], margins=True, margins_name='Soma entre os gêneros')
display(tabela1_format)


print("Quantidade de produtos adquiridos por gênero (considerando que cada ocorrência significa a compra de um único elemento daquele tipo):")
tabela2_format = pd.crosstab(df['PR_NOME'], df['CL_GENERO'], margins=True, margins_name='Soma entre os gêneros')
display(tabela2_format)

tabela_intervalo = tabela2_format.iloc[5:15]
print(tabela_intervalo)

print("Quantidade de produtos adquiridos por estado civil (considerando que cada ocorrência significa a compra de um único elemento daquele tipo):")
print(" 1: Casado \n 2: Divorciado \n 3: Separado \n 4: Solteiro \n 5: Viúvo")
tabela_sem_total = pd.crosstab(df['PR_NOME'], df['CL_EC'])
# print(tabela_sem_total)
tabela_sem_total['Soma'] = tabela_sem_total.sum(axis=1)
top7 = tabela_sem_total.sort_values(by='Soma', ascending=False).head(7)
top7 = top7.drop(columns=['Soma'])
display(top7.style.format("{:,}"))

df.to_csv('df_limpo.csv', index=False)

"""# Conclusões

## Nesse conjunto de dados observou-se as seguintes informações:

#### - A quantidade de produtos alimentícios comprados teve maior valor para ambos os gêneros dentre as categorias de produtos comprados;
#### - A quantidade de cada produto comprado não variou de forma significativa entre os gêneros, até mesmo absorvente que é um produto comprado predominantemente por mulheres teve pouca variação quando comparada a quantidade comprada pelo gênero masculino e quantidade comprada pelo gênero feminino;
#### - Necessidade de verificar se ocorre essa mínima variação na quantidade de produtos comprados para todos os produtos da lista;
#### - Necessidade de verificar por qual motivo a quantidade de produtos total comprada por pessoas separadas está maior que a quantidade comprada por pessoas casadas, pois há a possibilidade de todas essas pessoas separadas continuarem morando com filhos, mas ainda assim é de se estranhar que uma pessoa a menos na família não fez a quantidade de compras diminuir, e sim aumentar. Pode ser que o local da compra seja feito principalmente por pessoas separadas por conta de algum detalhe não conhecido do local;
#### - Necessidade de verificar por qual motivo a quantidade de compras feitas por pessoas vivúvas é extremamente baixa quando comparado com as pessoas em outros estados civis.
"""