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
    positions = {}
    for y, row in enumerate(map_lines):
        for x, char in enumerate(row):
            if char in "EDLMWS":
                positions[char] = (y, x)
    return positions

# Função heurística (distância de Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Implementação do algoritmo A*
def astar(start, goal):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    heapq.heapify(open_set)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        y, x = current
        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (y + dy, x + dx)
            if 0 <= neighbor[0] < len(map_lines) and 0 <= neighbor[1] < len(map_lines[0]):
                terrain_cost = char_to_terrain.get(map_lines[neighbor[0]][neighbor[1]], None)
                if terrain_cost is not None:
                    tentative_g_score = g_score[current] + terrain_cost
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        came_from[neighbor] = current
    return None

# Desenha o mapa na tela com Pygame
def draw_map(screen, path=[], current_pos=None, cost=0, elapsed_time=0):
    screen.fill((0, 0, 0))
    colors = {'.': (200, 200, 200), '~': (100, 100, 255), 'R': (255, 0, 0), 'P': (139, 69, 19), '#': (50, 50, 50),
              'D': (255, 165, 0), 'L': (255, 165, 0), 'M': (255, 165, 0), 'W': (255, 165, 0)}  # Destinos destacados
    for y, row in enumerate(map_lines):
        for x, char in enumerate(row):
            color = colors.get(char, (255, 255, 255))
            if (y, x) in path:
                color = (0, 255, 0)
            if (y, x) == current_pos:
                color = (255, 255, 0)
            pygame.draw.rect(screen, color, (x * tile_size, y * tile_size, tile_size, tile_size))
    font = pygame.font.Font(None, 24)
    text = font.render(f'Custo: {cost}', True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.topleft = (10, 10)
    pygame.draw.rect(screen, (0, 0, 0), text_rect)  # Background para legibilidade do texto
    screen.blit(text, text_rect)
    
    time_text = font.render(f'Tempo: {elapsed_time:.2f}s', True, (255, 255, 255))
    time_text_rect = time_text.get_rect()
    time_text_rect.topleft = (10, 40)
    pygame.draw.rect(screen, (0, 0, 0), time_text_rect)
    screen.blit(time_text, time_text_rect)
    
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((len(map_lines[0]) * tile_size, len(map_lines) * tile_size))
    positions = find_positions()
    order = ['D', 'L', 'M', 'W', 'S']
    current_pos = positions['E']
    total_path = []
    total_cost = 0
    
    start_time = time.time()
    
    for person in order:
        path = astar(current_pos, positions[person])
        if path:
            previous_terrain = map_lines[current_pos[0]][current_pos[1]]
            for step in path:
                current_terrain = map_lines[step[0]][step[1]]
                if current_terrain != previous_terrain:
                    translated_terrain = terrain_translation.get(current_terrain, current_terrain)
                    print(f'Tipo de terreno: {translated_terrain}')
                if current_terrain in "DLMW":
                    print(f'Encontrou um amigo na posição: {step}')
                if current_terrain in "P":
                    print(f'Passou por uma porta na posição: {step}')
                if current_terrain in "S":
                    print(f'Encontrou a saída na posição: {step}')
                total_cost += char_to_terrain[current_terrain]
                total_path.append(step)
                elapsed_time = time.time() - start_time
                draw_map(screen, total_path, step, total_cost, elapsed_time)
                time.sleep(0.1)
                previous_terrain = current_terrain
            current_pos = positions[person]
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Custo total: {total_cost}')
    print(f'Tempo total: {elapsed_time:.2f} segundos')
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
