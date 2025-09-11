import datetime


def vacuum_utility(db, force: bool = False, full: bool = False, logger=None):
    # if last vacuum more than 3 days but less than 6 run a normal vacuum
    # Else if more than 6 run a full vacuum analyze

    db.autocommit = True

    with db.cursor() as cur:
        cur.execute("""
            SELECT MAX(GREATEST(
                COALESCE(last_vacuum, 'epoch'),
                COALESCE(last_autovacuum, 'epoch')
            )) FROM pg_stat_user_tables;
        """)
        result = cur.fetchone()
        last_vacuum = result[0]
        now = datetime.datetime.now(datetime.timezone.utc)
        days_since_vacuum = (now - last_vacuum).days if last_vacuum else None

        # Decidir qual vacuum rodar
        if (force and full) or (days_since_vacuum is None or days_since_vacuum > 6):
            if logger:
                logger.info(f"Dias desde último vacuum: {days_since_vacuum}")
                logger.info("Rodando FULL VACUUM ANALYZE...")
            cur.execute("VACUUM FULL ANALYZE;")
        elif force or days_since_vacuum is not None and days_since_vacuum > 3:
            if logger:
                logger.info("Rodando VACUUM...")
            cur.execute("VACUUM;")
        else:
            if logger:
                logger.info("VACUUM não necessário.")
