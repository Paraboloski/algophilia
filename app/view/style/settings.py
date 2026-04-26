from pathlib import Path

_MAIN_COLORS = {
    "bg_dark": "#15161A",
    "bg_light": "#EFF6FF",
    "info_dark": "#1E3A5F",
    "info_light": "#3B82F6",
    "error_dark": "#4A1515",
    "error_light": "#AB3326",
    "warning_dark": "#3D2A00",
    "warning_light": "#F59E0B",
}

_MAIN_IMAGES = {
    "bg_fallback": Path("images") / "bg-fallback.png",
}

_MAIN_ICONS = {
    "info": Path("icons") / "info.svg",
    "error": Path("icons") / "error.svg",
    "close": Path("icons") / "close.svg",
    "warning": Path("icons") / "warning.svg",
}

_MAIN_FONTS = {
    "cinzel_bold": Path("fonts") / "Cinzel-Bold.ttf",
    "cinzel_black": Path("fonts") / "Cinzel-Black.ttf",
    "cinzel_medium": Path("fonts") / "Cinzel-Medium.ttf",
    "cinzel_regular": Path("fonts") / "Cinzel-Regular.ttf",
    "cinzel_semibold": Path("fonts") / "Cinzel-SemiBold.ttf",
    "cinzel_extrabold": Path("fonts") / "Cinzel-ExtraBold.ttf",
}

class Settings:
    def __init__ (self):
        self._main_width = 402
        self._main_height = 874
        self._app_name = "Algophilia"
        self._main_fonts = _MAIN_FONTS
        self._main_icons = _MAIN_ICONS
        self._main_colors = _MAIN_COLORS
        self._main_images = _MAIN_IMAGES
        
settings = Settings()