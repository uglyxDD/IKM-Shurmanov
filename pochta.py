class PostmanProblemSolver:
    def __init__(self):
        self.M = 0 
        self.letters = []  
        self.graph = []
        self.parent = []
        self.depth = []

    def read_input(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
            if not lines:
                raise ValueError("Файл пуст")
                
            self.M = int(lines[0])
            if not (0 < self.M < 1000):
                raise ValueError("M должно быть в интервале (0, 1000)")
                
            self.letters = [0] * (self.M + 1)  # индексация с 1
            self.graph = [[] for _ in range(self.M + 1)]
            
            for i in range(1, self.M + 1):
                if i >= len(lines):
                    raise ValueError(f"Недостаточно данных для узла {i}")
                    
                data = lines[i].split()
                if len(data) < 2:
                    raise ValueError(f"Для узла {i} ожидается минимум 2 числа")
                    
                try:
                    ni = int(data[0])  #количество соседей
                    li = int(data[1])  #количество писем
                except ValueError:
                    raise ValueError(f"Некорректные числовые данные для узла {i}")
                    
                self.letters[i] = li
                
                if len(data) < 2 + ni:
                    raise ValueError(f"Для узла {i} указано недостаточно соседей")
                    
                neighbors = []
                for j in range(2, 2 + ni):
                    try:
                        neighbor = int(data[j])
                        if not (1 <= neighbor <= self.M):
                            raise ValueError(f"Неверный номер узла {neighbor}")
                        neighbors.append(neighbor)
                    except ValueError:
                        raise ValueError(f"Некорректный номер соседа для узла {i}")
                self.graph[i] = neighbors
                
        except Exception as e:
            print(f"\nОшибка при чтении файла: {e}")
            print("Проверьте формат входных данных и попробуйте снова.")
            exit(1)

    def build_tree(self):
        self.parent = [0] * (self.M + 1)
        self.depth = [-1] * (self.M + 1)
        visited = [False] * (self.M + 1)
        queue = [1] 
        
        visited[1] = True
        self.depth[1] = 0
        self.parent[1] = 0
        
        while queue: #обход в ширину
            node = queue.pop(0)
            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    self.depth[neighbor] = self.depth[node] + 1
                    self.parent[neighbor] = node
                    queue.append(neighbor)

    def __collect_target_nodes(self):
        target_nodes = set()
        for i in range(1, self.M + 1):
            if self.letters[i] > 0:
                target_nodes.add(i)
        return target_nodes
    
    def __build_subtree(self, target_nodes):
        subtree = set()
        for node in target_nodes:
            current = node
            while current != 0:
                subtree.add(current)
                current = self.parent[current]
        return subtree if subtree else {1}  # Если писем нет - только корень
    
    def _calculate_apologies(self, subtree, target_nodes):
        size = len(subtree)    
        K = len(target_nodes)
        
        max_depth = 0
        if target_nodes:
            for node in target_nodes:
                if self.depth[node] > max_depth:
                    max_depth = self.depth[node]
        
        total_visits = 2 * (size - 1) - max_depth + 1 #Формула для расчёта извинений
        return total_visits - K
    
    def solve(self):
        target_nodes = self.__collect_target_nodes()
        subtree = self.__build_subtree(target_nodes)
        return self._calculate_apologies(subtree, target_nodes)

def display_welcome():
    print("\n" + "="*50)
    print(" ПРОГРАММА РАСЧЕТА МАРШРУТА ПОЧТАЛЬОНА")
    print("="*50)
    print("\nОписание задачи:")
    print("Тритон должен доставить письма птицам в гнездах на дубе.")
    print("При проходе через гнездо без доставки письма, он должен извиниться.")
    print("Программа рассчитывает минимальное количество таких извинений.\n")

def get_input_filename():
    while True:
        filename = input("Введите имя файла с данными (например, input.txt): ")
        if filename.strip():
            return filename
        print("Ошибка: имя файла не может быть пустым!")

def display_result(result):
    print("\n" + "="*50)
    print(f" РЕЗУЛЬТАТ: тритону придется извиниться {result} раз")
    print("="*50 + "\n")

def save_result(result, filename="output.txt"):
    try:
        with open(filename, 'w') as f:
            f.write(str(result))
        print(f"Результат сохранен в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результата: {e}")

def main():
    display_welcome()
    
    filename = get_input_filename()
    
    try:
        solver = PostmanProblemSolver()
        solver.read_input(filename)
        solver.build_tree()
        
        result = solver.solve()
        display_result(result)
        
        save = input("Сохранить результат в файл? (y/n): ").lower()
        if save == 'y':
            save_result(result)
            
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Программа завершена с ошибкой.")
    finally:
        print("\nСпасибо за использование программы!")

main()