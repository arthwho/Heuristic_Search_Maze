
[Especificações do projeto](Trabalho%20-%20Busca%20Heurística.pdf)

# Visão Geral
Este código implementa uma simulação da busca de caminho para Eleven resgatar seus amigos e escapar do laboratório, utilizando o algoritmo A* e visualização com a biblioteca Pygame. O agente percorre o mapa evitando obstáculos, considerando os custos dos terrenos e buscando o menor caminho para cada destino.

# Estrutura do Código

## 1. Mapeamento do Terreno
O mapa é representado por uma matriz de strings onde cada caractere representa um tipo de terreno ou elemento do cenário. Os custos para cada tipo de terreno são definidos no dicionário `char_to_terrain`.

## 2. Funções

### `find_positions()`
**Descrição:** Encontra e armazena as posições iniciais de todos os personagens e pontos importantes no mapa.

**Parâmetros:** Nenhum.

**Retorno:**
- Um dicionário com as posições dos personagens e da saída.

### `heuristic(a, b)`
**Descrição:** Calcula a distância de Manhattan entre dois pontos do mapa.

**Parâmetros:**
- `a`: Tupla representando um ponto `(y, x)`.
- `b`: Tupla representando um ponto `(y, x)`.

**Retorno:**
- Valor inteiro representando a distância heurística.

### `astar(start, goal)`
**Descrição:** Implementa o algoritmo A* para encontrar o caminho de menor custo entre `start` e `goal`.

**Parâmetros:**
- `start`: Coordenada inicial `(y, x)`.
- `goal`: Coordenada de destino `(y, x)`.

**Retorno:**
- Lista de coordenadas do caminho ótimo do ponto de partida até o destino.

### `draw_map(screen, path=[], current_pos=None, cost=0, elapsed_time=0)`
**Descrição:** Renderiza o mapa na tela do Pygame, destacando os caminhos percorridos e a posição atual do agente.

**Parâmetros:**
- `screen`: Tela do Pygame.
- `path`: Lista de coordenadas já percorridas.
- `current_pos`: Coordenada atual do agente.
- `cost`: Custo acumulado do caminho.
- `elapsed_time`: Tempo decorrido desde o início da simulação.

### `main()`
**Descrição:**
- Inicializa a tela do Pygame.
- Define a sequência de objetivos para Eleven.
- Utiliza o algoritmo A* para encontrar os caminhos e exibe a movimentação no mapa.
- Exibe o custo total do trajeto ao final da execução.
- Mantém a janela aberta até que o usuário a feche.

**Parâmetros:** Nenhum.

## 3. Dicionários de Mapeamento

### `char_to_terrain`
**Descrição:** Mapeia cada tipo de terreno a um custo específico.

**Exemplo:**
- `'.'`: 1 (Piso seco)
- `'~'`: 3 (Piso molhado)
- `'R'`: 6 (Fiação exposta)
- `'P'`: 4 (Porta)
- `'#'`: None (Parede, intransponível)
- `'E'`: 1 (Entrada)
- `'D'`: 1 (Destino 1)
- `'L'`: 1 (Destino 2)
- `'M'`: 1 (Destino 3)
- `'W'`: 1 (Destino 4)
- `'S'`: 1 (Saída)

### `terrain_translation`
**Descrição:** Mapeia cada tipo de terreno a uma tradução legível.

**Exemplo:**
- `'.'`: "Piso seco"
- `'~'`: "Piso molhado"
- `'R'`: "Fiação exposta"
- `'P'`: "Porta"
- `'S'`: "Saída"

# Alteração dos Destinos
Os destinos podem ser alterados modificando a lista `order` dentro da função `main()`. Atualmente, a ordem padrão é `['D', 'L', 'M', 'W', 'S']`, mas pode ser personalizada para testes diferentes.

# Melhorias Visuais
- **Pontos de destino (D, L, M, W)** foram destacados em laranja para melhor visibilidade.
- **O agente é destacado em amarelo**, diferenciando-o do caminho já percorrido (verde).

# Conclusão
O código implementa uma solução eficiente para o problema de busca, permitindo visualizar o percurso do agente e calcular o custo total do caminho. A modularidade das funções facilita testes e ajustes futuros.