# Pairs

<div align="center">
  <a href="https://github.com/lopenling">
    <img src="https://raw.githubusercontent.com/lopenling/Home/main/assets/Lopenling-Logo-Icon.png" alt="Lopenling" width="100">
  </a>
  <h3>Advanced Translation Management System for Tibetan Wisdom Texts</h3>
  <p>A powerful tool for managing, editing, and reviewing translations of Tibetan Buddhist texts with AI assistance</p>
</div>

<p align="center">
  <!-- Add badges here when available -->
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#api">API</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Overview

Pairs is an advanced translation management system specifically designed for translators working with Tibetan Buddhist wisdom texts. It provides a modern, intuitive interface for translation work with powerful AI-assisted features to enhance productivity and quality.

The system addresses the unique challenges of translating Tibetan texts, including complex terminology, specialized grammar, and philosophical concepts. It combines traditional translation workflows with cutting-edge AI capabilities to assist in research, grammar explanation, and translation suggestions, making it an essential tool for professional translators and scholars in the field of Tibetan Buddhism.

## Key Features

- **Intuitive Translation Interface**: Clean, distraction-free environment optimized for Tibetan text translation
- **AI-Assisted Translation**: Get intelligent translation suggestions for complex passages and Buddhist terminology
- **Context-Aware Tools**: Right-click on text to access various research and assistance tools
- **Reader View**: View translations in a clean, reader-friendly format optimized for reading
- **Keyword Research**: Analyze key terms and concepts in Tibetan Buddhist texts
- **Grammar Explanations**: Get detailed explanations of Tibetan grammatical structures
- **Glossary Integration**: Lookup and maintain consistent terminology across translations
- **Example Finder**: Find similar usage examples for difficult passages from other texts
- **Automatic Saving**: Never lose your work with automatic saving
- **Version Control**: Track changes and maintain a history of your translations
- **Review System**: Collaborative review and feedback system
- **Git Integration**: Commit and publish translations directly to GitHub

## Installation

### Prerequisites

- Python 3.8 or higher
- Git
- API key for Claude AI (for AI-assisted features)
- Google Cloud service account (for publishing features)

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

5. Create a Google Cloud service account file:
   - Follow the [official Google Cloud documentation](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating) to create a service account key
   - Download the JSON key file and save it in your project directory
   - Update the `service_account_file` path in your `.env` file

6. Run the application:
   ```bash
   python app/run.py
   ```

## Usage

### Basic Translation Workflow

1. Select a Tibetan text file to translate from the dropdown menu
2. Edit translations in the target column
3. Use the context menu (right-click) to access AI assistance tools
4. Use the Read button to view the text in a reader-friendly format
5. Changes are automatically saved as you work
6. Use the Commit button to save changes to version control
7. Use the Publish button to finalize translations

### Context Menu Tools

- **Research Keyword**: Analyze key terms and concepts in Tibetan Buddhist terminology
- **Suggest Translation**: Get AI-powered translation suggestions for difficult passages
- **Lookup Glossary**: Check terminology in the glossary of Buddhist terms
- **Find Examples**: Find similar usage examples in other translated texts
- **Explain Grammar**: Get grammatical explanations for complex Tibetan constructions

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

- `/research-keyword`: Analyze key terms in Tibetan texts
- `/suggest-translation`: Get translation suggestions
- `/lookup-glossary`: Search the glossary of Buddhist terms
- `/find-examples`: Find usage examples in other texts
- `/explain-grammar`: Get grammar explanations for Tibetan constructions
- `/get-context`: Retrieve context for a row
- `/autosave`: Save changes automatically

## Documentation

Comprehensive documentation for Pairs is available in the `/docs` directory. The documentation is organized into the following sections:

- **Getting Started**: Installation, first-time setup, and interface overview
- **Core Functionality**: File management, navigation, and translation workflow
- **Translation Interface**: Layout, editing features, and keyboard shortcuts
- **Context Menu Tools**: Research keyword, suggest translation, lookup glossary, etc.
- **Reader View**: Clean presentation of translations
- **Advanced Features**: Autosave, search functionality, and integrations
- **Workflow Guides**: Adding texts, translating, reviewing, and publishing
- **Troubleshooting**: Solutions for common issues
- **Glossary**: Definitions of key terms and concepts

To view the documentation:
1. Navigate to the `/docs` directory
2. Open `index.md` to start browsing the documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding style and includes appropriate tests.

## Contributors

Special thanks to all the contributors who have helped make Pairs possible:

- [@mikkokotila](https://github.com/mikkokotila) - Project Lead
- [@mcsneaky](https://github.com/mcsneaky) - Developer
- [@sidrun](https://github.com/sidrun) - Developer
- [@ngawangtrinley](https://github.com/ngawangtrinley) - Tibetan Language Expert

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Lopenling](https://github.com/lopenling) for supporting the development
- [Claude AI](https://www.anthropic.com/claude) for powering the AI assistance features
- All contributors and translators who have helped improve this tool

---

<div align="center">
  <sub>Built with ❤️ for the Tibetan translation community</sub>
</div>
