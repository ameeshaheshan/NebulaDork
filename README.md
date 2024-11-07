<h1 align="center">
  <br>
  <a href="https://github.com/ameeshaheshan/NebulaDork/"><img src="https://github.com/ameeshaheshan/NebulaDork/blob/main/src/banner.png" alt="NebulaDork"></a>
  <br>
  NebulaDork
  <br>
</h1>


<div align="center">

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-1.3-blue.svg)

**High-speed Google dorking tool with SQL injection detection capabilities**

[Features](#✨-features) • [Installation](#🚀-installation) • [Usage](#💡-usage) • [Examples](#📚-examples) • [Contributing](#🤝-contributing)

</div>
<div align="center">
  <img src="https://github.com/ameeshaheshan/NebulaDork/blob/main/src/1.png" alt="NebulaDork"></a>
  <img src="https://github.com/ameeshaheshan/NebulaDork/blob/main/src/2.png" alt="NebulaDork"></a>
</div>

## 🎯 Overview

NebulaDork is an open-source, high-speed Python tool for Google dorking that filters SQL-vulnerable URLs and web applications. With multi-threading support and advanced filtering capabilities, it streamlines web reconnaissance and vulnerability testing processes.

## ✨ Features

- 🚀 High-speed multi-threaded Google dorking
- 🎯 Domain and file type filtering
- 🛡️ Automated SQL injection vulnerability testing
- 🤖 CAPTCHA solving support
- 📱 Random User-Agent rotation
- 💾 Results export functionality
- 🎨 Customizable output filtering

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/ameeshaheshan/NebulaDork.git

# Navigate to the directory
cd NebulaDork

# Install requirements
pip install -r requirements.txt
```

## 💡 Usage

```bash
usage: main.py [-h] --dork DORK [--pages PAGES] [--filter FILTER] [--file-type FILE_TYPE] 
               [--delay DELAY] [--save] [--verbose] [--captcha-api CAPTCHA_API]
               [--threads {1,2,3,4,5,6,7,8,9,10}] [--show-title] 
               [--output-filter OUTPUT_FILTER] [--random-user-agent RANDOM_USER_AGENT]
               [--sql-injection]
```

### 🔧 Options

```bash
  -h, --help            show this help message and exit
  --dork DORK           Dork query
  --pages PAGES         Number of pages to fetch
  --filter FILTER       Filter by domain (e.g. .gov, .edu)
  --file-type FILE_TYPE Filter by file type (e.g. pdf, doc)
  --delay DELAY         Delay between requests (seconds)
  --save                Save output to file
  --verbose             Verbose mode for debugging
  --captcha-api CAPTCHA_API
                        API key for CAPTCHA solving service (e.g. 2captcha)
  --threads {1,2,3,4,5,6,7,8,9,10}
                       Number of threads for parallel requests (min 1, max 10)
  --show-title         Show titles of the search results along with URLs
  --output-filter OUTPUT_FILTER
                       Output URL filter (e.g., php?*=)
  --random-user-agent RANDOM_USER_AGENT
                       Use random User-Agent headers from a specified file
  --sql-injection      Test for SQL injection vulnerabilities
```

## 📚 Examples

### Basic SQL Injection Vulnerability Scanning

```bash
python3 main.py --dork "view_items.php?id=" --pages 10 --verbose --threads 10 --output-filter "php?" --sql-injection
```

This command will:
- Search for potentially vulnerable PHP pages
- Scan 10 pages of Google results
- Use maximum thread count for speed
- Filter results containing 'php?'
- Test each URL for SQL injection vulnerabilities
- Show detailed progress with verbose mode

### Domain-Specific Search

```bash
python3 main.py --dork "inurl:admin" --filter ".gov" --pages 5 --save
```

### File Type Filtering

```bash
python3 main.py --dork "confidential" --file-type "pdf" --pages 3 --save
```

## ⚠️ Disclaimer

This tool is for educational and ethical testing purposes only. Users are responsible for complying with applicable laws and obtaining necessary permissions before testing any systems they don't own.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ameeshaheshan/NebulaDork&type=Date)](https://star-history.com/#ameeshaheshan/NebulaDork&Date)

---
<div align="center">
Made with ❤️ by Ameesha Heshan
</div>
