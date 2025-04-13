# 🎥 MyTubeFeed

**Generate a beautiful HTML page with the latest videos from multiple YouTube channels using their RSS feeds.**

---

## 📦 Installation

You can install this CLI tool globally using [`pipx`](https://pypa.github.io/pipx/):

### 1. Install pipx (if not already installed)

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Restart your terminal if necessary.

### 2. Install from GitHub

```bash
pipx install git+https://github.com/mikaelmoutakis/mytubefeed.git
```

---

## 🚀 Usage

```bash
latest_videos path/to/my_list.txt path/to/my/page.html
```

- `my_list.txt` should contain one YouTube channel URL per line, e.g.:

```
https://www.youtube.com/user/darbinorvar
```

- The output HTML file will display embedded videos from all channels sorted by publish date.

---

## ♻️ Updating

If you've made updates to your GitHub repository and want the latest version:

```bash
pipx reinstall git+https://github.com/mikaelmoutakis/mytubefeed.git
```

---

## 💡 Features

- Handles multiple channels
- Videos sorted by latest first
- Clean, light blue design with embedded players
- Validates and handles malformed URLs

---

## 🧪 Running Tests

Clone the repository and run:

```bash
poetry install
poetry run pytest
```

