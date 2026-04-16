import pytest
from unittest.mock import MagicMock, patch

from models.category import Category
from models.sqllite_category_list import SqliteCategories

class MockCategory:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color

@pytest.fixture
def catlist():
    # Patch must stay active for the whole test (``add_category`` / ``delete_category`` call ordering).
    with patch.object(SqliteCategories, "_enforce_system_positions", lambda self: None):
        c_list = SqliteCategories()
        c_list.execute = MagicMock()
        yield c_list

@pytest.fixture
def category():
    return Category(None, "school", "yellow" )

#---------------------------------------------------------------------------------
# __EXECUTE FUNCTION__
#---------------------------------------------------------------------------------
def test_execute_calls_cursor_and_commit():
    """Test that execute function calls executes and commits queries"""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    with patch("sqlite3.connect", return_value=mock_conn), patch.object(
        SqliteCategories, "_enforce_system_positions", lambda self: None
    ):
        db = SqliteCategories()
        mock_cursor.reset_mock() # reset mock so execute is only called once
        mock_conn.reset_mock() # reset mock so commit is only called once
        query = "INSERT INTO category VALUES (?, ?)"
        args = ("Work", "green")
        result = db.execute(query, *args)
        mock_cursor.execute.assert_called_once_with(query, args)
        mock_conn.commit.assert_called_once()
        assert result == mock_cursor.execute.return_value
#---------------------------------------------------------------------------------
# __CREATE TABLE__
#---------------------------------------------------------------------------------
def test_create_table_query(catlist):
    """Test create table commits a CREATE TABLE query."""
    catlist.create_table()

    queries = [c.args[0] for c in catlist.execute.call_args_list]
    assert any("CREATE TABLE IF NOT EXISTS category" in q for q in queries)
#---------------------------------------------------------------------------------
# __LOAD FROM DB__
#---------------------------------------------------------------------------------
def test_load_category_query(catlist):
    """Test that load uses a SELECT on category."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "Todo", "teal", None)]
    catlist.execute = MagicMock(return_value=mock_cursor)
    catlist._ordered_ids = MagicMock(return_value=[1])

    catlist.load_categories()

    query = catlist.execute.call_args.args[0]
    assert "FROM category" in query
    assert "category_id" in query

def test_load_category_return(catlist):
    """Test load_categories return shape."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1, "Todo", "teal", None)]
    catlist.execute = MagicMock(return_value=mock_cursor)
    catlist._ordered_ids = MagicMock(return_value=[1])

    result = catlist.load_categories()

    assert result == [(1, "Todo", "teal")]
#---------------------------------------------------------------------------------
# __ADD TO DB__
#---------------------------------------------------------------------------------
def test_add_category_query(catlist, category):
    """Test that query inserts into DB."""
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 1
    catlist.execute = MagicMock(return_value=mock_cursor)

    catlist.add_category(category)

    query = catlist.execute.call_args.args[0]
    assert "INSERT INTO category" in query
    assert "category_name" in query

def test_add_category_return(catlist, category):
    """Test that add_category returns category with new id"""
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 1
    catlist.execute = MagicMock(return_value=mock_cursor)

    result = catlist.add_category(category)
    assert result.id == 1
    assert result.name == 'school'
    assert result.color == 'yellow'
#---------------------------------------------------------------------------------
# __DELETE FROM DB__
#---------------------------------------------------------------------------------
def test_delete_category_query(catlist):
    """Test that query deletes row from DB."""
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1
    catlist.execute = MagicMock(return_value=mock_cursor)
    catlist._ordered_ids = MagicMock(return_value=[1])

    catlist.delete_category(1)

    query = catlist.execute.call_args.args[0]
    assert "DELETE FROM category" in query

def test_non_existent_id(catlist):
    """Test that error is raised when id doesn't exist."""
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0
    catlist.execute = MagicMock(return_value=mock_cursor)
    catlist._ordered_ids = MagicMock(return_value=[1])

    with pytest.raises(ValueError):
        catlist.delete_category(999)
#---------------------------------------------------------------------------------
# __GRAB FROM DB__
#---------------------------------------------------------------------------------
def test_grab_category_query(catlist):
    """Test that query selects specific row"""
    catlist.grab_category(1)

    query = catlist.execute.call_args.args[0]
    assert query == "SELECT * FROM category WHERE category_id = ?"

def test_grab_category_return(catlist):
    """Test grab category return value"""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1, 'school', 'yellow')
    catlist.execute = MagicMock(return_value=mock_cursor)

    result = catlist.grab_category(1)
    assert result == (1, 'school', 'yellow')

def test_grab_non_existent_id(catlist):
    """Test that error is raised when id doesn't exist"""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    catlist.execute = MagicMock(return_value=mock_cursor)
    
    with pytest.raises(ValueError):
        catlist.grab_category(999)
#---------------------------------------------------------------------------------
# __CLOSE CONNECTION__
#---------------------------------------------------------------------------------
def test_close_connection(catlist):
    """Test that close function closes connection to db"""
    mock_conn = MagicMock()
    catlist.connection = mock_conn

    catlist.close()

    mock_conn.close.assert_called_once()
