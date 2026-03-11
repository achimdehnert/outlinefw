"""
outlinefw/src/outlinefw/frameworks.py

Complete, versioned story framework definitions for iil-outlinefw v0.1.0.
All frameworks validated on import via FrameworkDefinition (Pydantic).
"""

from __future__ import annotations

from outlinefw.schemas import ActPhase, BeatDefinition, FrameworkDefinition, TensionLevel

THREE_ACT = FrameworkDefinition(
    key="three_act",
    name="Drei-Akt-Struktur",
    description=(
        "Die klassische Drei-Akt-Struktur nach Aristoteles. "
        "Akt 1: Exposition und Aufbruch. Akt 2: Konfrontation und Komplikation. "
        "Akt 3: Klimax und Aufloesung."
    ),
    version="1.0.0",
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
            description=(
                "Der Protagonist trifft eine unwiderrufliche Entscheidung und tritt in Akt 2 ein."
            ),
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="midpoint",
            position=0.50,
            act=ActPhase.ACT_2A,
            description="Falsche Niederlage oder falscher Sieg.",
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
            description="Die neue Normalitaet.",
            tension=TensionLevel.LOW,
        ),
    ],
)

SAVE_THE_CAT = FrameworkDefinition(
    key="save_the_cat",
    name="Save the Cat (Blake Snyder)",
    description="Blake Snyders 15-Beat-Sheet fuer kommerziell erfolgreiche Drehbuecher.",
    version="1.0.0",
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
            description="Einfuehrung der B-Story.",
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
            description="Das Gegenteil von Akt-2-Einstieg.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="dark_night_of_the_soul",
            position=0.80,
            act=ActPhase.ACT_2B,
            description="Der tiefste Moment.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="break_into_three",
            position=0.85,
            act=ActPhase.ACT_3,
            description="A- und B-Story konvergieren.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="finale",
            position=0.92,
            act=ActPhase.ACT_3,
            description="Der Protagonist stuermt die Burg.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="final_image",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Spiegel zum Opening Image.",
            tension=TensionLevel.LOW,
        ),
    ],
)

HEROS_JOURNEY = FrameworkDefinition(
    key="heros_journey",
    name="Heldenreise (Joseph Campbell)",
    description="Joseph Campbells Monomythos. 12 Stationen der transformativen Reise des Helden.",
    version="1.0.0",
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
            description="Der Mentor erscheint.",
            tension=TensionLevel.LOW,
        ),
        BeatDefinition(
            name="crossing_the_threshold",
            position=0.28,
            act=ActPhase.ACT_2A,
            description="Der Held betritt die besondere Welt.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="tests_allies_enemies",
            position=0.38,
            act=ActPhase.ACT_2A,
            description="Der Held wird getestet.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="approach_to_inmost_cave",
            position=0.48,
            act=ActPhase.ACT_2A,
            description="Annaeherung an das Heiligtum.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="ordeal",
            position=0.55,
            act=ActPhase.ACT_2B,
            description="Die zentrale Krise.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="reward",
            position=0.65,
            act=ActPhase.ACT_2B,
            description="Der Held ueberlebt und gewinnt den Preis.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="road_back",
            position=0.75,
            act=ActPhase.ACT_3,
            description="Aufbruch zur Heimreise.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="resurrection",
            position=0.88,
            act=ActPhase.ACT_3,
            description="Zweite Krise. Letzte Transformation.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="return_with_elixir",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Heimkehr mit dem Elixier.",
            tension=TensionLevel.LOW,
        ),
    ],
)

FIVE_ACT = FrameworkDefinition(
    key="five_act",
    name="Fuenf-Akt-Struktur (Shakespeare)",
    description=(
        "Gustav Freytags Pyramide. 5 Akte: Exposition, Steigerung, Klimax, Wendung, Katastrophe."
    ),
    version="1.0.0",
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
            description="Zunehmende Komplikationen.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="climax",
            position=0.50,
            act=ActPhase.ACT_2B,
            description="Wendepunkt. Der entscheidende Moment.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="falling_action",
            position=0.72,
            act=ActPhase.ACT_3,
            description="Die Konsequenzen des Klimax.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="denouement",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Katastrophe oder Apotheose. Finale Ordnung.",
            tension=TensionLevel.LOW,
        ),
    ],
)

DAN_HARMON = FrameworkDefinition(
    key="dan_harmon",
    name="Dan Harmon Story Circle",
    description=(
        "Dan Harmons Vereinfachung der Heldenreise in 8 Stationen. Ideal fuer Episodenformat."
    ),
    version="1.0.0",
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
            description="Suche nach dem Ziel.",
            tension=TensionLevel.MEDIUM,
        ),
        BeatDefinition(
            name="find",
            position=0.50,
            act=ActPhase.ACT_2B,
            description="Die Figur findet, was sie gesucht hat.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="take",
            position=0.63,
            act=ActPhase.ACT_2B,
            description="Das Gefundene wird genommen.",
            tension=TensionLevel.PEAK,
        ),
        BeatDefinition(
            name="return",
            position=0.75,
            act=ActPhase.ACT_3,
            description="Rueckkehr in die vertraute Welt.",
            tension=TensionLevel.HIGH,
        ),
        BeatDefinition(
            name="change",
            position=1.0,
            act=ActPhase.ACT_3,
            description="Die Figur hat sich veraendert.",
            tension=TensionLevel.LOW,
        ),
    ],
)


FRAMEWORKS: dict[str, FrameworkDefinition] = {
    "three_act": THREE_ACT,
    "save_the_cat": SAVE_THE_CAT,
    "heros_journey": HEROS_JOURNEY,
    "five_act": FIVE_ACT,
    "dan_harmon": DAN_HARMON,
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
        }
        for fw in FRAMEWORKS.values()
    ]
