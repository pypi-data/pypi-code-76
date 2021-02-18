from arcade import color, key
from arcade import *
import random
import time
import sys

SC_WIDTH = 1000
SC_HEIGHT = 700
SC_TITLE = "模拟新冠肺炎的传染"


# 模拟的学生
class Students:
    def __init__(self):
        self.color = color.GREEN
        self.radius = 12
        self.AxisRange = (0, 0, 0, 0)
        self.classroomNumber = 1
        self.x = 0
        self.y = 0
        self.move_y = random.random() + 0.1
        self.move_x = random.random() + 0.1
        self.isInfected = False
        self.back = False
        self.counts = 0

    def setup(self):
        draw_circle_filled(self.x, self.y, self.radius, self.color)
        if self.y >= 500 or self.y <= 200:
            if self.x - self.radius <= self.AxisRange[0]:
                self.x = self.AxisRange[0] + self.radius
            if self.x + self.radius >= self.AxisRange[1]:
                self.x = self.AxisRange[1] - self.radius

    def MoveInHallway(self):
        self.x += self.move_x
        self.y += self.move_y
        draw_circle_filled(self.x, self.y, self.radius, self.color)
        if self.x <= self.radius or self.x >= SC_WIDTH - self.radius:
            self.move_x = -self.move_x

        if self.y <= self.radius or self.y >= SC_HEIGHT - self.radius:
            self.move_y = -self.move_y

        if 200 + self.radius <= self.y <= 500 - self.radius:
            if self.y == 200 + self.radius or self.y == 500 + self.radius:
                if 184 <= self.x <= 204 or 388 <= self.x <= 408 or 592 <= self.x <= 612 or \
                        796 <= self.x <= 816:
                    self.move_x = -self.move_x
                else:
                    self.x += self.move_x
                    self.y += self.move_y
            else:
                self.x += self.move_x
                self.y += self.move_y

        if self.y > 500 - self.radius or self.y < 200 + self.radius:
            if self.radius <= self.x <= 184 - self.radius or \
                    204 + self.radius <= self.x <= 388 - self.radius or \
                    408 + self.radius <= self.x <= 592 - self.radius or \
                    612 + self.radius <= self.x <= 796 - self.radius or \
                    816 + self.radius <= self.x <= 1000 - self.radius:
                self.move_x = -self.move_x
                draw_circle_filled(self.x, self.y, self.radius, self.color)


# 教室
class Classroom:
    def __init__(self):
        self.color = color.WHITE

    def draw(self):
        draw_rectangle_filled(194, 100, 20, 200, self.color)
        draw_rectangle_filled(194, 600, 20, 200, self.color)
        draw_rectangle_filled(398, 100, 20, 200, self.color)
        draw_rectangle_filled(398, 600, 20, 200, self.color)
        draw_rectangle_filled(602, 100, 20, 200, self.color)
        draw_rectangle_filled(602, 600, 20, 200, self.color)
        draw_rectangle_filled(806, 100, 20, 200, self.color)
        draw_rectangle_filled(806, 600, 20, 200, self.color)


class Covid19(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.total_time = 0
        self.last_time = 0
        self.InfectRate = 0.3
        self.classroom = Classroom()
        self.students = [Students() for _ in range(100)]
        self.Infected = []
        self.Exposed = []
        self.Susceptible = []
        for stu in self.students:
            self.Susceptible.append(stu)

    def on_draw(self):
        start_render()
        set_background_color(color.BLACK)
        self.classroom.draw()
        for stu in self.students:
            stu.setup()

    def on_update(self, delta_time):
        self.total_time += delta_time
        for stu in self.students:
            stu.setup()
            stu.MoveInHallway()
        if int(self.total_time) != int(self.last_time) and int(self.total_time) % 1 == 0:
            self.Infect()
        self.last_time = self.total_time

    def number(self):
        lst = [10 for _ in range(10)]
        for i in range(100):
            while True:
                temp = random.choice([i for i in range(1, 11)])
                lst[temp - 1] -= 1
                if lst[temp - 1] < 0:
                    continue
                else:
                    break

            self.students[i].classroomNumber = temp
            if self.students[i].classroomNumber == 1:
                self.students[i].AxisRange = (0, 184, 500, 700)
            elif self.students[i].classroomNumber == 2:
                self.students[i].AxisRange = (204, 388, 500, 700)
            elif self.students[i].classroomNumber == 3:
                self.students[i].AxisRange = (408, 592, 500, 700)
            elif self.students[i].classroomNumber == 4:
                self.students[i].AxisRange = (612, 796, 500, 700)
            elif self.students[i].classroomNumber == 5:
                self.students[i].AxisRange = (816, 1000, 500, 700)
            elif self.students[i].classroomNumber == 6:
                self.students[i].AxisRange = (0, 184, 0, 200)
            elif self.students[i].classroomNumber == 7:
                self.students[i].AxisRange = (204, 388, 0, 200)
            elif self.students[i].classroomNumber == 8:
                self.students[i].AxisRange = (408, 592, 0, 200)
            elif self.students[i].classroomNumber == 9:
                self.students[i].AxisRange = (612, 796, 0, 200)
            elif self.students[i].classroomNumber == 10:
                self.students[i].AxisRange = (816, 1000, 0, 200)

    def Infect(self):
        if len(self.Susceptible) > 0:
            infected = [random.choice(self.Susceptible)
                        for _ in range(2*(len(self.Exposed) + len(self.Infected)))]
            try:
                for i in infected:
                    self.Susceptible.remove(i)
                    self.Exposed.append(i)
                    i.color = color.ORANGE
                for j in self.Exposed:
                    self.Infected.append(j)
                    self.Exposed.remove(j)
                    j.color = color.RED
            except ValueError:
                pass
        else:
            time.sleep(3)
            sys.exit()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.KEY_1:
            self.number()
            temp_list = []
            for stu in self.students:
                temp_list.append(stu)
            infected_student = random.choice(temp_list)
            infected_student.color = color.ORANGE
            self.Exposed.append(infected_student)
            self.Susceptible.remove(infected_student)
            for stu in self.students:
                stu.x = random.randint(stu.AxisRange[0], stu.AxisRange[1])
                stu.y = random.randint(stu.AxisRange[2], stu.AxisRange[3])
                stu.setup()
                draw_circle_filled(stu.x, stu.y, stu.radius, stu.color)


def main():
    Covid19(SC_WIDTH, SC_HEIGHT, SC_TITLE)
    run()


if __name__ == "__main__":
    main()
