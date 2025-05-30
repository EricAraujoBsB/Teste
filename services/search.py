import ipeadatapy as ipea
import pandas as pd

def sidebar(phrase:str):
    global aux
    if phrase == "Órgão":
        aux = ipea.sources()
        aux = aux[aux["SIGLA"]]
        return aux
    elif phrase == "Tema":
        aux = ipea.themes()
        aux = aux[aux["NAME"]]
        return aux
    elif phrase == "Código":
        aux = ipea.list_series()
        aux = aux[aux["CODE"]]
        return aux

def organization(phrase: str):
    """
    Retorna um dataframe contendo as series com dados financeiros do IPEA de acordo com a string parametrizada referente ao órgão procurado.

    Caso a busca não seja bem sucedida sera retornado uma string "Não Encontrado".
    """
    series = ipea.metadata()
    series = series[series["MEASURE"].str.contains("\\$")]
    series = pd.concat([series[series["SOURCE ACRONYM"].str.lower().str.contains(phrase.lower())],
                        series[series["SOURCE"].str.lower().str.contains(phrase.lower())]])
    series = series.sort_values(by='CODE').drop_duplicates()
    return "Não Encontrado" if series.empty else series


def theme(phrase: str):
    """
    Retorna um dataframe contendo as series com dados financeiros do IPEA de acordo com a string parametrizada referente ao tema procurado.

    Caso a busca não seja bem sucedida sera retornado uma string "Não Encontrado".
    """
    getThemeID = ipea.themes()
    getThemeID = getThemeID[getThemeID['NAME'].str.lower().str.contains(phrase.lower())]
    found = pd.DataFrame()
    if not getThemeID.empty:
        for id in getThemeID['ID']:
            find = ipea.metadata(theme_id=id)
            find = find[find['MEASURE'].str.contains("\\$")]
            found = pd.concat([found, find])
        found = found.sort_values(by='CODE')
    return "Não Encontrado" if found.empty else found


def code(phrase: str):
    """
    Retorna um dataframe contendo as series com dados financeiros do IPEA de acordo com a string parametrizada referente ao código procurado.

    Caso a busca não seja bem sucedida sera retornado uma string "Não Encontrado".
    """
    code = ipea.metadata()
    code = code[code["MEASURE"].str.contains("\\$")]
    code = code[code["CODE"].str.contains(phrase.upper())]
    code = code.sort_values(by='CODE')
    return "Não Encontrado" if code.empty else code


def filtro(organizacao_usuario: str, tema_usuario: str, codigo_usuario: str, data_inicio_usuario: str, data_fim_usuario: str, pais_usuario: str, frequencia_usuario: str, unidade_usuario: str, subtema_usuario: str) -> pd.DataFrame:
    """
    Filtra os metadados do IPEA com base nos critérios fornecidos pelo usuário e prepara os dados para visualização.
    
    Parâmetros:
    -----------
    organizacao_usuario : str
        Nome ou acrônimo da organização que publicou os dados.
    tema_usuario : str
        Nome do tema dos dados.
    codigo_usuario : str
        Código específico do indicador (por exemplo, 'IGP-DI').
    data_inicio_usuario : str
        Data de início para o filtro, no formato 'AAAA-MM-DD'.
    data_fim_usuario : str
        Data de fim para o filtro, no formato 'AAAA-MM-DD'.
    pais_usuario : str
        País ao qual os dados se referem.
    frequencia_usuario : str
        Frequência dos dados (por exemplo, 'anual', 'mensal').
    unidade_usuario : str
        Unidade de medida dos dados (por exemplo, 'USD', 'toneladas').
    subtema_usuario : str
        Subtema relacionado aos dados.
    
    Retorna:
    --------
    pd.DataFrame
        DataFrame com os metadados filtrados, removendo duplicatas e pré-processado para visualização.
    
    Exceções:
    ----------
    ValueError
        Se as datas fornecidas estiverem em um formato inválido.
    """

    # Carrega metadados iniciais e filtra por medidas com símbolo "$"
    informacoes = ipea.metadata()
    informacoes = informacoes[informacoes["MEASURE"].str.contains("\\$")]
    
    # Lista para armazenar DataFrames filtrados
    filtros = [informacoes]

    
    # Filtra pelo código do usuário
    if codigo_usuario.strip():
        filtros.append(informacoes[informacoes["CODE"].str.contains(codigo_usuario.upper())])

    # Filtra pela organização
    if organizacao_usuario.strip():
        org_mask = informacoes["SOURCE ACRONYM"].str.lower().str.contains(organizacao_usuario.lower()) | \
                   informacoes["SOURCE"].str.lower().str.contains(organizacao_usuario.lower())
        filtros.append(informacoes[org_mask])

    # Filtra pelo tema
    if tema_usuario.strip():
        temas = ipea.themes()
        temas_filtrados = temas[temas['NAME'].str.lower().str.contains(tema_usuario.lower())]
        if not temas_filtrados.empty:
            for theme_id in temas_filtrados['ID']:
                filtros.append(ipea.metadata(theme_id=theme_id))

    # Filtra pelas datas (com validação)
    if data_inicio_usuario.strip() or data_fim_usuario.strip():
        informacoes["LAST UPDATE"] = pd.to_datetime(informacoes["LAST UPDATE"], errors="coerce")
        try:
            data_inicio = pd.to_datetime(data_inicio_usuario.strip(), format="%Y-%m-%d") if data_inicio_usuario.strip() else None
            data_fim = pd.to_datetime(data_fim_usuario.strip(), format="%Y-%m-%d") if data_fim_usuario.strip() else None
        except ValueError as e:
            raise ValueError(f"Formato de data inválido: {e}")

        # Cria máscara para filtrar por data
        date_mask = pd.Series([True] * len(informacoes))
        if data_inicio is not None:
            date_mask &= informacoes["LAST UPDATE"] >= data_inicio
        if data_fim is not None:
            date_mask &= informacoes["LAST UPDATE"] <= data_fim
        filtros.append(informacoes[date_mask])

    # Filtra por país
    if pais_usuario.strip():
        filtros.append(informacoes[informacoes["COUNTRY"].str.lower().str.contains(pais_usuario.lower())])

    # Filtra por frequência
    if frequencia_usuario.strip():
        filtros.append(informacoes[informacoes["FREQUENCY"].str.lower().str.contains(frequencia_usuario.lower())])

    # Filtra por unidade
    if unidade_usuario.strip():
        filtros.append(informacoes[informacoes["UNIT"].str.lower().str.contains(unidade_usuario.lower())])

    # Filtra por subtema
    if subtema_usuario.strip():
        filtros.append(informacoes[informacoes["SUBTHEME"].str.lower().str.contains(subtema_usuario.lower())])

    # Junta todos os filtros e remove duplicatas
    informacoes_final = pd.concat(filtros).drop_duplicates().reset_index(drop=True)

    # Remove valores nulos e organiza colunas para visualização
    informacoes_final.dropna(inplace=True)
    informacoes_final.sort_values(by=["LAST UPDATE", "CODE"], ascending=[False, True], inplace=True)

    # Prepara para gráficos: conversão para séries temporais
    if not informacoes_final.empty and "LAST UPDATE" in informacoes_final.columns:
        informacoes_final.set_index("LAST UPDATE", inplace=True)
        informacoes_final.sort_index(inplace=True)

    return informacoes_final
