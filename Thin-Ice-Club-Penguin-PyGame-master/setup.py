from setuptools import setup, find_packages

setup(
    name="thin_ice",
    version="0.1.0",
    description="Thin Ice Game with Reinforcement Learning Environment",
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
        "gym>=0.21.0",
        "numpy>=1.18.0",
        "stable-baselines3>=1.6.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
