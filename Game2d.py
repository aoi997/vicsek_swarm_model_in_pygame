


import os, sys, time, platform, pygame
from pygame.locals import *
print("=========================================================")
import numpy as np
# from VicsekModel import Agent, World, get_neighbors
from AgentWorld import Agent, World

# parameters setting

# world
size                    =   (1000, 800)
if_render               =   1                   # if_render
if_save                 =   0                   # if save pictures
draw_radius             =   10
max_setp                =   80                  # max steps in one episode
n_agents                =   20
fps                     =   1
max_turning_angle       =   15                  # max turning angle for each step

# agent
step_length             =   50                  # plot length
velocity                =   20                  # step length
view_range              =   0


if __name__ == '__main__':
    print("start gaming ...")

    for epoch in range(2):
        for episode in range(2):

            swarm = []

            # world = World(length=screen_size[0], wide=screen_size[1],
            #               global_awareness=per_rad, max_step_rad=max_step_rad)

            for id in range(n_agents):
                swarm += [Agent(
                    id=id,
                    step_length=step_length,
                    vel=velocity,
                    view_range=view_range
                )]

            env = World(
                size=size,
                agent_lst=swarm,
                if_render=if_render,
                if_save=if_save,
                fps=fps,
                max_turning_angle=max_turning_angle,
                draw_radius=draw_radius
            )

            # reset swarm positions, headings
            env.reset()

            now_step = 0

            while now_step < max_setp:

                print("=========================================================")

                print("epoch {}, episode {}, step {}".format(epoch,episode,now_step))

                if env.if_render:
                    env.render()

                # vicsek rule

                env.step()

                if env.if_render:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()  # end running

                now_step += 1

            if env.if_render:
                env.close()

        print("in epoch {}, end all episode".format(epoch))

    print("end all epoch")
