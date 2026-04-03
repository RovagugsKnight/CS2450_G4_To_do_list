import pytest
from unittest.mock import MagicMock
from src.controller.category_controller import CategoryController
from src.models.category import Category

@pytest.fixture
def repo():
    fake_repo = MagicMock()
    fake_repo.add_category = MagicMock(return_value="category")
    fake_repo.load_categories = MagicMock(return_value=[(1,"School","yellow")])
    fake_repo.delete_categories = MagicMock()
    fake_repo.grab_category = MagicMock(return_value=(1,"School","yellow"))
    return fake_repo

@pytest.fixture
def controller(repo):
    return CategoryController(repo)

#---------------------------------------------------------------------------------
# __ADD CATEGORY__
#---------------------------------------------------------------------------------
def test_add_category_calls_repo(controller, repo):
    """Test call to repository"""
    controller.add_category("Work", "green")
    (cat,) = repo.add_category.call_args.args
    repo.add_category.assert_called_once()
    assert cat.id == None
    assert cat.name == "Work"
    assert cat.color == "green"

def test_add_category_success_return(controller):
    """Test return value on add category success"""
    result = controller.add_category("Work", "green")
    assert result.success == True
    assert result.return_val == "category"
    
def test_add_category_failure_return(controller, repo):
    """Test return value on ValueError"""
    repo.add_category.side_effect = ValueError("invalid category")
    result = controller.add_category("","")
    repo.add_category.assert_not_called()
    assert result.success == False
    assert result.error

def test_add_category_name_not_str(controller):
    """Test error raised with a non string name"""
    with pytest.raises(TypeError):
        controller.add_category(1, 'blue')

def test_add_category_color_not_str(controller):
    """Test error raised with a non string color"""
    with pytest.raises(TypeError):
        controller.add_category('Work', 1)
#---------------------------------------------------------------------------------
# __LOAD CATEGORY__
#---------------------------------------------------------------------------------
def test_load_categories_repo_call(controller, repo):
    """Test call to repository"""
    controller.load_categories()
    repo.load_categories.assert_called_once()
    
def test_load_categories_return(controller):
    """Test return value of load categories"""
    categories = controller.load_categories()
    assert categories[0].id == 1
    assert categories[0].name == "School"
    assert categories[0].color == "yellow"
#---------------------------------------------------------------------------------
# __DELETE CATEGORY__
#---------------------------------------------------------------------------------
def test_delete_category_repo_call(controller, repo):
    """Test call to repository"""
    controller.delete_category(1)
    repo.delete_category.assert_called_once_with(1)

def test_delete_category_success(controller):
    """Test return value of delete category"""
    result = controller.delete_category(1)
    assert result.success == True

def test_delete_category_neg_val(controller):
    """Test error raised with negative id"""
    with pytest.raises(ValueError):
        controller.delete_category(-1)

def test_delete_category_non_num(controller):
    """Test error raised with non numeric id"""
    with pytest.raises(TypeError):
        controller.delete_category('1')
#---------------------------------------------------------------------------------
# __GET CATEGORY__
#---------------------------------------------------------------------------------
def test_get_category_repo_call(controller, repo):
    """Test call to repository"""
    controller.get_category(1)
    repo.grab_category.assert_called_once_with(1)

def test_get_category_success(controller):
    """Test return value of get category"""
    result = controller.get_category(1)
    category = result.return_val
    assert result.success == True
    assert category.id == 1
    assert category.name == "School"
    assert category.color == "yellow"

def test_get_category_neg_val(controller):
    """Test errorr raised with negative id"""
    with pytest.raises(ValueError):
        controller.delete_category(-1)

def test_get_category_non_num(controller):
    """Test error raised with non numeric id"""
    with pytest.raises(TypeError):
        controller.delete_category('1')


