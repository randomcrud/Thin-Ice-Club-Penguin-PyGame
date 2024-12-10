from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Wrap the environment for vectorized training
vec_env = make_vec_env(lambda: ThinIceCustom(), n_envs=1)

# Train the agent
model = PPO("MlpPolicy", vec_env, verbose=1)
model.learn(total_timesteps=10000)

# Test the trained agent
env = ThinIceCustom()
obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()

env.close()
