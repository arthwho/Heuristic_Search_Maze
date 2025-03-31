import heapq
import pygame
import time

tile_size = 15
pygame.init()

map_lines = [
    "##########################################",
    "#..............#............#..~~........#",
    "#..RRR~.~RRRRR.P............#..~~..#RRR..#",
    "#..RRR..~RRRRR~#............#..~~..#RRR..#",
    "#..RRR.~~RRRRR~#....RRR.....#..~~..#RRR..#",
    "#..RRR.D......~#~~~.RRR.....#..~~..#RRR..#",
    "#..RRR...RR....#~~~.RRR.....#~.....#....E#",
    "#........RR....#~~~.RRR.....#~.....#######",
    "#..............#~~~.RRR.....#RRRRR.......#",
    "################~~~.RRR.....#RRRRR.......#",
    "#...............~~~.RRR.....#RRRRR.......#",
    "#...........................#............#",
    "#..................~~~~~~...###P##########",
    "#.....................~~~~...............#",
    "###P################.....~~~~~~~.........#",
    "#....~~~...........#.....................#",
    "#.........~~~~~....#RRRR################P#",
    "#...RRRRRRRRRRRRR..#RRRR#~...........M#..#",
    "#...~~~~.....~~....#....#.~..........#R..#",
    "#...~~~~.....~~....#....#..~~~......#RR..#",
    "#########.L..~~....#....#..~~~.....#RRR..#",
    "#.......#....~~....#....#..~~~....#RRR...#",
    "#.......#..........#....#..~~~...#RRR....#",
    "#.......#..........#....P..~~~..#RRRR....#",
    "#.......############....#..~...#RRRR.....#",
    "#...........RRRRR.......#..~..#RRRRR.....#",
    "#.~~~~~.....RRRRR.......#..~..#RRR.......#",
    "#.~~~~~RRRRRRRR.........#..~..#RR........#",
    "#.~~~~~RRR#####.........#.....#RR.~~~~...#",
    "#.....RR.#....#....~..R.#.....#RR.~~~~...#",
    "#~~~~...#..W..#....~..R.#.....#RR.~~~~...#",
    "#~~~..##......#.RRR~RRR.#.....#RR.~~~~...#",
    "#....#..RRR...#.......R.#######RR....RR#P#",
    "#...#...RRR...#RRRRR..RRRRRRRRRRR...RR#..#",
    "##P#....RRR...#.......R............RR#...#",
    "#....~~~RRR...#~~~.RRRR..........RRR#....#",
    "#....~~~......#~~~....R~~~~.....RRR#..~~~#",
    "###############~~~....R..~..RRRRRR#...~~~#",
    "#..............~~~....R..~..RRRRR#....~~~#",
    "#..............~~~.......~..RRRR#........#",
    "#...........................RRRRP........#",
    "########################################S#"
]

# Dicionário que mapeia cada tipo de terreno a um custo
char_to_terrain = {
    '.': 1, '~': 3, 'R': 6, 'P': 4, '#': None,
    'E': 1, 'D': 1, 'L': 1, 'M': 1, 'W': 1, 'S': 1
}

# Dicionário que mapeia cada tipo de terreno a uma tradução
terrain_translation = {
    '.': "Piso seco", '~': "Piso molhado", 'R': "Fiação exposta", 'P': "Porta", 'S': "Saída"
}

# Encontra as posições dos personagens no mapa
def find_positions():
    positions = {}  # Inicializa um dicionário vazio para armazenar as posições
    for y, row in enumerate(map_lines):  # Itera sobre cada linha do mapa com seu índice
        for x, char in enumerate(row):  # Itera sobre cada caractere da linha com seu índice
            if char in "EDLMWS":  # Verifica se o caractere é um dos personagens
                positions[char] = (y, x)  # Adiciona a posição do personagem ao dicionário
    return positions  # Retorna o dicionário com as posições dos personagens

# Função heurística (distância de Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Calcula e retorna a distância de Manhattan entre os pontos a e b

# Implementação do algoritmo A*
def astar(start, goal):
    open_set = [(0, start)]  # Inicializa a lista de nós abertos com o ponto de partida e custo 0
    came_from = {}  # Dicionário para rastrear o caminho
    g_score = {start: 0}  # Dicionário para armazenar o custo do caminho do início até o nó atual
    f_score = {start: heuristic(start, goal)}  # Dicionário para armazenar o custo estimado total do início até o objetivo
    heapq.heapify(open_set)  # Converte a lista de nós abertos em uma heap
    
    while open_set:  # Enquanto houver nós abertos
        _, current = heapq.heappop(open_set)  # Remove o nó com o menor f_score da heap
        if current == goal:  # Se o nó atual for o objetivo
            path = []  # Inicializa a lista do caminho
            while current in came_from:  # Reconstrói o caminho a partir do objetivo até o início
                path.append(current)  # Adiciona o nó atual ao caminho
                current = came_from[current]  # Atualiza o nó atual para o nó de onde veio
            path.append(start)  # Adiciona o ponto de partida ao caminho
            return path[::-1]  # Retorna o caminho na ordem correta (do início ao objetivo)
        
        y, x = current  # Obtém as coordenadas do nó atual
        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Itera sobre os vizinhos (cima, baixo, esquerda, direita)
            neighbor = (y + dy, x + dx)  # Calcula as coordenadas do vizinho
            if 0 <= neighbor[0] < len(map_lines) and 0 <= neighbor[1] < len(map_lines[0]):  # Verifica se o vizinho está dentro dos limites do mapa
                terrain_cost = char_to_terrain.get(map_lines[neighbor[0]][neighbor[1]], None)  # Obtém o custo do terreno do vizinho
                if terrain_cost is not None:  # Se o custo do terreno for válido
                    tentative_g_score = g_score[current] + terrain_cost  # Calcula o g_score tentativo do vizinho
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:  # Se o vizinho não estiver no g_score ou o g_score tentativo for menor
                        g_score[neighbor] = tentative_g_score  # Atualiza o g_score do vizinho
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)  # Calcula e atualiza o f_score do vizinho
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))  # Adiciona o vizinho à heap de nós abertos
                        came_from[neighbor] = current  # Atualiza o came_from do vizinho para o nó atual
    return None  # Retorna None se não encontrar um caminho

# Desenha o mapa na tela com Pygame
def draw_map(screen, path=[], current_pos=None, cost=0, elapsed_time=0):
    screen.fill((0, 0, 0))  # Preenche a tela com a cor preta
    colors = {'.': (200, 200, 200), '~': (100, 100, 255), 'R': (255, 0, 0), 'P': (139, 69, 19), '#': (50, 50, 50),
              'D': (255, 165, 0), 'L': (255, 165, 0), 'M': (255, 165, 0), 'W': (255, 165, 0)}  # Dicionário de cores para cada tipo de terreno
    for y, row in enumerate(map_lines):  # Itera sobre cada linha do mapa com seu índice
        for x, char in enumerate(row):  # Itera sobre cada caractere da linha com seu índice
            color = colors.get(char, (255, 255, 255))  # Obtém a cor do terreno atual
            if (y, x) in path:  # Se a posição estiver no caminho
                color = (0, 255, 0)  # Muda a cor para verde
            if (y, x) == current_pos:  # Se a posição for a posição atual
                color = (255, 255, 0)  # Muda a cor para amarelo
            pygame.draw.rect(screen, color, (x * tile_size, y * tile_size, tile_size, tile_size))  # Desenha um retângulo na tela com a cor definida
    font = pygame.font.Font(None, 24)  # Define a fonte do texto
    text = font.render(f'Custo: {cost}', True, (255, 255, 255))  # Renderiza o texto do custo
    text_rect = text.get_rect()  # Obtém o retângulo do texto
    text_rect.topleft = (10, 10)  # Define a posição do texto
    pygame.draw.rect(screen, (0, 0, 0), text_rect)  # Desenha um retângulo de fundo para o texto
    screen.blit(text, text_rect)  # Desenha o texto na tela
    
    time_text = font.render(f'Tempo: {elapsed_time:.2f}s', True, (255, 255, 255))  # Renderiza o texto do tempo decorrido
    time_text_rect = time_text.get_rect()  # Obtém o retângulo do texto do tempo
    time_text_rect.topleft = (10, 40)  # Define a posição do texto do tempo
    pygame.draw.rect(screen, (0, 0, 0), time_text_rect)  # Desenha um retângulo de fundo para o texto do tempo
    screen.blit(time_text, time_text_rect)  # Desenha o texto do tempo na tela
    
    pygame.display.flip()  # Atualiza a tela

def main():
    screen = pygame.display.set_mode((len(map_lines[0]) * tile_size, len(map_lines) * tile_size))  # Define o tamanho da tela com base no tamanho do mapa
    positions = find_positions()  # Encontra as posições dos personagens no mapa
    order = ['D', 'L', 'M', 'W', 'S']  # Define a ordem dos personagens a serem encontrados
    current_pos = positions['E']  # Define a posição inicial como a posição do personagem 'E'
    total_path = []  # Inicializa a lista do caminho total
    total_cost = 0  # Inicializa o custo total
    
    start_time = time.time()  # Marca o tempo de início
    
    for person in order:  # Para cada personagem na ordem
        path = astar(current_pos, positions[person])  # Encontra o caminho do A* do ponto atual até o personagem
        if path:  # Se o caminho for encontrado
            previous_terrain = map_lines[current_pos[0]][current_pos[1]]  # Obtém o terreno anterior
            for step in path:  # Itera sobre cada passo do caminho
                current_terrain = map_lines[step[0]][step[1]]  # Obtém o terreno atual
                if current_terrain != previous_terrain:  # Se o terreno atual for diferente do anterior
                    translated_terrain = terrain_translation.get(current_terrain, current_terrain)  # Obtém a tradução do terreno atual
                    print(f'Tipo de terreno: {translated_terrain}')  # Imprime o tipo de terreno
                if current_terrain in "DLMW":  # Se o terreno atual for um dos destinos
                    print(f'Encontrou um amigo na posição: {step}')  # Imprime a posição do amigo encontrado
                if current_terrain in "P":  # Se o terreno atual for uma porta
                    print(f'Passou por uma porta na posição: {step}')  # Imprime a posição da porta
                if current_terrain in "S":  # Se o terreno atual for a saída
                    print(f'Encontrou a saída na posição: {step}')  # Imprime a posição da saída
                total_cost += char_to_terrain[current_terrain]  # Atualiza o custo total
                total_path.append(step)  # Adiciona o passo ao caminho total
                elapsed_time = time.time() - start_time  # Calcula o tempo decorrido
                draw_map(screen, total_path, step, total_cost, elapsed_time)  # Desenha o mapa na tela
                time.sleep(0.1)  # Espera 0.1 segundos
                previous_terrain = current_terrain  # Atualiza o terreno anterior
            current_pos = positions[person]  # Atualiza a posição atual para a posição do personagem
    
    end_time = time.time()  # Marca o tempo de fim
    elapsed_time = end_time - start_time  # Calcula o tempo decorrido
    print(f'Custo total: {total_cost}')  # Imprime o custo total
    print(f'Tempo total: {elapsed_time:.2f} segundos')  # Imprime o tempo total
    
    while True:  # Mantém a janela do Pygame aberta
        for event in pygame.event.get():  # Para cada evento do Pygame
            if event.type == pygame.QUIT:  # Se o evento for de saída
                pygame.quit()  # Encerra o Pygame
                return  # Sai da função

if __name__ == "__main__":
    main()
