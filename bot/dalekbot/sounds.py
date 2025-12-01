from pydantic import BaseModel


class Sound(BaseModel):
    identifier: str
    file_path: str
    description: str

def new_identifier(namespace: str, name: str) -> str:
    return f"{namespace}.{name}"

SOUNDS = [
    Sound(
        identifier=new_identifier("dalekbot", "exterminate"),
        file_path="data/sounds/exterminate.ogg",
        description="Dalek's iconic 'Exterminate!' catchphrase.",
    ),
    Sound(
        identifier=new_identifier("dalekbot", "uwu"),
        file_path="data/sounds/uwu.ogg",
        description="A cute 'uwu' sound effect.",
    ),
]
