import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus

def buscar_perfumes_por_nome(nome_perfume):
    base_url = 'https://www.thekingofparfums.com.br/search/'
    page_number = 1
    resultados = []

    while True:
        url = urljoin(base_url, f'?q={quote_plus(nome_perfume)}&page={page_number}')
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            search_results = soup.find('div', class_='search-results-container')
            if search_results and search_results.text.strip() == 'Nenhum resultado encontrado para a pesquisa.':
                return 'Nenhum resultado encontrado para a pesquisa.'

            itens_perfume = soup.find_all('div', class_='span3 item-container m-bottom-half')

            if len(itens_perfume) == 1:
                nome = itens_perfume[0].find('a', class_='js-item-name').text.strip()
                preco = itens_perfume[0].find('span', class_='js-price-display').text.strip()
                resultados.append({'nome': nome, 'preco': preco})
            else:
                for item in itens_perfume:
                    nome = item.find('a', class_='js-item-name').text.strip()
                    preco = item.find('span', class_='js-price-display').text.strip()
                    resultados.append({'nome': nome, 'preco': preco})

            if not soup.find('a', class_='page-next'):
                break

            page_number += 1
        else:
            return f'Falha ao obter a página: {response.status_code}'

    return resultados

nome_perfume = input('Digite o nome do perfume: ')

resultados = buscar_perfumes_por_nome(nome_perfume)
if isinstance(resultados, str):
    print(resultados)
else:
    for i, resultado in enumerate(resultados, start=1):
        print(f'Perfume {i}:')
        print(f'  Nome: {resultado["nome"]}')
        print(f'  Preço: {resultado["preco"]}')

    if len(resultados) > 1:
        while True:
            escolha = input('Selecione o número do perfume desejado: ')
            if escolha.isdigit() and 1 <= int(escolha) <= len(resultados):
                escolha = int(escolha)
                print(f'Você selecionou o Perfume {escolha}:')
                print(f'  Nome: {resultados[escolha - 1]["nome"]}')
                print(f'  Preço: {resultados[escolha - 1]["preco"]}')
                break
            else:
                print('Escolha inválida. Por favor, selecione um número válido.')

# segunda busca ////////////////////////////////////////////////////////////////////////////////////////
                
def pequiperfumes_buscar(nome_perfume):
    base_url = 'https://www.pequiperfumes.com.br/search/'
    url = urljoin(base_url, f'?q={quote_plus(nome_perfume)}')
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        search_results = soup.find('div', class_='search-results-container')
        if search_results and search_results.text.strip() == 'Nenhum resultado encontrado para a pesquisa.':
            return 'Nenhum resultado encontrado para a pesquisa.'

        resultados = []

        itens_perfume = soup.find_all('div', class_='span3 item-container m-bottom-half')

        for item in itens_perfume:
            nome_element = item.find('a', class_='item-name')
            preco_element = item.find('span', class_='preco-produto')
            if nome_element and preco_element:
                nome = nome_element.text.strip()
                preco = preco_element.text.strip()
                resultados.append({'nome': nome, 'preco': preco})

        return resultados
    else:
        return f'Falha ao obter a página: {response.status_code}'

# Solicitando ao usuário que digite o nome do perfume a ser buscado
nome_perfume = input('Digite o nome do perfume: ')

# Buscando perfumes no site "pequiperfumes.com.br" com base no nome fornecido
resultados = pequiperfumes_buscar(nome_perfume)

# Verificando se a busca retornou uma mensagem de erro
if isinstance(resultados, str):
    print(resultados)  # Imprimindo a mensagem de erro
else:
    # Imprimindo os resultados encontrados
    for i, resultado in enumerate(resultados, start=1):
        print(f'Perfume {i}:')
        print(f'  Nome: {resultado["nome"]}')
        print(f'  Preço: {resultado["preco"]}')