from lichess import api
from lichess.format import PGN


pgns = api.user_games('BLAC3', format=PGN, max=100_000)
with open('D:/BLAC3/games.txt', 'a') as file:
    while True:
        pgn = next(pgns)
        try:
            file.write(pgn)
        except UnicodeEncodeError:
            pass  # happens for some symbols in names or tournament titles, which are an insignificant fraction
