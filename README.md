# Notes

A markdown TODO ingester.

This project ingests a folder of markdown files and parses all TODOs (e.g. `- [ ] Say hi to Allen` or `- [x] Buy a coffee`). The ingested TODOs are then saved to a single output markdown file.

## Usage

**Generate `TODO.md` file:**
```bash
make
```

**Watch markdown files:**
```bash
make watch
```

**Run tests:**
```bash
make test
```
