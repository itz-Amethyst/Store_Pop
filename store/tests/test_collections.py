from rest_framework import status
import pytest

@pytest.fixture
def create_collection(api_client):
    def do_create_collection(collection):
        return api_client.post('/store/collection/', collection)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    @pytest.mark.skip # Will skip the test
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Arrange

        # Act
        response = create_collection({'title': 'a'})

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403( self, authenticate, create_collection):

        authenticate()
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_return_400( self, authenticate, create_collection ):

        authenticate(is_staff = True)
        response = create_collection({"title": ''})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_return_201( self, authenticate, create_collection ):
        authenticate(is_staff = True)
        response = create_collection({'title': 'a'})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

# ptw python test watch command

