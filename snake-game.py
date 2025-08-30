import tkinter as tk
import random

# 게임 설정
WIDTH = 400
HEIGHT = 400
SEG_SIZE = 20
INIT_LENGTH = 3
DELAY = 100  # ms

# 방향 정의
DIRECTIONS = {
    "Left": (-1, 0),
    "Right": (1, 0),
    "Up": (0, -1),
    "Down": (0, 1)
}

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()
        self.direction = "Right"
        self.snake = []
        self.food = None
        self.running = True
        self.score = 0

        # 초기화
        self.init_snake()
        self.create_food()
        self.master.bind("<Key>", self.on_key_press)
        self.run_game()

    def init_snake(self):
        self.snake = []
        start_x = WIDTH // 2
        start_y = HEIGHT // 2
        for i in range(INIT_LENGTH):
            x = start_x - i * SEG_SIZE
            y = start_y
            seg = self.canvas.create_rectangle(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="green")
            self.snake.append(seg)

    def create_food(self):
        while True:
            x = random.randint(0, (WIDTH - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            y = random.randint(0, (HEIGHT - SEG_SIZE) // SEG_SIZE) * SEG_SIZE
            overlap = False
            for seg in self.snake:
                coords = self.canvas.coords(seg)
                if coords[0] == x and coords[1] == y:
                    overlap = True
                    break
            if not overlap:
                break
        if self.food:
            self.canvas.delete(self.food)
        self.food = self.canvas.create_oval(x, y, x+SEG_SIZE, y+SEG_SIZE, fill="red")

    def on_key_press(self, event):
        key = event.keysym
        if self.running:
            if key in DIRECTIONS:
                # 반대 방향으로는 이동 불가
                if (self.direction == "Left" and key != "Right") or \
                   (self.direction == "Right" and key != "Left") or \
                   (self.direction == "Up" and key != "Down") or \
                   (self.direction == "Down" and key != "Up"):
                    self.direction = key
        else:
            if key == "space":
                self.reset_game()

    def run_game(self):
        if self.running:
            self.move_snake()
            self.master.after(DELAY, self.run_game)

    def move_snake(self):
        dx, dy = DIRECTIONS[self.direction]
        head_coords = self.canvas.coords(self.snake[0])
        new_x = head_coords[0] + dx * SEG_SIZE
        new_y = head_coords[1] + dy * SEG_SIZE

        # 벽 충돌 체크
        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            self.game_over()
            return

        # 자기 몸 충돌 체크
        for seg in self.snake[1:]:
            coords = self.canvas.coords(seg)
            if coords[0] == new_x and coords[1] == new_y:
                self.game_over()
                return

        # 이동
        new_head = self.canvas.create_rectangle(new_x, new_y, new_x+SEG_SIZE, new_y+SEG_SIZE, fill="green")
        self.snake = [new_head] + self.snake

        # 먹이 먹었는지 체크
        food_coords = self.canvas.coords(self.food)
        if food_coords[0] == new_x and food_coords[1] == new_y:
            self.score += 1
            self.create_food()
        else:
            tail = self.snake.pop()
            self.canvas.delete(tail)

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="게임 오버!", fill="red", font=("Arial", 30))
        self.canvas.create_text(WIDTH//2, HEIGHT//2+40, text=f"점수: {self.score}", fill="black", font=("Arial", 20))
        self.canvas.create_text(WIDTH//2, HEIGHT//2+80, text="스페이스바로 재시작", fill="gray", font=("Arial", 15))

    def reset_game(self):
        self.canvas.delete("all")
        self.direction = "Right"
        self.snake = []
        self.food = None
        self.running = True
        self.score = 0
        self.init_snake()
        self.create_food()
        self.run_game()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("지렁이 게임")
    game = SnakeGame(root)
    root.mainloop()
