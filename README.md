# KeplerLLM Chrome Extension

<p align="center">
  <img src="src/media/kepler-llm.png" alt="KeplerLLM Chrome Extension logo" width="200">
</p>

<p align="center">
  Seamlessly integrate KeplerLLM into Google Chrome.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#development">Development</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## Features

- 🔗 Connect to your KeplerLLM instance with a simple connection string or automatic browser extension registration
- 📑 Save selected text to KeplerLLM directly from any webpage
- 📄 Upload entire web pages to KeplerLLM for processing
- 🗂️ Embed content into specific workspaces
- 🔄 Automatic logo synchronization with your KeplerLLM instance

## Installation

_The button below is the **upstream** AnythingLLM extension published by Mintplex Labs — shown for reference. This fork is not published on the Chrome Web Store; to use KeplerLLM's build, install from source or a release from this repo._

<a href="https://chromewebstore.google.com/detail/anythingllm-browser-compa/pncmdlebcopjodenlllcomedphdmeogm">
  <img src="https://storage.googleapis.com/web-dev-uploads/image/WlD8wC6g8khYWPJUsQceQkhXSlv1/iNEddTyWiMfLSwFD6qGq.png" alt="Chrome Extension" width="200">
</a>

_or_

1. Clone this repository or download the latest release.
2. Open Chrome and navigate to `chrome://extensions`.
3. Enable "Developer mode" in the top right corner.
4. Click "Load unpacked" and select the `dist` folder from this project.

## Development

To set up the project for development:

1. Install dependencies:

   ```
   yarn install
   ```

2. Run the development server:

   ```
   yarn dev
   ```

3. To build the extension:
   ```
   yarn build
   ```

The built extension will be in the `dist` folder.

## Usage

1. Click on the KeplerLLM extension icon in your Chrome toolbar.
2. Enter your KeplerLLM browser extension API key to connect to your instance (or create the API key inside KeplerLLM and have it automatically register to the extension).
3. Right-click on selected text or anywhere on a webpage to see KeplerLLM options.
4. Choose to save selected text or the entire page to KeplerLLM.

## Contributing

Contributions are welcome! Feel free to submit a PR.

## Acknowledgements

- This extension is designed to work with [KeplerLLM](https://github.com/fernando-reis-guimaraes/KeplerLLM).
- Forked from the upstream [Mintplex-Labs AnythingLLM browser extension](https://github.com/Mintplex-Labs/anythingllm-extension) — thank you to Mintplex Labs and all upstream contributors.

---

Copyright © 2024 [Mintplex Labs](https://github.com/Mintplex-Labs). <br />
This project is [MIT](LICENSE) licensed.
