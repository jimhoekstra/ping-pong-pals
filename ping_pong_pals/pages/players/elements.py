from newsflash.elements import Table, Plot, Checkbox


class PlayersTable(Table):
    id: str = "players-table"


class PlotWonGamesToggle(Checkbox):
    id: str = "plot-won-games-toggle"
    label: str = "Only show won games"


class PlayersPlot(Plot):
    id: str = "players-plot"
