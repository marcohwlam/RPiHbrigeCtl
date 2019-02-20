class RoomClean:
    def cleanRoom(self, robot):
        path = set()

        def dfs(x, y, dx, dy):
            # 1, Clean current
            robot.clean();
            path.add((x, y))

            # 2, Clean next
            for _ in range(4):
                if (x + dx, y + dy) not in path and robot.move():
                    dfs(x + dx, y + dy, dx, dy)
                robot.turnLeft()
                dx, dy = -dy, dx

            # 3, Back to previous position and direction
            robot.turnLeft();
            robot.turnLeft()
            robot.move()
            robot.turnLeft();
            robot.turnLeft()

        dfs(0, 0, 0, 1)
