
# Design Document for Chrome Extension to Extract Audio and Separate Stems

---

## 1. Overview
The Chrome extension will allow users to input a YouTube link, which will be used to extract audio (in .wav format) using `youtube-dl`. This audio will then be processed by one of the AI models (Spleeter, Demucs, or Open-Unmix) to separate the audio into different stems (e.g., vocals, drums, bass, etc.), which will be outputted for the user to download.

---

## 2. High-Level Features
- Input field for users to paste YouTube URLs.
- Backend service to process the YouTube link and extract the .wav file.
- Option to choose between different AI models for stem separation.
- Generate and return separate stem files for the user to download.
- Clean and user-friendly UI for interactions.

---

## 3. Components
### 3.1 Frontend (Chrome Extension Interface)
- **UI for YouTube Link Input**: A simple text input field where users can paste the YouTube link.
- **AI Model Selection**: A dropdown or radio button selection for the user to choose between Spleeter, Demucs, and Open-Unmix.
- **Progress Indicator**: Shows the user the progress of the audio extraction and stem separation.
- **Download Links**: Once stems are processed, users should be able to download the separate stems.

### 3.2 Backend (Node.js or Python Service)
- **YouTube Audio Extraction**: Use `youtube-dl` or its Python counterpart `yt-dlp` to download the audio from a YouTube link.
- **Audio Processing with AI Models**: Pass the downloaded audio file to the selected AI model for stem separation.
- **File Storage and Serving**: Store the separated stems on a server or provide them for direct download by the user.

---

## 4. System Architecture

### 4.1 Chrome Extension (Frontend)
- The Chrome extension's UI will be built using HTML, CSS, and JavaScript. The extension will allow users to enter YouTube URLs and select an AI model.
- A background script will communicate with the backend server to send the YouTube URL and selected model.

### 4.2 Backend (Server-side)
- The backend service can be built using either Python (Flask, FastAPI) or Node.js (Express). This service will:
  1. Receive the YouTube link from the extension.
  2. Extract the audio using `youtube-dl` or `yt-dlp`.
  3. Process the extracted audio using the selected AI model for stem separation.
  4. Store the resulting stems on a temporary server or cloud storage.
  5. Return download links for the stems to the extension.

### 4.3 File Management
- Store files temporarily on the server during processing.
- Once the processing is complete, return a download link to the user for each stem (drums, bass, vocals, etc.).
- Implement an automatic cleanup system to delete files after a certain period.

---

## 5. Technical Steps for Code Base

### Step 1: Chrome Extension Setup
- **Manifest File**: Create `manifest.json` to define the permissions and resources your Chrome extension will need (e.g., permissions for activeTab, storage, and access to external APIs).
  ```json
  {
    "manifest_version": 3,
    "name": "YouTube Stem Separator",
    "version": "1.0",
    "permissions": ["activeTab", "storage"],
    "background": {
      "service_worker": "background.js"
    },
    "action": {
      "default_popup": "popup.html"
    },
    "icons": {
      "48": "icon.png"
    }
  }
  ```
- **Popup HTML**: Create a simple HTML file (`popup.html`) that includes:
  - An input for YouTube URL.
  - A dropdown for AI model selection.
  - A button to start the process.
- **Popup JavaScript**: This will handle sending the data (YouTube link and model choice) to the backend server using a REST API.

### Step 2: Backend Setup
- **Server Creation**:
  - **Python**: Use Flask or FastAPI to create an API that handles incoming requests from the extension.
  - **Node.js**: Use Express to create the same API functionality.

- **REST API Endpoints**:
  - `POST /extract`: Accepts the YouTube URL and AI model selection, extracts audio using `youtube-dl` or `yt-dlp`, processes it, and returns a download link for the stems.
  - **Example Request**:
    ```json
    {
      "youtube_url": "https://www.youtube.com/watch?v=example",
      "model": "spleeter"
    }
    ```

- **YouTube Audio Extraction**: 
  - Use `youtube-dl` or `yt-dlp` to download the audio from the provided YouTube URL.
    ```bash
    youtube-dl -x --audio-format wav <YouTube URL>
    ```
  - Convert the file into `.wav` format for processing.

### Step 3: Integrate AI Model
- **Load and Run AI Model**: Once the `.wav` file is downloaded, pass it to one of the AI models.
  - Example using Spleeter:
    ```python
    from spleeter.separator import Separator
    separator = Separator('spleeter:4stems')
    separator.separate_to_file('input_audio.wav', 'output_directory/')
    ```

- **Return Stems**: Once the stems are processed, store them in a temporary directory and return the download links to the Chrome extension frontend.

### Step 4: File Management and Cleanup
- Implement a file storage solution, such as a local storage directory or cloud storage (AWS S3, Google Cloud Storage), to store the extracted stems.
- Ensure proper cleanup of temporary files after stems have been processed and delivered (e.g., files older than 24 hours are deleted).

### Step 5: Handling User Interaction
- **Progress Feedback**: Use WebSockets or long-polling to provide real-time updates to the user about the progress of the extraction and processing steps.
- **Error Handling**: Provide clear error messages if the audio extraction or stem separation fails, such as invalid URLs or failed downloads.

---

## 6. Example Workflow

1. **User Input**: User opens the Chrome extension, pastes a YouTube link, and selects a stem separation model.
2. **Data Submission**: The extension sends the link and model choice to the backend API.
3. **Audio Extraction**: The backend extracts the audio from the YouTube video using `youtube-dl`.
4. **Stem Separation**: The extracted audio is passed to the selected AI model (Spleeter, Demucs, Open-Unmix) for stem separation.
5. **Output**: The backend stores the separated stems and returns the download links to the Chrome extension.
6. **Download**: The user downloads the separated stems via links presented in the extension.

---

## 7. Technology Stack
- **Frontend**: HTML, CSS, JavaScript (Chrome Extension APIs)
- **Backend**: Python (Flask, FastAPI) or Node.js (Express)
- **YouTube Download**: `youtube-dl` or `yt-dlp`
- **AI Models**: Spleeter, Demucs, Open-Unmix
- **File Storage**: Local storage or cloud (AWS S3, Google Cloud)
- **File Formats**: `.wav` for audio processing and output stems.

---

## 8. Future Enhancements
- **Support for multiple file formats**: Allow users to download stems in formats other than `.wav` (e.g., `.mp3` or `.flac`).
- **Batch processing**: Allow multiple YouTube URLs to be processed in parallel.
- **Account and History Management**: Allow users to create accounts and view/download their previously processed stems.
