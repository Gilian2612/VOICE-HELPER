"""Captura del audio del sistema vía WASAPI loopback (solo Windows).

Pendiente: implementar y probar en un PC con Windows.
"""

from collections.abc import Iterator


def list_devices() -> None:
    """Lista los dispositivos de audio y marca los loopback disponibles."""
    raise NotImplementedError("Pendiente: requiere Windows + PyAudioWPatch")


def stream_system_audio() -> Iterator[bytes]:
    """Genera bloques PCM 16-bit del audio que sale por los parlantes."""
    raise NotImplementedError("Pendiente: requiere Windows + PyAudioWPatch")
