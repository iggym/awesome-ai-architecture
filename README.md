
# 🏛️ AWESOME AI ARCHITECTURE

> **A curated, battle-tested blueprint index for enterprise AI systems, multi-agent frameworks, RAG pipelines, and model infrastructure.**

[![Live Architecture Index](https://img.shields.io/badge/Live%20Directory-iggym.github.io%2Fawesome--ai--architecture-purple?style=for-the-badge&logo=github)](https://iggym.github.io/awesome-ai-architecture)
[![GitHub Repository](https://img.shields.io/badge/GitHub-iggym%2Fawesome--ai--architecture-black?style=for-the-badge&logo=github)](https://github.com/iggym/awesome-ai-architecture/tree/main)
[![Awesome List](https://img.shields.io/badge/Awesome-AI%20Architecture-FF69B4?style=for-the-badge&logo=awesome-lists)](https://iggym.github.io/awesome-ai-architecture)

---

## 🗺️ THE MODERN AI SYSTEM BLUEPRINT

<p align="center">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 280" width="100%" height="auto" style="border-radius: 12px; background: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <pattern id="archGrid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="1"/>
    </pattern>
    <linearGradient id="purpleGlow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#a855f7"/>
      <stop offset="50%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#06b6d4"/>
    </linearGradient>
  </defs>

  <rect width="800" height="280" fill="#0b0f19"/>
  <rect width="800" height="280" fill="url(#archGrid)" opacity="0.6"/>

  <!-- Layer 1: Client / App Interfaces -->
  <rect x="30" y="30" width="740" height="40" rx="8" fill="#1e1b4b" stroke="#6366f1" stroke-width="1.5"/>
  <text x="400" y="55" fill="#a5b4fc" font-size="13" font-weight="bold" text-anchor="middle">📱 CLIENT LAYER (Web Apps, APIs, Voice Interfaces, IDE Extensions)</text>

  <!-- Connection line 1-2 -->
  <path d="M 400 70 L 400 90" stroke="#6366f1" stroke-width="2" stroke-dasharray="4,4"/>

  <!-- Layer 2: Guardrails & Router -->
  <rect x="30" y="90" width="740" height="45" rx="8" fill="#311042" stroke="#d946ef" stroke-width="1.5"/>
  <text x="400" y="117" fill="#f0abfc" font-size="13" font-weight="bold" text-anchor="middle">🛡️ GUARDRAILS & ROUTER (PII Sanitization, Prompt Injection Defenses, Cost-Cascades)</text>

  <!-- Split Lines to Orchestration & Context -->
  <path d="M 220 135 L 220 155" stroke="#d946ef" stroke-width="2"/>
  <path d="M 580 135 L 580 155" stroke="#d946ef" stroke-width="2"/>

  <!-- Layer 3A: Agent Orchestration -->
  <rect x="30" y="155" width="360" height="55" rx="8" fill="#0f172a" stroke="#0ea5e9" stroke-width="1.5"/>
  <text x="210" y="178" fill="#38bdf8" font-size="13" font-weight="bold" text-anchor="middle">🤖 AGENT ORCHESTRATION</text>
  <text x="210" y="196" fill="#94a3b8" font-size="11" text-anchor="middle">State Graphs • Tool Loops • Sub-Agents</text>

  <!-- Layer 3B: Context & Retrieval -->
  <rect x="410" y="155" width="360" height="55" rx="8" fill="#0f172a" stroke="#10b981" stroke-width="1.5"/>
  <text x="590" y="178" fill="#34d399" font-size="13" font-weight="bold" text-anchor="middle">💾 CONTEXT & RETRIEVAL (RAG)</text>
  <text x="590" y="196" fill="#94a3b8" font-size="11" text-anchor="middle">Vector DBs • Knowledge Graphs • Memory</text>

  <!-- Connection to Model Serving -->
  <path d="M 210 210 L 210 230" stroke="#0ea5e9" stroke-width="2"/>
  <path d="M 590 210 L 590 230" stroke="#10b981" stroke-width="2"/>

  <!-- Layer 4: Model Engine -->
  <rect x="30" y="230" width="740" height="35" rx="8" fill="#111827" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="400" y="252" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">⚡ INFERENCE & ENGINE LAYER (Frontier Cloud APIs • On-Prem vLLM/Ollama • Local Weights)</text>

  <!-- Top Accent Bar -->
  <rect x="30" y="15" width="740" height="3" rx="1.5" fill="url(#purpleGlow)"/>
</svg>
</p>

---

## 🚀 THE VISION: CUTTING THROUGH THE NOISE

The AI landscape is flooded with thousands of repos, toy frameworks, and wrapper libraries. **Awesome AI Architecture** filters out the hype to deliver a pragmatic, battle-tested directory of real-world infrastructure components and system blueprints.

> 💬 *"Building modern AI applications is no longer about fine-tuning custom models for every task—it's about composing modular, resilient architecture layers that manage context, enforce determinism, and scale predictably."*

Whether you're migrating an enterprise codebase to local open-weights, wiring up multi-agent state machines, or building hybrid search RAG pipelines, this repository maps out **what actually works in production**.

---

## 👥 AUDIENCE: WHO IS THIS FOR?

| Role | Operational Value |
| :--- | :--- |
| 🏗️ **AI System Architects** | Evaluate end-to-end design patterns, state persistence models, and infrastructure stack trade-offs. |
| 🤖 **Lead Machine Learning Engineers** | Compare model serving engines (vLLM, TensorRT-LLM, llama.cpp), vector databases, and evaluation harnesses side-by-side. |
| 🛡️ **Enterprise Security & Platform Leads** | Find battle-hardened prompt firewalls, self-hosted sandboxes, and data-residency compliant tools. |
| 🛠️ **Full-Stack & Systems Engineers** | Discover clean, low-overhead libraries and patterns for integrating non-deterministic models into production web apps. |

---

## 💡 WHY CURATED ARCHITECTURE MATTERS

> 💬 *"The biggest mistake teams make in 2026 is coupling their core application code directly to a single model provider. Robust AI architecture isolates the model behind routing, caching, and evaluation layers so you can swap model providers overnight without breaking downstream systems."* — [Explore the Directory](https://iggym.github.io/awesome-ai-architecture)

### Core Architectural Pillars Indexed:
* 🧠 **Agent & State Orchestration:** Deterministic DAGs, human-in-the-loop controls, and multi-agent consensus protocols.
* ⚡ **Inference & Model Serving:** High-throughput engine benchmarking, quantization, and local deployment tooling.
* 💾 **Vector, Graph & Hybrid Storage:** Dense embeddings, sparse lexical search, knowledge graph integration, and long-term agent memory.
* 🛡️ **Guardrails & Interceptors:** Pre-flight sanitization, real-time response filters, and automated schema repair.
* 📊 **Observability & Tracing:** OpenTelemetry-compatible tracing, cost attribution, and real-time evaluation harnesses.

---

## 📚 ARCHITECTURE CATEGORY HIGHLIGHTS


```

📂 AWESOME-AI-ARCHITECTURE
├── 🤖 Agent Frameworks (State Machines, DAGs, Multi-Agent Loops)
├── 💾 Retrieval & Memory (Vector DBs, Graph RAG, Hybrid Search)
├── ⚡ Inference Engines (vLLM, SGLang, Ollama, TensorRT)
├── 🛡️ Safety & Guardrails (LlamaGuard, NeMo, Outlines, Instructor)
├── 📊 Observability & Evals (Langfuse, Phoenix, Ragas, Braintrust)
└── 🌉 Model Interfaces & Protocols (MCP, Tool Schemas, Function Calling)

```

---

## ⚡ TECH STACK & DESIGN PHILOSOPHY

This index is delivered as an ultra-fast, zero-overhead static web experience:

- 🎨 **Frontend Stack:** Modern Vanilla HTML5, CSS3, and modern ECMAScript (ES6+)
- 🚀 **Zero Dependencies:** No React, Vue, Tailwind, or complex build toolchains


---

## 🛠️ QUICKSTART (LOCAL DEVELOPMENT)

Because there are no npm packages or build systems required, spinning up the site locally takes 5 seconds:

```bash
# 1. Clone the repository
git clone [https://github.com/iggym/awesome-ai-architecture.git](https://github.com/iggym/awesome-ai-architecture.git)

# 2. Enter the repository directory
cd awesome-ai-architecture

# 3. Launch a simple web server
python3 -m http.server 8000

```

Point your web browser to `http://localhost:8000` to explore the interactive architecture directory offline! 🎈

---

## 🤝 CONTRIBUTING TO THE ARCHITECTURE INDEX

Found a production-grade tool, framework, or architectural pattern that belongs in this index?

1. 🍴 **Fork** the repository (`iggym/awesome-ai-architecture`)
2. 🌿 Create your feature branch (`git checkout -b feature/add-new-pattern`)
3. 📥 Submit a **Pull Request** with a brief explanation of why the tool/pattern is battle-tested and valuable for production AI architectures.

---
