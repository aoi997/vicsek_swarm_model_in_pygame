import numpy as np


def vicsek_mean_vel_update(swarm_lst):
    """velocity average"""
    """vicsek model"""
    print("Using Vicsek Model ...")

    for agent in swarm_lst:
        print("vicsek agent {} "
              "course {} "
              "mean_course {}".format(agent.id,
                                      agent.course,
                                      agent.mean_course))


        if abs(agent.course-agent.mean_course) <= agent.max_step_rad:   # 2 course closed
            agent.course = agent.mean_course

        elif abs(agent.course-agent.mean_course) > agent.max_step_rad:
            if agent.course > agent.mean_course:
                if agent.course-agent.mean_course > np.pi:      # clockwise
                    agent.course += agent.max_step_rad
                elif agent.course-agent.mean_course <= np.pi:   # anti-clockwise
                    agent.course -= agent.max_step_rad
            elif agent.course < agent.mean_course:
                # agent.course += agent.max_step_rad
                if agent.mean_course-agent.course > np.pi:      # anti-clockwise
                    agent.course -= agent.max_step_rad
                elif agent.mean_course-agent.course <= np.pi:   # clockwise
                    agent.course += agent.max_step_rad
