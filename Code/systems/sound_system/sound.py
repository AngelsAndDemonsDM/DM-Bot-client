from audioplayer import AudioPlayer
from pathlib import Path
from root_path import ROOT_PATH


class Sound:
    def __init__(self, path: Path | str) -> None:
        audio_path = ROOT_PATH / "Content" / path
        if not Sound._check_audio_path(audio_path):
            raise ValueError(f"{path} is not a mp3 file or doesn't exist")
        self.player = AudioPlayer(audio_path)
                
    @staticmethod
    def _check_audio_path(audio_path: Path) -> bool:
        if audio_path.exists() and audio_path.is_file() and audio_path.suffix.lower() == ".mp3":
            return True
        else:
            return False
