# Ulauncher IDE Opener Extension

A Ulauncher extension that helps you quickly open your projects in your favorite code editors. It searches through specified directories for Git repositories and allows you to open them in various editors like VSCode, Sublime Text, Vim, and more.

## Features

- 🎯 Support for multiple code editors
- 🔄 Default editor configuration
- 🚀 Fast project navigation

## Supported Editors

- VSCode (`code`)
- Sublime Text (`subl`)
- Atom (`atom`)
- Vim (`vim`)
- Neovim (`nvim`)
- Emacs (`emacs`)
- Kate (`kate`)
- Cursor (`cursor`)
- Windsurf (`windsurf`)

## Installation

1. Open Ulauncher preferences
2. Go to the "Extensions" tab
3. Click "Add extension"
4. Paste the following URL:
   ```
   https://github.com/nazifkivrik/ulauncher-ide-opener
   ```

## Configuration

The extension has two main preferences that can be configured:

1. **Default Editor**: The editor to use when no specific editor is specified in the query
   - Default: `code` (VSCode)

2. **Search Paths**: Comma-separated list of directories to search for Git repositories
   - Example: `~/Projects,~/Work,~/Documents/GitHub`
   - Supports `~` for home directory

## Usage

1. Open Ulauncher
2. Type your extension keyword (default: `code`)
3. Start typing to search for your project

### Basic Usage
```
` projectname
```
This will open the project in your default editor

### Specify Editor
```
` editor:projectname
```
Example:
```
` code:myproject    # Opens in VSCode
` vim:myproject     # Opens in Vim
` subl:myproject    # Opens in Sublime
```
