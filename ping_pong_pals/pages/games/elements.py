from typing import Iterable

from newsflash.models import Element
from newsflash.elements import (
    Select,
    InputInteger,
    Button,
    Paragraph,
    Vertical,
    Table,
)


class WinnerSelect(Select):
    id: str = "winner-select"


class WinnerPointsInput(InputInteger):
    id: str = "winner-points-input"
    placeholder: str = "winner points"
    value: int = 11


class LoserSelect(Select):
    id: str = "loser-select"


class LoserPointsInput(InputInteger):
    id: str = "loser-points-input"
    placeholder: str = "loser points"


class SubmitGameButton(Button):
    id: str = "submit-game-button"
    label: str = "Submit Game"


class NewGameForm(Vertical):
    id: str = "new-games-form"

    def compose(self) -> Iterable[Element]:
        yield Paragraph(id="winner-paragraph", text="Select the winner:")
        yield WinnerSelect()
        yield WinnerPointsInput()
        yield Paragraph(id="loser-paragraph", text="Select the loser:")
        yield LoserSelect()
        yield LoserPointsInput()
        yield SubmitGameButton()


class GamesTable(Table):
    id: str = "games-table"
