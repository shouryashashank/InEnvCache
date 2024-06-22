# InEnvCache
InEnvCache is a Python library designed to facilitate caching across pods within an environment, leveraging the Kubernetes API for distributed cache management. This framework allows for efficient and secure storage and retrieval of cached objects, making it ideal for applications running in Kubernetes clusters.

## Features

- **Encryption Support**: Secure your cached data with optional encryption.
- **Kubernetes Integration**: Seamlessly integrates with Kubernetes for distributed caching across pods.
- **Environment Variable Fallback**: Uses environment variables for caching if Kubernetes API is not accessible.
- **Thread-Safe Operations**: Ensures thread safety with lock mechanisms for concurrent operations.

### Quick Start

To get started with InEnvCache, follow these simple steps:

1. **Installation**: First, install the library using pip:

    ```bash
    pip install inenvcache
    ```

2. **Initialization**: Import and initialize InEnvCache in your Python application:

    ```python
    from in_env_cache import InEnvCache

    # Create an instance of InEnvCache with optional encryption key
    cache = InEnvCache(key="my-secret-key")
    ```

3. **Set a Cache Value**: Store a value in the cache with an optional time-to-live (TTL):

    ```python
    cache.set("key1", "value1", ttl=600)
    ```

4. **Get a Cache Value**: Retrieve a value from the cache:

    ```python
    value = cache.get("key1")
    print(value)  # Output: value1
    ```

5. **Delete a Cache Value**: Remove a value from the cache:

    ```python
    cache.delete("key1")
    ```

6. **Flush the Cache**: Clear all values from the cache:

    ```python
    cache.flush_all()
    ```

With these steps, you can easily integrate InEnvCache into your Kubernetes-based applications for efficient caching solutions.
## License

This project is licensed under multiple licenses:

- For **free users**, the project is licensed under the terms of the GNU Affero General Public License (AGPL). See  [`LICENSE-AGPL`](LICENSE-AGPL) for more details.

- For **paid users**, there are two options:
    - A perpetual commercial license. See [`LICENSE-COMMERCIAL-PERPETUAL`](LICENSE-COMMERCIAL-PERPETUAL) for more details.
    - A yearly commercial license. See [`LICENSE-COMMERCIAL-YEARLY`](LICENSE-COMMERCIAL-YEARLY) for more details.

Please ensure you understand and comply with the license that applies to you.
