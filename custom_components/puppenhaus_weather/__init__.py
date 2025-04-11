"""Init for Puppenhaus Wetter platform."""

DOMAIN = "puppenhaus_weather"

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Old-style platform setup (unused here)."""
    pass

def setup(hass, config):
    """Set up is called when Home Assistant is loading config."""
    return True
