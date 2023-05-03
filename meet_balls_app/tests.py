import pytest


class TestUi:

    def test_home_page_extends_base(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'<nav' in response.content
        assert b'Login' in response.content

    @pytest.mark.django_db
    def test_logged_user_see_logout_in_navbar(self, client, player):
        client.force_login(player.user)
        response = client.get('/')
        assert response.status_code == 200
        assert b'<nav' in response.content
        assert b'Logout' in response.content
