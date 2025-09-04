import datetime


def vacuum_utility(db, force: bool = False, full: bool = False):
    # if last vacuum more than 3 days but less than 6 run a normal vacuum
    # Else if more than 6 run a full vacuum analyze
    with db.cursor() as cur:
        cur.execute("""
            SELECT MAX(GREATEST(
                COALESCE(last_vacuum, 'epoch'),
                COALESCE(last_autovacuum, 'epoch')
            )) FROM pg_stat_user_tables;
        """)
        last_vacuum = cur.fetchone()[0]

        now = datetime.datetime.now(datetime.timezone.utc)
        days_since_vacuum = (now - last_vacuum).days if last_vacuum else None
        # Decidir qual vacuum rodar
        if force or full or (days_since_vacuum is not None and days_since_vacuum > 6):
            print("Rodando FULL VACUUM ANALYZE...")
            cur.execute("VACUUM FULL ANALYZE;")
        elif days_since_vacuum is not None and days_since_vacuum > 3:
            print("Rodadndo VACUUM...")
            cur.execute("VACUUM;")
        else:
            print("VACUUM não necessário.")

        db.commit()
