
# Hindi Government AI Assistant

A local Hindi/Hinglish AI assistant designed to help
citizens understand government schemes and common
citizen services.

## Main Features

- Hindi/Hinglish conversation
- Local Ollama LLM
- Persistent citizen profile
- Central Government scheme information
- State Government scheme information
- Eligibility matching
- Scheme benefit explanation
- Required document information
- Application process
- Aadhaar and citizen-service FAQs
- Local SQLite database
- Future Hindi STT
- Future Hindi TTS
- Future telephone-call integration

## Architecture

Caller
    |
    v
Speech-to-Text
    |
    v
Conversation Manager
    |
    +--> Citizen Profile
    |
    +--> Scheme Matcher
    |
    +--> Citizen Knowledge Base
    |
    +--> Ollama
    |
    v
Text-to-Speech
    |
    v
Caller

## Local AI

The project uses Ollama.

Default model:

llama3.2:3b

Ollama must be running locally.

## Installation

Create virtual environment:

python -m venv .venv

Activate:

Windows PowerShell:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Start Ollama

ollama list

ollama run llama3.2:3b

## Run Application

python run.py

## Database

SQLite is used for:

- citizen profiles
- conversation history
- persistent memories

## Government Scheme Data

Scheme data must be obtained from trusted
official government sources.

Each scheme should contain:

- scheme name
- government level
- state
- department
- description
- benefits
- eligibility criteria
- required documents
- application procedure
- application URL
- official source URL
- verification date

The LLM must not invent eligibility rules.

## Privacy

Do not store:

- Aadhaar number unless absolutely required
- OTP
- PIN
- passwords
- CVV
- banking credentials

Citizen profile information should only be stored
for the intended assistance and personalization.

## Future Development

1. Hindi STT
2. Hindi neural TTS
3. Better profile extraction
4. Official scheme data synchronization
5. More citizen-service knowledge
6. Phone-number-based profile lookup
7. Telephony integration
8. Call interruption handling
9. Production security
10. Admin dashboard

