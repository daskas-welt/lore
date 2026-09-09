"""Unit tests for the TUI section parser (split_sections)."""

from lore.tui import split_sections

SAMPLE = (
    "A narrow defile between two black cliffs, choked with the wreckage of a "
    "forgotten war.\n"
    "Read-Aloud: The trail funnels into a gap where the mountains nearly "
    "touch. Splintered shields and rusted mail crust the scree.\n"
    "Atmosphere: Cold, exposed, wind howling through the gap, tense. "
    "Hazards: Rockfall (DC 13 DEX), ambush positions. Hooks: Siege engine "
    "wreck. Sounds: Wind through the gap."
)


class TestSplitSections:
    def test_no_sections_returns_body_and_empty(self):
        intro, sections = split_sections("Just a plain description.")
        assert intro == "Just a plain description."
        assert sections == []

    def test_all_five_sections_parsed(self):
        intro, sections = split_sections(SAMPLE)
        assert "defile" in intro
        assert "forgotten war" in intro
        keys = [k for k, _ in sections]
        assert keys == ["Read-Aloud", "Atmosphere", "Hazards", "Hooks", "Sounds"]
        by_key = dict(sections)
        assert "mountains nearly touch" in by_key["Read-Aloud"]
        assert "Rockfall (DC 13 DEX)" in by_key["Hazards"]
        assert "Siege engine wreck" in by_key["Hooks"]
        assert "Wind through the gap" in by_key["Sounds"]

    def test_line_start_sections(self):
        body = "Intro text.\nAtmosphere: Quiet.\nHooks: A stray dog follows."
        intro, sections = split_sections(body)
        assert intro == "Intro text."
        assert sections == [("Atmosphere", "Quiet."), ("Hooks", "A stray dog follows.")]

    def test_case_insensitive_keys(self):
        intro, sections = split_sections("HazardS: spikes everywhere.")
        assert intro == ""
        assert sections == [("Hazards", "spikes everywhere.")]

    def test_read_aloud_variant_spellings(self):
        _, sections = split_sections("Read Aloud: step into the light.")
        assert sections == [("Read Aloud", "step into the light.")]

    def test_empty_body(self):
        assert split_sections("") == ("", [])

    def test_word_boundary_not_matched_inside_word(self):
        intro, sections = split_sections("The hooksmith forges sounds alike.")
        assert "hooksmith" in intro
        assert sections == []
