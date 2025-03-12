# First-Time Setup

After installing Pairs, you'll need to perform some initial setup to get the application ready for use. This guide will walk you through the necessary steps to configure Pairs for your translation work.

## Initial Configuration

When you first launch Pairs, you'll need to configure a few settings to ensure the application works correctly for your needs.

### Starting the Application

1. Open a terminal or command prompt
2. Navigate to the Pairs directory
3. Run the application:

```bash
python app/app-server.py
```

4. Open a web browser and navigate to `http://localhost:5000`

### Setting Up Your Workspace

Pairs works with translation files stored in your local filesystem. You'll need to set up a workspace directory where your translation files will be stored.

1. Create a directory on your system where you want to store your translation files
2. When you first open Pairs, you'll be prompted to select this directory
3. Click the "Browse" button and navigate to your workspace directory
4. Click "Select" to confirm your choice

Your workspace directory will now be the default location for all translation files created or managed by Pairs.

## Configuration Options

Pairs offers several configuration options that you can adjust according to your preferences.

### Language Settings

You can configure the default source and target languages for your translations:

1. Click on the settings icon in the top-right corner of the interface
2. In the "Languages" section, select your preferred source language (typically Tibetan)
3. Select your preferred target language (e.g., English)
4. Click "Save" to apply your changes

### AI Integration Settings

Pairs uses AI to assist with translations. You can configure these settings:

1. Click on the settings icon
2. In the "AI Integration" section, you can:
   - Enable or disable AI-assisted translation
   - Adjust the confidence threshold for suggestions
   - Configure API keys if you're using custom AI services
3. Click "Save" to apply your changes

### Interface Preferences

You can customize the Pairs interface to suit your workflow:

1. Click on the settings icon
2. In the "Interface" section, you can:
   - Adjust the font size for better readability
   - Toggle dark/light mode
   - Configure keyboard shortcuts
   - Set the default view mode (edit, review, or read)
3. Click "Save" to apply your changes

## Creating Your First Translation Project

Once you've configured Pairs, you can create your first translation project:

1. Click the "New" button in the main interface
2. Enter a name for your translation project
3. Select the source file or enter the source text
4. Click "Create" to start your new translation project

For more detailed information on creating and managing translation projects, see the [Adding New Texts](../workflow-guides/adding-texts.md) guide.

## Next Steps

Now that you've completed the first-time setup, you can:

- Explore the [Interface Overview](interface-overview.md) to familiarize yourself with Pairs
- Learn about the [Translation Workflow](../core-functionality/translation-workflow.md)
- Start [Translating Texts](../workflow-guides/translating.md) with Pairs 