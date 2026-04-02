"""
outlinefw/src/outlinefw/frameworks.py

Framework definitions for iil-outlinefw.
Each framework defines: structure (beats), content_mode, and llm_instructions.

llm_instructions give the LLM domain-specific guidance that is appended
to the user prompt at generation time (ADR-001).

Fiction:     three_act, save_the_cat, heros_journey, five_act, dan_harmon
Non-Fiction: scientific_essay, academic_essay, imrad_article, essay
"""

from __future__ import annotations

from outlinefw.schemas import ActPhase, BeatDefinition, FrameworkDefinition, TensionLevel

# =============================================================================
# Fiction Frameworks
# =============================================================================

THREE_ACT = FrameworkDefinition(
    key="three_act",
    name="Drei-Akt-Struktur",
    description=(
        "Die klassische Drei-Akt-Struktur nach Aristoteles. "
        "Akt 1: Exposition und Aufbruch. Akt 2: Konfrontation und Komplikation. "
        "Akt 3: Klimax und Aufloesung."
    ),
    version="1.0.0",
    llm_instructions=(
        "Sorge fuer einen konsistenten Charakter-Bogen des Protagonisten ueber alle drei Akte. "
        "Jeder Beat muss kausal aus dem vorherigen folgen. "
        "Der Midpoint muss eine echte Verschiebung in der Zielsetzung des Protagonisten erzeugen."
    ),
    beats=[
        BeatDefinition(
            name="exposition",
            position=0.0,
            act=ActPhase.ACT_1,
            description="Vorstellung der Welt, der Figuren und des Status Quo.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="inciting_incident",
            position=0.12,
            act=ActPhase.ACT_1,
            description="Das ausloesende Ereignis, das die Geschichte in Gang setzt.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="first_turning_point",
            position=0.25,
            act=ActPhase.ACT_1,
            description="Der Protagonist trifft eine unwiderrufliche Entscheidung und tritt in Akt 2 ein.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="midpoint",
            position=0.50,
            act=ActPhase.ACT_2A,
            description="Falsche Niederlage oder falscher Sieg. Zielsetzung des Protagonisten verschiebt sich.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="second_turning_point",
            position=0.75,
            act=ActPhase.ACT_2B,
            description="Tiefpunkt: Alles scheint verloren.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="climax",
            position=0.88,
            act=ActPhase.ACT_3,
            description="Der finale Konflikt.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="resolution",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Die neue Normalitaet nach der Transformation.",
            tension=TensionLevel.LOW,
        ),
    ],
)

SAVE_THE_CAT = FrameworkDefinition(
    key="save_the_cat",
    name="Save the Cat (Blake Snyder)",
    description="Blake Snyders 15-Beat-Sheet fuer kommerziell erfolgreiche Drehbuecher.",
    version="1.0.0",
    llm_instructions=(
        "Halte dich strikt an Snyders Seitenzahlen-Proportionen (Catalyst bei ca. 12%, "
        "Break into Two bei 25%, Midpoint bei 50%, All is Lost bei 75%, Finale bei 92%). "
        "Fun and Games muss die Praemisse des Films einloesen, nicht nur Handlung beschreiben."
    ),
    beats=[
        BeatDefinition(
            name="opening_image",
            position=0.0,
            act=ActPhase.ACT_1,
            description="Ein Schnappschuss der Welt vor der Geschichte.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="theme_stated",
            position=0.05,
            act=ActPhase.ACT_1,
            description="Jemand formuliert das Thema der Geschichte.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="setup",
            position=0.09,
            act=ActPhase.ACT_1,
            description="Vorstellung von Welt, Figuren und Status Quo.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="catalyst",
            position=0.12,
            act=ActPhase.ACT_1,
            description="Das ausloesende Ereignis.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="debate",
            position=0.18,
            act=ActPhase.ACT_1,
            description="Der Protagonist zoegert.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="break_into_two",
            position=0.25,
            act=ActPhase.ACT_2A,
            description="Der Protagonist waehlt aktiv.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="b_story",
            position=0.30,
            act=ActPhase.ACT_2A,
            description="Einfuehrung der B-Story (oft der Liebes-/Lernstrang).",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="fun_and_games",
            position=0.38,
            act=ActPhase.ACT_2A,
            description="Die Praemisse des Films wird eingeloest.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="midpoint",
            position=0.50,
            act=ActPhase.ACT_2A,
            description="Falscher Sieg oder falsche Niederlage.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="bad_guys_close_in",
            position=0.60,
            act=ActPhase.ACT_2B,
            description="Antagonistische Kraefte schliessen sich zusammen.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="all_is_lost",
            position=0.75,
            act=ActPhase.ACT_2B,
            description="Das Gegenteil von Akt-2-Einstieg. Alles ist verloren.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="dark_night_of_the_soul",
            position=0.80,
            act=ActPhase.ACT_2B,
            description="Der tiefste Moment. Innere Einkehr.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="break_into_three",
            position=0.85,
            act=ActPhase.ACT_3,
            description="A- und B-Story konvergieren zur Loesung.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="finale",
            position=0.92,
            act=ActPhase.ACT_3,
            description="Der Protagonist stuermt die Burg. Alle fuenf Punkte des Finales.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="final_image",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Spiegel zum Opening Image — zeigt die Transformation.",
            tension=TensionLevel.LOW,
        ),
    ],
)

HEROS_JOURNEY = FrameworkDefinition(
    key="heros_journey",
    name="Heldenreise (Joseph Campbell)",
    description="Joseph Campbells Monomythos. 12 Stationen der transformativen Reise des Helden.",
    version="1.0.0",
    llm_instructions=(
        "Die Transformation des Helden muss psychologisch glaubwuerdig sein. "
        "Der Mentor darf nicht zu viel loesen — der Held muss selbst wachsen. "
        "Das Elixier in der letzten Station muss eine greifbare innere Veraenderung repraesentieren."
    ),
    beats=[
        BeatDefinition(
            name="ordinary_world",
            position=0.0,
            act=ActPhase.ACT_1,
            description="Die gewoehnliche Welt des Helden.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="call_to_adventure",
            position=0.09,
            act=ActPhase.ACT_1,
            description="Der Ruf zur Reise.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="refusal_of_call",
            position=0.16,
            act=ActPhase.ACT_1,
            description="Der Held verweigert zunaechst.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="meeting_the_mentor",
            position=0.22,
            act=ActPhase.ACT_1,
            description="Der Mentor erscheint und gibt dem Helden Werkzeuge/Weisheit.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="crossing_the_threshold",
            position=0.28,
            act=ActPhase.ACT_2A,
            description="Der Held betritt die besondere Welt. Kein Zurueck.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="tests_allies_enemies",
            position=0.38,
            act=ActPhase.ACT_2A,
            description="Der Held wird getestet, findet Verbündete und Feinde.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="approach_to_inmost_cave",
            position=0.48,
            act=ActPhase.ACT_2A,
            description="Annaeherung an das zentrale Heiligtum/den Kern des Problems.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="ordeal",
            position=0.55,
            act=ActPhase.ACT_2B,
            description="Die zentrale Krise. Der Held konfrontiert seinen groessten Feind/Angst.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="reward",
            position=0.65,
            act=ActPhase.ACT_2B,
            description="Der Held ueberlebt und gewinnt den Preis (auesserlich und innerlich).",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="road_back",
            position=0.75,
            act=ActPhase.ACT_3,
            description="Aufbruch zur Heimreise. Neue Bedrohung entsteht.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="resurrection",
            position=0.88,
            act=ActPhase.ACT_3,
            description="Zweite, finale Krise. Letzte und vollstaendige Transformation.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="return_with_elixir",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Heimkehr mit dem Elixier — Weisheit, Schatz oder Heilung fuer die Gemeinschaft.",
            tension=TensionLevel.LOW,
        ),
    ],
)

FIVE_ACT = FrameworkDefinition(
    key="five_act",
    name="Fuenf-Akt-Struktur (Shakespeare/Freytag)",
    description="Gustav Freytags Pyramide. 5 Akte: Exposition, Steigerung, Klimax, Wendung, Katastrophe.",
    version="1.0.0",
    llm_instructions=(
        "Die Steigerung muss durch konkrete Ereignisse getrieben sein, nicht nur durch Emotionen. "
        "Der Klimax muss der dramatische Hoehepunkt sein, von dem alles abfaellt. "
        "Denouement zeigt die neue Ordnung der Welt nach dem dramatischen Bruch."
    ),
    beats=[
        BeatDefinition(
            name="exposition",
            position=0.0,
            act=ActPhase.ACT_1,
            description="Einfuehrung der Figuren, der Welt und des dramatischen Konflikts.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="rising_action",
            position=0.22,
            act=ActPhase.ACT_2A,
            description="Zunehmende Komplikationen. Spannungssteigerung durch Ereignisse.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="climax",
            position=0.50,
            act=ActPhase.ACT_2B,
            description="Wendepunkt. Der entscheidende Moment. Hoehepunkt der Spannung.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="falling_action",
            position=0.72,
            act=ActPhase.ACT_3,
            description="Die Konsequenzen des Klimax. Spannungsabfall.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="denouement",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Katastrophe oder Apotheose. Finale Ordnung der Welt.",
            tension=TensionLevel.LOW,
        ),
    ],
)

DAN_HARMON = FrameworkDefinition(
    key="dan_harmon",
    name="Dan Harmon Story Circle",
    description="Dan Harmons Vereinfachung der Heldenreise in 8 Stationen. Ideal fuer Episodenformat.",
    version="1.0.0",
    llm_instructions=(
        "Der Circle muss sich schliessen: die Figur kehrt zurueck, aber veraendert. "
        "'Find' und 'Take' muessen emotional unterschiedliche Qualitaeten haben. "
        "Ideal fuer episodisches Erzaehlen: jede Episode kann einen eigenen Circle haben."
    ),
    beats=[
        BeatDefinition(
            name="you",
            position=0.0,
            act=ActPhase.ACT_1,
            description="Eine Figur in ihrer Komfortzone.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="need",
            position=0.14,
            act=ActPhase.ACT_1,
            description="Die Figur will oder braucht etwas.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="go",
            position=0.25,
            act=ActPhase.ACT_2A,
            description="Die Figur verlaesst die Komfortzone.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="search",
            position=0.38,
            act=ActPhase.ACT_2A,
            description="Suche nach dem Ziel. Hindernisse und Entscheidungen.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="find",
            position=0.50,
            act=ActPhase.ACT_2B,
            description="Die Figur findet, was sie gesucht hat — aber zu einem Preis.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="take",
            position=0.63,
            act=ActPhase.ACT_2B,
            description="Das Gefundene wird genommen/bezahlt. Die Konsequenz trifft ein.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="return",
            position=0.75,
            act=ActPhase.ACT_3,
            description="Rueckkehr in die vertraute Welt mit dem Gewonnenen.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="change",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Die Figur und/oder die Welt haben sich veraendert.",
            tension=TensionLevel.LOW,
        ),
    ],
)


# =============================================================================
# Non-Fiction Frameworks
# =============================================================================

SCIENTIFIC_ESSAY = FrameworkDefinition(
    key="scientific_essay",
    name="Wissenschaftlicher Aufsatz",
    description=(
        "Argumentativ-hermeneutischer Aufsatz fuer Fachzeitschriften, Sammelbände oder "
        "Qualifikationsarbeiten in Geistes- und Sozialwissenschaften."
    ),
    version="1.0.0",
    content_mode="nonfiction",
    llm_instructions=(
        "Keine Romandramaturgie. Jeder Abschnitt muss eine klar definierte wissenschaftliche "
        "Funktion haben (Framing, Forschungsstand, Analyse, Synthese, Kritik). "
        "Die These aus der Einleitung muss im Fazit explizit beantwortet werden. "
        "Argumente muessen evidenzbasiert sein (Quellen, Fallbeispiele, Theorien). "
        "Der Forschungsstand muss die Forschungsluecke benennen, die der Aufsatz schliesst."
    ),
    beats=[
        BeatDefinition(
            name="einleitung",
            position=0.0,
            act=ActPhase.ACT_OPEN,
            description="These, Problemstellung, wissenschaftliche Relevanz und Aufbau des Aufsatzes.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="forschungsstand",
            position=0.15,
            act=ActPhase.ACT_1,
            description="Einordnung in bestehende Literatur, Forschungsluecke benennen.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="theoretischer_rahmen",
            position=0.28,
            act=ActPhase.ACT_1,
            description="Theoretische Grundlagen, Schluesselkonzepte und analytisches Instrumentarium.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="hauptargument_1",
            position=0.45,
            act=ActPhase.ACT_2A,
            description="Erstes zentrales Argument mit Belegen, Beispielen und Analyse.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="hauptargument_2",
            position=0.62,
            act=ActPhase.ACT_2B,
            description="Zweites zentrales Argument, vertiefend oder kontrastierend zum ersten.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="diskussion",
            position=0.78,
            act=ActPhase.ACT_3,
            description="Kritische Wuerdigung, Gegenargumente, Grenzen der Analyse, Implikationen.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="fazit",
            position=1.0,
            act=ActPhase.ACT_CLOSE,
            description="These beantworten, Erkenntnisse zusammenfassen, weiteren Forschungsbedarf benennen.",
            tension=TensionLevel.LOW,
        ),
    ],
)

ACADEMIC_ESSAY = FrameworkDefinition(
    key="academic_essay",
    name="Akademischer Essay",
    description=(
        "Strukturierter argumentativer Essay fuer Hochschulseminare, Pruefungsleistungen "
        "und Qualifikationsarbeiten auf Bachelor-/Masterniveau."
    ),
    version="1.0.0",
    content_mode="nonfiction",
    llm_instructions=(
        "Klare Thesenstruktur: eine Hauptthese, die durch alle Abschnitte bewiesen wird. "
        "Der Hintergrundabschnitt darf keine eigene Argumentation enthalten — nur Kontext setzen. "
        "Gegenargumente muessen ernst genommen und differenziert widerlegt oder integriert werden. "
        "Schluss muss ueber blosse Zusammenfassung hinausgehen: Was bedeutet das fuer das Feld?"
    ),
    beats=[
        BeatDefinition(
            name="einleitung",
            position=0.0,
            act=ActPhase.ACT_OPEN,
            description="These formulieren, Relevanz begruenden, Gliederung ankuendigen.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="hintergrund",
            position=0.18,
            act=ActPhase.ACT_1,
            description="Kontext, Grundbegriffe und notwendiges Vorwissen klaeren — ohne Eigenwertung.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="hauptteil",
            position=0.40,
            act=ActPhase.ACT_2A,
            description="Kernargumente entfalten, Belege anfuehren, Analyse vertiefen.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="gegenargumente",
            position=0.70,
            act=ActPhase.ACT_2B,
            description="Gegenpositionen darstellen und differenziert widerlegen oder produktiv integrieren.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="schluss",
            position=1.0,
            act=ActPhase.ACT_CLOSE,
            description="These bestaetigen, Erkenntnisse wuerdigen, Ausblick auf Implikationen geben.",
            tension=TensionLevel.LOW,
        ),
    ],
)

IMRAD_ARTICLE = FrameworkDefinition(
    key="imrad_article",
    name="IMRaD-Artikel (empirisch)",
    description=(
        "Empirischer Forschungsartikel nach IMRaD-Standard. "
        "Typisch fuer Natur-, Ingenieur- und empirische Sozialwissenschaften."
    ),
    version="1.0.0",
    content_mode="nonfiction",
    llm_instructions=(
        "Strikte IMRaD-Trennung einhalten: Results KEIN Interpretation, Discussion KEINE neuen Daten. "
        "Methods muss so detailliert sein, dass die Studie repliziert werden koennte. "
        "Der Abstract muss eigenstaendig lesbar sein (Ziel, Methode, Ergebnis, Schlussfolgerung). "
        "Hypothesen aus der Introduction muessen in Results und Discussion explizit adressiert werden."
    ),
    beats=[
        BeatDefinition(
            name="abstract",
            position=0.0,
            act=ActPhase.ACT_OPEN,
            description="Eigenstaendige Kurzzusammenfassung: Ziel, Methode, Ergebnisse, Schlussfolgerung.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="introduction",
            position=0.10,
            act=ActPhase.ACT_1,
            description="Forschungsfrage, Forschungsstand, Ziel der Studie und Hypothesen.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="methods",
            position=0.28,
            act=ActPhase.ACT_2A,
            description="Forschungsdesign, Stichprobe, Datenerhebung, Auswertungsverfahren.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="results",
            position=0.50,
            act=ActPhase.ACT_2A,
            description="Darstellung der Ergebnisse ohne Interpretation. Tabellen, Grafiken, Befunde.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="discussion",
            position=0.72,
            act=ActPhase.ACT_2B,
            description="Interpretation, Einordnung in Literatur, Limitations, Implikationen.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="conclusion",
            position=1.0,
            act=ActPhase.ACT_CLOSE,
            description="Hauptbefunde zusammenfassen, Beitrag zum Feld benennen, weiteren Forschungsbedarf.",
            tension=TensionLevel.LOW,
        ),
    ],
)

ESSAY = FrameworkDefinition(
    key="essay",
    name="Essay (literarisch-reflexiv)",
    description=(
        "Freier, reflexiver Essay fuer Feuilleton, Kulturmagazine oder literarische Zeitschriften. "
        "Denkerisch und subjektiv, aber argumentativ stringent."
    ),
    version="1.0.0",
    content_mode="nonfiction",
    llm_instructions=(
        "Persoenliche Stimme und subjektive Perspektive sind Qualitaetsmerkmale des Essays, keine Fehler. "
        "Assoziative Verbindungen zwischen Ideen sind erwuenscht, muessen aber einem roten Faden folgen. "
        "Die Wende muss die Ausgangsperspektive echte verschieben oder in Frage stellen. "
        "Schluss darf offen bleiben — gute Essays stellen Fragen, die im Leser nachhallen."
    ),
    beats=[
        BeatDefinition(
            name="einstieg",
            position=0.0,
            act=ActPhase.ACT_OPEN,
            description="Anekdote, Zitat, provokante Beobachtung oder Frage als Einstieg.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="entfaltung",
            position=0.22,
            act=ActPhase.ACT_1,
            description="Thema entfalten — assoziativ, persoenlich, mit Bezug zur eigenen Perspektive.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="vertiefung",
            position=0.50,
            act=ActPhase.ACT_2A,
            description="Kerngedanke vertiefen, Beispiele und Referenzen organisch einflechten.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="wende",
            position=0.75,
            act=ActPhase.ACT_2B,
            description="Unerwartete Wendung, Gegenposition oder Selbstwiderlegung beleuchtet das Thema neu.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="schluss",
            position=1.0,
            act=ActPhase.ACT_CLOSE,
            description="Offene oder pointierte Schlussreflexion — keine blossen Zusammenfassungen.",
            tension=TensionLevel.MEDIUM,
        ),
    ],
)


# =============================================================================
# Registry
# =============================================================================

FRAMEWORKS: dict[str, FrameworkDefinition] = {
    # Fiction
    "three_act": THREE_ACT,
    "save_the_cat": SAVE_THE_CAT,
    "heros_journey": HEROS_JOURNEY,
    "five_act": FIVE_ACT,
    "dan_harmon": DAN_HARMON,
    # Non-Fiction
    "scientific_essay": SCIENTIFIC_ESSAY,
    "academic_essay": ACADEMIC_ESSAY,
    "imrad_article": IMRAD_ARTICLE,
    "essay": ESSAY,
}


def get_framework(key: str) -> FrameworkDefinition:
    if key not in FRAMEWORKS:
        available = ", ".join(sorted(FRAMEWORKS))
        raise KeyError(f"Unknown framework key: {key!r}. Available: {available}")
    return FRAMEWORKS[key]


def list_frameworks() -> list[dict[str, str]]:
    return [
        {
            "key": fw.key,
            "name": fw.name,
            "description": fw.description,
            "version": fw.version,
            "beat_count": str(len(fw.beats)),
            "content_mode": fw.content_mode,
        }
        for fw in FRAMEWORKS.values()
    ]


def register_framework(framework: FrameworkDefinition) -> None:
    """Register a custom framework. Raises ValueError if key already exists."""
    if framework.key in FRAMEWORKS:
        raise ValueError(
            f"Framework key {framework.key!r} already registered. "
            f"Use unregister_framework() first to replace it."
        )
    FRAMEWORKS[framework.key] = framework


def unregister_framework(key: str) -> FrameworkDefinition:
    """Remove a framework. Returns it. Raises KeyError if not found."""
    if key not in FRAMEWORKS:
        available = ", ".join(sorted(FRAMEWORKS))
        raise KeyError(f"Unknown framework key: {key!r}. Available: {available}")
    return FRAMEWORKS.pop(key)
