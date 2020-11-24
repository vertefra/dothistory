def test_database_not_None(test_app_with_db):
    ''' Test that the instance of db_test exists '''
    db = test_app_with_db.db

    assert db is not None


# def test_tables_are_created(test_app_with_db):
