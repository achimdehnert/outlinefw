# ADR-001: Dynamic Prompt Architecture — Context-driven Outline Generation

**Status:** Accepted  
**Datum:** 2026-04-02  
**Version:** outlinefw v0.3.1+  

## Kontext

Die initiale Implementierung (v0.1–v0.2) hatte hardcodierte System- und User-Prompts,
die ausschliesslich fuer Fiction-Frameworks (Protagonist, Setting, Drama-Beats) ausgelegt waren.

Dies fuehrte zu:
- Falschen Outlines fuer wissenschaftliche Aufsaetze (Protagonist-orientierter Prompt fuer Wissenschaft)
- Fehlenden nicht-fiktionalen Frameworks in der Registry
- Keiner Moeglichkeit, framework-spezifische LLM-Anweisungen einzubetten
- Inkonsistenter Nutzung des `ProjectContext` (nicht alle Felder wurden genutzt)

## Entscheidung

### 1. Einheitlicher System-Prompt

Ein einziger, content-type-agnostischer System-Prompt ersetzt die separaten
Fiction/Non-Fiction Prompts. Der System-Prompt definiert nur das **Ausgabeformat** (JSON-Schema),
nicht den Stil oder die Domäne.

```python
_SYSTEM_PROMPT = """
Du bist ein professioneller Outline-Assistent fuer alle Textformate...
Antworte AUSSCHLIESSLICH mit einem JSON-Array.
"""
```

**Begründung:** Das Ausgabeformat (JSON-Schema mit beat_name, position, act, title, summary...)
ist fuer alle Texttypen identisch. Die Domäne wird durch den User-Prompt gesteuert.

### 2. Vollständige Kontextnutzung im User-Prompt

Alle nicht-leeren Felder von `ProjectContext` werden in den User-Prompt injiziert:

| Fiction | Non-Fiction |
|---------|-------------|
| protagonist, setting | research_question, methodology |
| logline | Kernaussage/These |
| themes, tone, additional_notes | themes, tone, additional_notes |

`additional_notes` ist das universelle Feld für Kontext, der nicht in die Standard-Felder passt
(z.B. Autorenstil, Zielgruppe, spezifische Anforderungen des Auftraggebers).

### 3. `llm_instructions` in FrameworkDefinition

Jede `FrameworkDefinition` kann optionale `llm_instructions` enthalten — framework-spezifische
Anweisungen, die an den LLM-User-Prompt angehängt werden:

```python
SCIENTIFIC_ESSAY = FrameworkDefinition(
    key="scientific_essay",
    ...
    content_mode="nonfiction",
    llm_instructions=(
        "Keine Romandramaturgie. Jeder Abschnitt muss eine klar definierte "
        "wissenschaftliche Funktion haben..."
    ),
)
```

**Begründung:** Framework-Autoren kennen die Qualitätskriterien ihres Formats besser
als ein generischer Prompt. `llm_instructions` macht dieses Wissen explizit und maschinenlesbar.

### 4. `content_mode` routet nur die Kontextlabels

`content_mode: Literal["fiction", "nonfiction"]` steuert **nur** die Beschriftung
im User-Prompt (`Logline` vs. `Kernaussage/These`, `Protagonist` wird weggelassen, etc.).
Es schränkt **nicht** ein, welche Frameworks verfügbar sind oder welcher System-Prompt verwendet wird.

### 5. `system_prompt` als vollständiger Override

Für Sonderfälle kann `FrameworkDefinition.system_prompt` den gesamten System-Prompt ersetzen.
Dies ist für spezialisierte Anwendungsfälle gedacht (z.B. Drehbuch-spezifisches Formatting).

## Implementierung

```
gen.generate(framework_key, context) 
  └─ get_framework(key)               # Framework aus Registry
  └─ _get_system_prompt(framework)    # framework.system_prompt OR _SYSTEM_PROMPT
  └─ _build_user_prompt(framework, context)
       └─ beats_overview              # aus framework.beats (immer dynamisch)
       └─ _format_context_block(...)  # alle non-leeren context fields
       └─ framework.llm_instructions  # framework-spezifische Guidance
  └─ router.completion(messages)
  └─ parse_nodes(raw_response)
```

## Extensibility

Custom Frameworks können via `register_framework()` registriert werden:

```python
from outlinefw import register_framework, FrameworkDefinition, BeatDefinition, ActPhase, TensionLevel

THESIS = FrameworkDefinition(
    key="thesis",
    name="Wissenschaftliche Arbeit (Thesis)",
    content_mode="nonfiction",
    llm_instructions="Forschungsstand muss Forschungsluecke benennen...",
    beats=[...],
)
register_framework(THESIS)
```

## Konsequenzen

**Positiv:**
- Jedes Framework kann domänenspezifische LLM-Guidance mitbringen
- Kein hardcoding: neue Frameworks brauchen keine Änderung an `generator.py`
- Voller Kontext: der LLM hat alle verfügbaren Projektinformationen
- Backward-compatible: bestehende Frameworks ohne `llm_instructions` funktionieren unverändert

**Negativ/Trade-offs:**
- Längere User-Prompts (mehr Token-Verbrauch bei gut befülltem ProjectContext)
- Qualität der `llm_instructions` hängt von Framework-Autor ab

## Alternativen (verworfen)

| Alternative | Grund für Ablehnung |
|-------------|--------------------|
| Jinja2 Template-Strings in FrameworkDefinition | Unnötige Dependency, str.format() + llm_instructions reicht |
| Separater PromptStrategy-Klass | Überkomplex für den Anwendungsfall |
| Hardcoded if/else pro Framework-Typ | Nicht erweiterbar ohne Code-Änderung |
| Zwei-Pfad-Architektur in Consumer (writing-hub) | Logik gehört ins Framework, nicht in den Consumer |
