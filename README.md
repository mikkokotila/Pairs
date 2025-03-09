# Pairs

<div align="center">
  <!-- Add a project logo or banner image here when available -->
  <h3>Advanced Translation Management System</h3>
  <p>A powerful tool for managing, editing, and reviewing translations with AI assistance</p>
</div>

<p align="center">
  <!-- Add badges here when available -->
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#api">API</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Overview

Pairs is an advanced translation management system designed for translators working with Tibetan texts. It provides a modern, intuitive interface for translation work with powerful AI-assisted features to enhance productivity and quality.

The system combines traditional translation workflows with cutting-edge AI capabilities to assist in research, grammar explanation, and translation suggestions, making it an essential tool for professional translators and scholars.

## Key Features

- **Intuitive Translation Interface**: Clean, distraction-free environment for translation work
- **AI-Assisted Translation**: Get intelligent translation suggestions for complex passages
- **Context-Aware Tools**: Right-click on text to access various research and assistance tools
- **Keyword Research**: Analyze key terms and concepts in the source text
- **Grammar Explanations**: Get detailed explanations of grammatical structures
- **Glossary Integration**: Lookup and maintain consistent terminology
- **Example Finder**: Find similar usage examples for difficult passages
- **Automatic Saving**: Never lose your work with automatic saving
- **Version Control**: Track changes and maintain a history of your translations
- **Review System**: Collaborative review and feedback system
- **Git Integration**: Commit and publish translations directly to GitHub

## Installation

### Prerequisites

- Python 3.8 or higher
- Git
- API key for Claude AI (for AI-assisted features)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/mikkokotila/Pairs.git
   cd Pairs
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following:
   ```
   api_key=your_claude_api_key
   service_account_subject=your_service_account_email
   service_account_file=path_to_service_account_file.json
   ```

5. Run the application:
   ```bash
   python app/run.py
   ```

## Usage

### Basic Translation Workflow

1. Select a file to translate from the dropdown menu
2. Edit translations in the target column
3. Use the context menu (right-click) to access AI assistance tools
4. Changes are automatically saved as you work
5. Use the Commit button to save changes to version control
6. Use the Publish button to finalize translations

### Context Menu Tools

- **Research Keyword**: Analyze key terms and concepts
- **Suggest Translation**: Get AI-powered translation suggestions
- **Lookup Glossary**: Check terminology in the glossary
- **Find Examples**: Find similar usage examples
- **Explain Grammar**: Get grammatical explanations

### Keyboard Shortcuts

- **Enter**: Move to the next row
- **Shift+Enter**: Insert a line break
- **Arrow Up/Down**: Navigate between rows

## Configuration

### File Structure

- `app/`: Main application code
  - `data/`: Translation files
  - `models/`: AI and processing models
  - `routes/`: API routes
  - `static/`: CSS, JavaScript, and images
  - `templates/`: HTML templates
  - `utils/`: Utility functions

### Customization

The system can be customized by modifying:
- `app/static/style.css`: Visual appearance
- `app/models/suggest_translation.py`: AI translation behavior
- `app/templates/index.html`: Interface layout

## API

The system provides several API endpoints:

- `/research-keyword`: Analyze key terms
- `/suggest-translation`: Get translation suggestions
- `/lookup-glossary`: Search the glossary
- `/find-examples`: Find usage examples
- `/explain-grammar`: Get grammar explanations
- `/get-context`: Retrieve context for a row
- `/autosave`: Save changes automatically

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding style and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Lopenling](https://github.com/lopenling) for supporting the development
- [Claude AI](https://www.anthropic.com/claude) for powering the AI assistance features
- All contributors and translators who have helped improve this tool

---

<div align="center">
  <sub>Built with ❤️ for the translation community</sub>
</div>
