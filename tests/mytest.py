import pytest

# 하나의 테스트를 다른 인자들로 반복.
@pytest.mark.parametrize('x,y,res',[(3,2,5),
                                    (1,2,3),
                                    (2,4,5)])
def test_add(x,y,res):
    print('testing...')
    sum = add(x,y)
    assert sum==res

## 여러 테스트에 필요한 반복요소를 미리 작성하여 인자로 넘긴다.
# @pytest.fixture
# def functionX():
#     return objectX


# def test_function1(functionX):
#     assert something.sumthing

# def test_function2(functionX):
#     assert something.sumthing
