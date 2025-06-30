class FileReader:
    """Класс для чтения и хранения данных из входного файла
    
    Атрибуты:
        M (int): Количество гнезд на дубе
        letters (list): Количество писем для каждого гнезда (индексация с 1)
        graph (list): Список смежности для дерева гнезд
    """
    
    def __init__(self):
        self.M = 0
        self.letters = []
        self.graph = []
    
    def read_file(self, filename: str) -> None:
        """Читает данные из файла и сохраняет их в атрибутах класса
        
        Args:
            filename (str): Путь к входному файлу
            
        Raises:
            ValueError: Если файл содержит некорректные данные
            FileNotFoundError: Если файл не существует
        """
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
                    ni = int(data[0])  # количество соседей
                    li = int(data[1])  # количество писем
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
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не найден")
        except Exception as e:
            raise ValueError(f"Ошибка при чтении файла: {e}")


class TreeBuilder:
    """Класс для построения дерева и вычисления структур данных
    
    Атрибуты:
        parent (list): Список родителей для каждого узла
        depth (list): Список глубин для каждого узла
    """
    
    def __init__(self, file_reader):
        """Инициализирует класс с данными из FileReader
        
        Args:
            file_reader (FileReader): Объект с прочитанными данными
        """
        self.M = file_reader.M
        self.letters = file_reader.letters
        self.graph = file_reader.graph
        self.parent = []
        self.depth = []
    
    def build_tree(self) -> None:
        """Строит дерево гнезд, вычисляя родителей и глубину для каждого узла"""
        self.parent = [0] * (self.M + 1)
        self.depth = [-1] * (self.M + 1)
        visited = [False] * (self.M + 1)
        queue = [1] 
        
        visited[1] = True
        self.depth[1] = 0
        self.parent[1] = 0
        
        while queue:  # обход в ширину
            node = queue.pop(0)
            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    self.depth[neighbor] = self.depth[node] + 1
                    self.parent[neighbor] = node
                    queue.append(neighbor)


class PostmanSolver:
    """Класс для решения задачи почтальона и расчета извинений"""
    
    def __init__(self, tree_builder):
        """Инициализирует класс с построенным деревом
        
        Args:
            tree_builder (TreeBuilder): Объект с построенным деревом
        """
        self.M = tree_builder.M
        self.letters = tree_builder.letters
        self.parent = tree_builder.parent
        self.depth = tree_builder.depth
    
    def solve(self) -> int:
        """Решает задачу и возвращает минимальное количество извинений
        
        Returns:
            int: Количество необходимых извинений
        """
        target_nodes = self._collect_target_nodes()
        subtree = self._build_subtree(target_nodes)
        return self._calculate_apologies(subtree, target_nodes)
    
    def _collect_target_nodes(self) -> set:
        """Собирает множество гнезд, куда нужно доставить письма
        
        Returns:
            set: Множество номеров гнезд с письмами
        """
        return {i for i in range(1, self.M + 1) if self.letters[i] > 0}
    
    def _build_subtree(self, target_nodes: set) -> set:
        """Строит поддерево из целевых узлов и их предков
        
        Args:
            target_nodes (set): Множество целевых гнезд
            
        Returns:
            set: Множество узлов поддерева
        """
        subtree = set()
        for node in target_nodes:
            current = node
            while current != 0:
                subtree.add(current)
                current = self.parent[current]
        return subtree if subtree else {1}  # если писем нет - только корень
    
    def _calculate_apologies(self, subtree: set, target_nodes: set) -> int:
        """Вычисляет количество извинений по формуле
        
        Args:
            subtree (set): Множество узлов поддерева
            target_nodes (set): Множество целевых гнезд
            
        Returns:
            int: Количество извинений
        """
        size = len(subtree)    
        K = len(target_nodes)
        
        max_depth = 0
        if target_nodes:
            for node in target_nodes:
                if self.depth[node] > max_depth:
                    max_depth = self.depth[node]
        
        total_visits = 2 * (size - 1) - max_depth + 1
        return total_visits - K


def display_welcome():
    print("\n" + "="*50)
    print(" ПРОГРАММА РАСЧЕТА МАРШРУТА ПОЧТАЛЬОНА")
    print("="*50)
    print("\nОписание задачи:")
    print("Тритон должен доставить письма птицам в гнездах на дубе.")
    print("При проходе через гнездо без доставки письма, он должен извиниться.")
    print("Программа рассчитывает минимальное количество таких извинений.\n")


def get_input_filename() -> str:
    """Запрашивает у пользователя имя входного файла
    
    Returns:
        str: Имя файла, введенное пользователем
    """
    while True:
        filename = input("Введите имя файла с данными (например, input.txt): ")
        if filename.strip():
            return filename
        print("Ошибка: имя файла не может быть пустым!")


def display_result(result: int) -> None:
    """Выводит результат работы программы
    
    Args:
        result (int): Количество извинений
    """
    print("\n" + "="*50)
    print(f" РЕЗУЛЬТАТ: тритону придется извиниться {result} раз")
    print("="*50 + "\n")


def save_result(result: int, filename: str = "output.txt") -> None:
    """Сохраняет результат в файл
    
    Args:
        result (int): Количество извинений
        filename (str, optional): Имя файла для сохранения. По умолчанию "output.txt".
    """
    try:
        with open(filename, 'w') as f:
            f.write(str(result))
        print(f"Результат сохранен в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении результата: {e}")


def main():
    """Основная функция программы"""
    display_welcome()
    
    filename = get_input_filename()
    
    try:
        file_reader = FileReader()
        file_reader.read_file(filename)
        tree_builder = TreeBuilder(file_reader)
        tree_builder.build_tree()
        solver = PostmanSolver(tree_builder)
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