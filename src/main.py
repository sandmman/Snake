import snake

def grid_size():
    print "How big of a grid? "
    s = raw_input("Please choose 270,300,330,420 ")
    snake.size = int(s)
    return s + "x" + s

if __name__ == "__main__":
    size = grid_size()

    snake.app = snake.Snake(None)
    snake.app.geometry(size)
    snake.app.title("Snake - Score: 0")
    snake.app.mainloop()
