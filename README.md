# Best 403 Unlocker (Python Version)

## Key Differences and Features of the Python Version

The Python version of the 403 unlocker tool, available in [here](https://github.com/403unlocker/best403unlocker-py), has several key features:

### Python-based Implementation

Built using Python's robust networking libraries and tools, providing excellent DNS handling capabilities and cross-platform support.

### Cross-platform Support

Thanks to Python's portability, this project supports:

- **Windows** (manual DNS configuration required)
- **Linux** (automatic configuration)
- **macOS** (automatic configuration)

### Features

- Automated DNS speed testing
- Progress bar visualization
- Config file support
- Both CLI and interactive modes

## How to Run the Python Version

### Method 1 - Using pip (recommended)

```bash
pip install best403unlocker_py
```

### Method 2 - Using poetry (**NOT** recommended)

### Prerequisites

- Python 3.8 or higher
- Poetry package manager
- Administrative/root privileges (required for DNS configuration)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/403unlocker/best403unlocker-py.git
cd best403unlocker-py
```

2. Install dependencies using Poetry:

```bash
poetry install
```

## Usage

### Default Interactive Mode

This will:

- Test all configured DNS servers
- Display a progress bar during testing
- Show results in a table format
- Prompt to apply the fastest DNS server

Command Line Options

1. Test DNS servers with applying:

    ```bash
    unlock403 [--url URL]
    ```

2. Test DNS servers without applying:

    ```bash
    unlock403 search-dns [--url URL]
    ```

3. Set custom DNS servers:

   ```bash
   unlock403 set-custom-dns 8.8.8.8 8.8.4.4
   ```

Examples
Find fastest DNS for a specific domain:

1. Default mode searche and set:

```bash
unlock403
```

2. Default mode searche and set with specific URL:

```bash
unlock403 --url developers.google.com
```

3. search with default url for dns:

```bash
unlock403 search-dns
```

4. search with custom url url for dns

```bash
unlock403 search-dns --url developers.google.com
```

## Contact

Feel free to open issues and PRs on GitHub.

[@msnp1381](https://github.com/msnp1381)
OR
[Email Me](mailto:mohamadnematpoor@gmail.com)
