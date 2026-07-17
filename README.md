```text
 ▄█     █▄   ▄█     ▄████████    ▄████████    ▄█    █▄       ▄████████     ███    
███     ███ ███    ███    ███   ███    ███   ███    ███     ███    ███ ▀█████████▄
███     ███ ███▌   ███    █▀    ███    █▀    ███    ███     ███    ███    ▀███▀▀██
███     ███ ███▌   ███         ▄███▄▄▄      ▄███▄▄▄▄███▄▄   ███    ███     ███   ▀
███     ███ ███▌ ▀███████████ ▀▀███▀▀▀     ▀▀███▀▀▀▀███▀  ▀███████████     ███    
███     ███ ███           ███   ███    █▄    ███    ███     ███    ███     ███    
███ ▄█▄ ███ ███     ▄█    ███   ███    ███   ███    ███     ███    ███     ███    
 ▀███▀███▀  █▀    ▄████████▀    ██████████   ███    █▀      ███    █▀     ▄████▀  
```
**Wisehat Helps Whitehats Hunt Wisely - AI-powered intelligence for bug bounty hunters.**

---

WiseHat is an AI-powered intelligence tool that analyzes Blockchain Bug Bounty Programs (BBPs) and produces a structured, researcher-friendly report **before** you spend time hunting. Instead of reading pages of documentation, whitehats get an instant breakdown of the rules, risks, rewards, scope, and requirements that materially affect whether a valid vulnerability will actually be accepted, classified correctly, and rewarded.

WiseHat does **not** summarize documentation. It analyzes bug bounty documentation from the perspective of an experienced security triager and expert bug bounty rules analyzer — identifying the rules, wording, exclusions, classifications, and requirements that determine whether a researcher can:

- Hunt safely
- Submit valid reports
- Receive fair rewards
- Avoid unnecessary disputes
- Understand program expectations

---

## Supported Platforms

| Platform | How data is fetched |
|---|---|
| **Immunefi** | Scrapes the program's `information`, `scope`, and `resources` pages via LangChain's `WebBaseLoader`. Program slugs are resolved case-insensitively against Immunefi's canonical program list. |
| **Hackenproof** | Fetches program data through the Hackenproof MCP (JSON-RPC) API. |

---

## Report Sections

Every WiseHat report contains the following sections, generated strictly from the provided documentation:

- **Program Overview** — what the project protects, assets covered, notable characteristics (no marketing language).
- **WiseHat Recommendation and Rating** — an overall `1–10` score representing how researcher-friendly the program is, with a verdict and short explanation.
  - `9.0–10.0` → Excellent — Highly Recommended
  - `8.0–8.9` → Very Good — Recommended
  - `7.0–7.9` → Good — Hunt with Awareness
  - `5.0–6.9` → Proceed with Caution
  - `< 5.0` → High Risk for Researchers
- **Mandatory Requirements** — every requirement that could invalidate an otherwise valid report (PoC, KYC, responsible disclosure, testing restrictions, etc.).
- **Green Flags** — characteristics that benefit researchers (clear documentation, Primacy of Impact, deterministic rewards, etc.).
- **Red Flags** — characteristics that increase researcher uncertainty or risk ("up to", "sole discretion", undefined severities, vague exclusions, etc.).
- **Scope & Impact Analysis** — in-scope/out-of-scope assets, reward ranges, severity classification, and known-issue exclusions.
- **Other Things to Consider** — additional observations worth knowing before hunting.
- **Hunter Tips** — practical advice derived only from the documentation.
- **Before You Hunt Checklist** — a concise, documentation-backed checklist to run through before starting.

---

## Project Structure

```
Wisehat/
├── app.py                      # Core: LLM chain, WiseHatReport schema, generate_report()
├── frontend/
│   └── streamlit_app.py        # Streamlit web UI
├── programs/
│   ├── immunefi_loader.py      # Immunefi page loader + case-insensitive slug resolver
│   └── hackenproof_mcp.py      # Hackenproof MCP (JSON-RPC) client
├── prompts/
│   └── system_prompt.md        # WiseHat AI system prompt (analysis framework + rules)
├── .env.example                # Required environment variables
└── requirements.txt            # Python dependencies
```

---

## Setup

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd Wisehat
uv pip install -r requirements.txt   # or: pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Required for | Description |
|---|---|---|
| `OPENCODE_GO_API_KEY` | All reports | API key for the OpenCode GO LLM endpoint (GLM-5.2). |
| `HACKENPROOF_API_KEY` | Hackenproof only | API key for the Hackenproof MCP. |

---

## Usage

### Web UI (Streamlit)

```bash
streamlit run frontend/streamlit_app.py
```

Then open http://localhost:8501, pick a platform, enter the program name (any casing works), and click **Generate Intelligence Report**.

> Note: Streamlit hot-reloads `streamlit_app.py` on save, but changes to `app.py` or files under `programs/` require a server restart to take effect (Python caches imported modules).

### CLI

```bash
python app.py
```

Prompts for platform and program name, then prints the structured report as JSON.

---

## How It Works

```
User input (platform + program name)
        │
        ▼
┌────────────────────────┐
│  Platform data loader  │
│  (Immunefi / Hackenproof)│
└────────────────────────┘
        │ program_data
        ▼
┌────────────────────────┐
│  ChatPromptTemplate    │  ← system_prompt.md (WiseHat analysis framework)
│  + WiseHatReport schema│  ← pydantic structured output
└────────────────────────┘
        │ structured_llm.invoke()
        ▼
┌────────────────────────┐
│   WiseHatReport (JSON) │
└────────────────────────┘
```

1. The selected platform loader fetches the program's raw documentation.
2. The documentation is injected into a chat prompt built from `prompts/system_prompt.md`.
3. The LLM (`glm-5.2` via OpenCode GO) produces a `WiseHatReport` using LangChain's structured output, guaranteed to match the pydantic schema.
4. The report is rendered in the Streamlit UI (or printed as JSON in CLI mode).

---

## Core Principles

WiseHat follows a strict analyst mindset, enforced by the system prompt:

- **Accuracy over completeness** — never invent rules, exclusions, requirements, or severity mappings.
- **No speculation** — if something is missing, unclear, or ambiguous, it is explicitly called out.
- **Documented facts vs. WiseHat observations** — these are always distinguished, never blurred.
- **No bad-faith accusations** — only practical consequences of wording are explained.
- **Date agnosticism** — dates are reported as documented facts, never interpreted relative to "today" to infer whether a program is active/paused/expired.

---

## Tech Stack

- **LangChain** — prompt templates + structured output
- **OpenCode GO (GLM-5.2)** — LLM via OpenAI-compatible API
- **Pydantic** — `WiseHatReport` structured schema
- **Streamlit** — web frontend
- **requests / WebBaseLoader** — program data fetching

---

## License

See [LICENSE](LICENSE).
