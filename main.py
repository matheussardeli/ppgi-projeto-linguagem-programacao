import pandas as pd
import matplotlib.pyplot as plt

# Configurações iniciais
config = {
    'path_gols': 'https://raw.githubusercontent.com/matheussardeli/ppgi-projeto-linguagem-programacao/main/goalscorers.csv',  # Caminho do arquivo CSV com dados dos artilheiros
    'path_jogos': 'https://raw.githubusercontent.com/matheussardeli/ppgi-projeto-linguagem-programacao/main/results.csv',     # Caminho do arquivo CSV com dados dos resultados dos jogos
    'path_vitorias': 'https://raw.githubusercontent.com/matheussardeli/ppgi-projeto-linguagem-programacao/main/shootouts.csv', # Caminho do arquivo CSV com dados das vitórias
    'date_format': '%Y-%m-%d'        # Formato das datas nos arquivos CSV
}

# Função para carregar dados de um arquivo CSV
def carregar_dados(caminho):
    """
    Carrega dados de um arquivo CSV.

    Argumentos:
    caminho (str): Caminho do arquivo CSV.

    Retornos:
    pd.DataFrame: DataFrame contendo os dados carregados.
    """
    try:
        df = pd.read_csv(caminho)  # Tenta carregar o arquivo CSV
        return df
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")  # Imprime mensagem de erro em caso de falha
        return None

# Função para tratar dados de datas em um DataFrame
def tratar_dados(df, colunas_datas=[]):
    """
    Converte colunas de datas para o formato correto e remove linhas com datas inválidas.

    Argumentos:
    df (pd.DataFrame): DataFrame a ser tratado.
    colunas_datas (list): Lista de nomes das colunas de datas a serem tratadas.

    Retornos:
    pd.DataFrame: DataFrame tratado.
    """
    for coluna in colunas_datas:
        # Converte as colunas de datas para o formato datetime, substituindo valores inválidos por NaT
        df[coluna] = pd.to_datetime(df[coluna], format=config['date_format'], errors='coerce')
    df.dropna(inplace=True)  # Remove linhas com datas inválidas
    return df

# Função para plotar histograma de gols por minuto
def plotar_gols_por_minuto(df):
    """
    Plota um histograma da distribuição de gols por minuto.

    Argumentos:
    df (pd.DataFrame): DataFrame contendo os dados dos gols.
    """
    plt.figure(figsize=(10, 6))  # Define o tamanho da figura
    df['minute'].plot(kind='hist', bins=45)  # Plota o histograma da coluna 'minute'
    plt.title('Distribuição de Gols por Minuto')
    plt.xlabel('Minuto do Gol')
    plt.ylabel('Quantidade de Gols')
    plt.show()

# Função para plotar proporção de tipos de gols
def plotar_proporcao_gols(df):
    """
    Plota um gráfico de pizza mostrando a proporção de tipos de gols.

    Argumentos:
    df (pd.DataFrame): DataFrame contendo os dados dos gols.
    """
    labels = ['Gols Normais', 'Gols Contra', 'Gols de Pênalti']  # Rótulos para os tipos de gols
    sizes = [
        len(df[(df['own_goal'] == False) & (df['penalty'] == False)]),  # Contagem de gols normais
        len(df[df['own_goal'] == True]),  # Contagem de gols contra
        len(df[df['penalty'] == True])  # Contagem de gols de pênalti
    ]
    plt.figure(figsize=(8, 8))  # Define o tamanho da figura
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)  # Plota o gráfico de pizza
    plt.title('Proporção de Tipos de Gols')
    plt.show()

# Função para plotar soma de gols por ano
def plotar_gols_por_ano(df):
    """
    Plota um gráfico de barras mostrando a soma de gols por ano.

    Argumentos:
    df (pd.DataFrame): DataFrame contendo os dados dos gols.
    """
    df['year'] = df['date'].dt.year  # Extrai o ano da coluna 'date'
    gols_por_ano = df.groupby('year').size()  # Agrupa e conta gols por ano
    plt.figure(figsize=(12, 6))  # Define o tamanho da figura
    gols_por_ano.plot(kind='bar')  # Plota o gráfico de barras
    plt.title('Soma de Gols por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Gols')
    plt.show()

# Função para plotar número de vitórias por time
def plotar_vitorias_por_time(df):
    """
    Plota um gráfico de barras horizontais mostrando o número de vitórias por time.

    Argumentos:
    df (pd.DataFrame): DataFrame contendo os dados das vitórias.
    """
    vitorias = df['winner'].value_counts().nlargest(10).sort_values(ascending=True)  # Conta e ordena as vitórias por time
    plt.figure(figsize=(12, 6))  # Define o tamanho da figura
    vitorias.plot(kind='barh')  # Plota o gráfico de barras horizontais
    plt.title('Top 10 Times com Mais Vitórias')
    plt.xlabel('Quantidade de Vitórias')
    plt.ylabel('Time')
    plt.show()

# Função para plotar os 10 artilheiros com a quantidade de gols
def plotar_top_artilheiros(df):
    """
    Plota um gráfico de barras horizontais mostrando os 10 principais artilheiros.

    Argumentos:
    df (pd.DataFrame): DataFrame contendo os dados dos gols.
    """
    artilheiros = df['scorer'].value_counts().nlargest(10).sort_values(ascending=True)  # Conta e ordena os artilheiros
    plt.figure(figsize=(12, 6))  # Define o tamanho da figura
    artilheiros.plot(kind='barh')  # Plota o gráfico de barras horizontais
    plt.title('Top 10 Artilheiros')
    plt.xlabel('Quantidade de Gols')
    plt.ylabel('Jogador')
    plt.show()

# Função para plotar soma de gols por competição
def plotar_gols_por_competicao(df):
    """
    Plota um gráfico de barras horizontais mostrando a soma de gols por competição.

    Argumentos:
    df (pd.DataFrame): DataFrame contendo os dados dos jogos.
    """
    df['total_goals'] = df['home_score'] + df['away_score']  # Calcula a soma dos gols de cada jogo
    gols_por_competicao = df.groupby('tournament')['total_goals'].sum().nlargest(10)  # Agrupa e soma gols por competição
    plt.figure(figsize=(12, 6))  # Define o tamanho da figura
    gols_por_competicao.plot(kind='barh')  # Plota o gráfico de barras horizontais
    plt.title('Soma de Gols por Competição')
    plt.xlabel('Quantidade de Gols')
    plt.ylabel('Competição')
    plt.show()

# Função principal que executa o script
def main():
    # Carregar e tratar os dados
    df_gols = carregar_dados(config['path_gols'])  # Carrega dados dos artilheiros
    df_jogos = carregar_dados(config['path_jogos'])  # Carrega dados dos jogos
    df_vitorias = carregar_dados(config['path_vitorias'])  # Carrega dados das vitórias

    df_gols = tratar_dados(df_gols, ['date'])  # Trata dados de datas dos artilheiros
    df_jogos = tratar_dados(df_jogos, ['date'])  # Trata dados de datas dos jogos
    df_vitorias = tratar_dados(df_vitorias, ['date'])  # Trata dados de datas das vitórias

    # Criar gráficos
    plotar_gols_por_minuto(df_gols)  # Plota histograma de gols por minuto
    plotar_proporcao_gols(df_gols)  # Plota gráfico de pizza de tipos de gols
    plotar_gols_por_ano(df_gols)  # Plota gráfico de barras de gols por ano
    plotar_vitorias_por_time(df_vitorias)  # Plota gráfico de barras de vitórias por time
    plotar_top_artilheiros(df_gols)  # Plota gráfico de barras de artilheiros
    plotar_gols_por_competicao(df_jogos)  # Plota gráfico de barras de gols por competição

if __name__ == "__main__":
    main()  # Executa a função principal
