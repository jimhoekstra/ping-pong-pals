from ping_pong_pals.database import get_db
from ping_pong_pals.scores import recompute_all_scores


def main():
    db = get_db()

    try:
        recompute_all_scores(db=db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
