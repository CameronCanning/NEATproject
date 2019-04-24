import neat
import pygame
import sys
from tkinter import *

def next_gen():
    population.next_generation(int(gen_txt.get()))
    #population.rank_and_remove(True)
    gen.config(text='  Generation: '+str(population.generation))
    pop_size.config(text='  Size: '+str(population.size))
    species_size.config(text='  Species: '+str(len(population.species)))
    top_fitness.config(text='  Top Fitness: '+str(population.top_genome.fitness))
    avg_fitness.config(text='  Avg Fitness: '+str(round(population.average_fitness,3)))
    #population.breed()
    #population.evaluate_fitness()
    #population.generation += 1
def show_genome():
    print(population.top_genome)
    sys.stdout.flush()
def play():
    population.setup_player()

    WHITE = (255, 255, 255)
    BLACK = (0, 0 ,0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GRAY = (50, 50, 50)
    RED = (255, 0, 0)

    cell = 20
    dimention = 25
    margin = 3
    side_width = 100
    size = margin + ((margin + cell) * dimention)

    pygame.init()
    screen = pygame.display.set_mode([size, size])
    pygame.display.set_caption('Round')
    clock = pygame.time.Clock()
    playing = True

    time_elapsed = 0
    dt = 0
    done = False
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if done:
            playing = False
        for y in range(0, dimention):
            for x in range(0, dimention):
                if population.game.board[x][y]:
                    pygame.draw.rect(screen, BLACK,
                                    [(cell + margin) * x + margin,
                                     (cell + margin) * y + margin,
                                     cell,
                                     cell])
                elif population.game.start == (x, y):
                    pygame.draw.rect(screen, RED,
                                    [(cell + margin) * x + margin,
                                     (cell + margin) * y + margin,
                                     cell,
                                     cell])
                elif population.game.end == (x, y):
                    pygame.draw.rect(screen, GREEN,
                                    [(cell + margin) * x + margin,
                                     (cell + margin) * y + margin,
                                     cell,
                                     cell])
                elif population.game.player.position == (x, y):
                    pygame.draw.rect(screen, BLUE,
                                    [(cell + margin) * x + margin,
                                     (cell + margin) * y + margin,
                                     cell,
                                     cell])
                else:
                    pygame.draw.rect(screen, WHITE,
                                    [(cell + margin) * x + margin,
                                     (cell + margin) * y + margin,
                                     cell,
                                     cell])


        time_elapsed += dt

        if time_elapsed > 100 and not done:
            done = population.game.move_top()
            time_elapsed = 0
        dt = clock.tick(60)
        pygame.display.flip()

population = neat.Population()

window = Tk()
window.title('NEATProject')
window.geometry('400x120')

btn_frame = Frame(window)
btn_frame.grid(column=0, row=0, padx=2, pady=2)

output_frame = Frame(window)
output_frame.grid(column=1, row=0)

gen_btn = Button(btn_frame, text = "Next Generation",command=next_gen)
gen_btn.grid(column=0, row=0, padx=2, pady=2)

gen_txt = Entry(btn_frame, width=5)
gen_txt.insert(END, '1')
gen_txt.grid(column=1, row=0, padx=2, pady=2)

play_btn = Button(btn_frame, text = 'Play', command=play)
play_btn.grid(column=0, row=1, sticky='ew', padx=2, pady=2)

show_gen = Button(btn_frame, text= 'Show Genome', command=show_genome)
show_gen.grid(column=0, row=2, sticky='ew',padx=2, pady=2)

pop_title = Label(output_frame, text='Population: ')
pop_title.grid(column=0, row=0, sticky='w')

gen = Label(output_frame, text='  Generation: '+str(population.generation))
gen.grid(column=0, row=0, stick='w')

pop_size = Label(output_frame, text='  Size: '+str(population.size))
pop_size.grid(column=0, row=1, sticky='w')

species_size = Label(output_frame, text='  Species: '+str(len(population.species)))
species_size.grid(column=0, row=2, sticky='w')

top_fitness = Label(output_frame, text='  Top Fitness: '+str(population.top_genome.fitness))
top_fitness.grid(column=0, row=3, sticky='w')

avg_fitness = Label(output_frame, text='  Avg Fitness: '+str(population.average_fitness))
avg_fitness.grid(column=0, row=4, sticky='w')

window.mainloop()
