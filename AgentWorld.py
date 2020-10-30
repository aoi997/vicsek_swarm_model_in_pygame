import numpy as np
import pygame
import copy
import sys
from pygame.locals import *
from VicsekModel import vicsek_mean_vel_update

class Agent(object):

    def __init__(self, id, step_length, vel, view_range):

        # agent id
        self.id             =   id
        # plot length
        self.step_length    =   step_length             # plot 50
        # step length in world
        self.vel            =   vel                     # step 20


        # random course/heading
        self.course = np.random.uniform(0, 1*np.pi, 1)   # default: 0~2 pi course/heading

        # random position
        self.position       =   None

        self.view_range     =   view_range

        # neighbors
        self.neighbor_lst   =   []
        self.mean_course    =   None

        self.max_step_rad   =   None



    def update_state(self):     # update the situation of swarm

        while self.course >= 2*np.pi:
            self.course -= 2*np.pi
        while self.course < 0*np.pi:
            self.course += 2*np.pi

        # print("course ",self.course)

        self.pos[0] += self.vel * np.sin(self.course[0])
        self.pos[1] -= self.vel * np.cos(self.course[0])
        self.pos = np.round(self.pos)

        # print(
        #     "agent", self.id,
        #     "position", [int(i) for i in self.pos],
        #     "course", int(self.course * 180 / np.pi), "degree"
        # )


    def next_vector_pos(self):
        next_pos = copy.deepcopy(self.pos)
        next_pos[0] += self.step_length * np.sin(self.course[0])
        next_pos[1] -= self.step_length * np.cos(self.course[0])
        # print("next ",next_pos.tolist())
        self.next_pos_vector = next_pos
        return next_pos.tolist()


    def next_vector_arrow(self):
        arrow_course = copy.deepcopy(self.course)

        left_point = [1,1]
        left_point[0] = \
            self.next_pos_vector[0]-0.2*self.step_length*np.sin(0.75*np.pi-self.course[0])
        left_point[1] = \
            self.next_pos_vector[1]-0.2*self.step_length*np.cos(0.75*np.pi-self.course[0])

        right_point = [1,1]
        right_point[0] = \
            self.next_pos_vector[0]-0.2*self.step_length*np.sin(self.course[0]-0.25*np.pi)
        right_point[1] = \
            self.next_pos_vector[1]+0.2*self.step_length*np.cos(self.course[0]-0.25*np.pi)

        return left_point, right_point



class World(object):

    def __init__(self, size, agent_lst, if_render, if_save, fps,
                 max_turning_angle, draw_radius):

        self.length                 =   size[0]
        self.width                  =   size[1]
        self.agent_lst              =   agent_lst
        self.if_render              =   if_render
        self.if_save                =   if_save
        self.fps                    =   fps

        self.max_turning_rad        =   max_turning_angle * np.pi / 180
        for agent in self.agent_lst:
            agent.max_step_rad = self.max_turning_rad

        # plot agent size
        self.draw_radius            =   draw_radius

        # RGB
        self.WHITE                  =   (255, 255, 255)
        self.BLACK                  =   (  0,   0,   0)
        self.RED                    =   (255,   0,   0)
        self.GREEN                  =   (  0, 255,   0)
        self.BLUE                   =   (  0,   0, 255)
        self.YELLOW                 =   (255, 255,   0)
        self.QING_BLUE              =   (  0, 255, 255)
        self.GREY                   =   (192, 192, 192)

        if self.if_render:
            pygame.init()
            self.title   =  pygame.display.set_caption("vicsek swarm model 2D")
            self.window  =  pygame.display.set_mode((self.length, self.width))
            self.clock   =  pygame.time.Clock()

            self.window.fill(self.WHITE)


    def reset(self):


        for agent in self.agent_lst:
            x = np.random.uniform(self.length * 0.4, self.length * 0.6, 1)
            y = np.random.uniform( self.width * 0.4,  self.width * 0.6, 1)
            agent.pos = np.round(np.concatenate([x, y]))
            # print("agent {} pos {}".format(agent.id, agent.pos))



    def render(self):



        for agent in self.agent_lst:
            pos = []
            pos = [int(each) for each in agent.pos]
            print("agent {} pos {}".format(agent.id, pos))
            # position
            particle_content = pygame.draw.circle(self.window, self.GREY, pos, self.draw_radius, 0)
            particle_outline = pygame.draw.circle(self.window, self.BLACK, pos, self.draw_radius, 1)
            # vector
            vector = pygame.draw.aaline(self.window, self.BLACK, agent.pos.tolist(), agent.next_vector_pos(), 1)
            # vector = pygame.draw.line(self.window, self.BLACK, agent.pos.tolist(), agent.next_vector_pos(), 3)
            l_point, r_point = agent.next_vector_arrow()
            vector_l = pygame.draw.aaline(self.window, self.BLACK, agent.next_pos_vector.tolist(), l_point, 1)
            # vector_l = pygame.draw.line(self.window, self.BLACK, agent.next_pos_vector.tolist(), l_point, 3)
            vector_r = pygame.draw.aaline(self.window, self.BLACK, agent.next_pos_vector.tolist(), r_point, 1)
            # vector_r = pygame.draw.line(self.window, self.BLACK, agent.next_pos_vector.tolist(), r_point, 3)
        self.clock.tick(int(self.fps))  # fps
        pygame.display.flip()
        pygame.display.update()
        self.window.fill(self.WHITE)  # retain

    def step(self):
        # print("updated ...")

        # get info : {neighbors_lst, mean_course}
        self.get_neighbors()

        # pipe correction
        vicsek_mean_vel_update(self.agent_lst)

        for agent in self.agent_lst:
            agent.update_state()        # agents update pos

    def close(self):

        if self.if_render:
            pygame.quit()
            # sys.exit()  # end running

        print("env closed ...")

    def get_neighbors(self):
        """
        get {neighbors_lst, mean_course} info
        """

        for agent in self.agent_lst:

            neighbors_lst = []
            for neighbor in self.agent_lst:
                if agent.id != neighbor.id:  # not self
                    distance = np.linalg.norm(agent.pos - neighbor.pos)
                    if agent.view_range == 0:  # global view
                        neighbors_lst.append(neighbor)
                    elif agent.view_range != 0:  # perceive radius
                        if distance <= agent.view_range:
                            neighbors_lst.append(neighbor)
                        elif distance >= agent.view_range:  # cannot perceive not neighbor
                            pass
                        else:
                            print("unknown error 01 in get_neighbor")
                            sys.exit()
                    else:
                        print("unknown error 02 in get_neighbor")
                        sys.exit()
                        # time.sleep(100)
            agent.neighbor_lst = neighbors_lst

            # mean course
            mean_course = []
            for each in neighbors_lst:
                mean_course.append(each.course)

            if not len(mean_course):  # not neighbor in view
                mean_course = int(agent.course[0] * 180 / np.pi)
                agent.mean_course = agent.course[0]
            elif len(mean_course):  # have neighbor in view
                mean_course = np.sum(np.array(mean_course)) / len(mean_course)  # rad
                agent.mean_course = np.array([mean_course])  # rad



