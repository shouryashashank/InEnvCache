# Build Guide

To get started with compiling InEnvCache locally, follow these steps:

1. Clone the InEnvCache repository:
    ```bash
    git clone https://github.com/shouryashashank/InEnvCach.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install wheel:
    ```bash
    pip install wheel
    ```

4. Build the project:
    ```bash
    python setup.py bdist_wheel sdist
    ```

5. Install InEnvCache:
    ```bash
    pip install .
    ```

6. Import InEnvCache and use it in your code:
    ```python
    from InEnvCache import InEnvCache
    InEnvCache.rollout()
    ```