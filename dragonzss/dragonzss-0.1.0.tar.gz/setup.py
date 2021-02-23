# import pickle
from setuptools import setup
# from app.mushroomer_Qlearning import MushroomerQlearning
# from game import *
# from ml_algorithm import *
#
# # RUN = sys.argv[1]
# # MODEL = sys.argv[2]
# Train = False
#
# if __name__ == "__main__":
#
#     mushroom_app = MushroomerQlearning()
#     env = Env()
#     agent = QLearningBase(actions=list(range(env.n_actions)))
#
#     if Train:
#         q_table = mushroom_app.train(agent)
#         print(q_table)
#         with open('./app/q_table.pkl', "wb") as f:
#             f.write(pickle.dumps(dict(q_table)))
#     else:
#         with open('./app/q_table.pkl', "rb") as f:
#             q_table = pickle.load(f)
#         mushroom_app.run(agent, q_table, model='human')


setup(
    name='dragonzss',
    version='0.1.0',
    packages=['app', 'game', 'game.mushroomer', 'game.mushroomer.object', 'ml_algorithm', 'ml_algorithm.Q_learning'],
    url='',
    license='',
    author='perhaps',
    author_email='17090881116@163.com',
    description='',

)
