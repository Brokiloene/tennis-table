
def recreate_db():
    from sqlalchemy_utils import database_exists, create_database, drop_database
    from tennis_app.models import engine

    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    

def test_fill_db():
    from tennis_app.dto import CreateMatchDTO
    from tennis_app.dao import MatchDAO, PlayerDAO

    players = [
        "Bjorn Borg", #1
        "John McEnroe", #2
        "Ivan Lendl", #3
        "Roger Federer", #4
        "Pete Sampras", #5
        "Rafael Nadal", #6
        "John Isner", #7
        "Nicolas Mahut", #8
        "Andre Agassi", #9
        "Fernando Verdasco", #10
        "Andy Roddick", #11
        "Novac Djokovic", #12
        "Stanislas Wawrinka", #13
        "Juan Martin del Potro" # 14
    ]
    matches = [
        CreateMatchDTO(
            uuid='test-match-1',
            player1_id=1,
            player2_id=2,
            winner_id=1,
            score="1 6 7 5 6 3"
        ),
        CreateMatchDTO(
            uuid='test-match-2',
            player1_id=2,
            player2_id=1,
            winner_id=2,
            score="4 6 7 6 7 6"
        ),
        CreateMatchDTO(
            uuid='test-match-3',
            player1_id=3,
            player2_id=2,
            winner_id=3,
            score="3 6 7 5 7 5"
        ),
        CreateMatchDTO(
            uuid='test-match-4',
            player1_id=4,
            player2_id=5,
            winner_id=5,
            score="5 7 6 4 6 7"
        ),
        CreateMatchDTO(
            uuid='test-match-5',
            player1_id=7,
            player2_id=8,
            winner_id=7,
            score="6 4 3 6 7 6"
        ),
        CreateMatchDTO(
            uuid='test-match-6',
            player1_id=5,
            player2_id=9,
            winner_id=5,
            score="6 7 7 6 7 6"
        ),
        CreateMatchDTO(
            uuid='test-match-7',
            player1_id=6,
            player2_id=10,
            winner_id=6,
            score="6 7 6 4 7 6"
        ),
        CreateMatchDTO(
            uuid='test-match-8',
            player1_id=4,
            player2_id=11,
            winner_id=4,
            score="5 7 7 6 7 6"
        ),
        CreateMatchDTO(
            uuid='test-match-9',
            player1_id=12,
            player2_id=6,
            winner_id=12,
            score="5 7 6 4 6 2"
        ),
        CreateMatchDTO(
            uuid='test-match-10',
            player1_id=6,
            player2_id=13,
            winner_id=6,
            score="6 2 3 6 6 1"
        ),
        CreateMatchDTO(
            uuid='test-match-11',
            player1_id=6,
            player2_id=14,
            winner_id=6,
            score="1 6 6 1 7 6"
        )
    ]

    for player in players:
        PlayerDAO.insert_one(name=player)
    for match_dto in matches:
        MatchDAO.insert_one(dto=match_dto)

def start():
    recreate_db()

    import subprocess
    subprocess.run("alembic revision --autogenerate -m 'Create database'", shell=True)
    subprocess.run("alembic upgrade head", shell=True)

    test_fill_db()
