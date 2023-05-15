import pytest
from court.models import Court
from decimal import Decimal
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestCourtModel:

    @pytest.fixture
    def court(self):
        court = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                     city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
        return court

    def test_get_instance(self, court):
        court_in_db = Court.objects.get(pk=court.pk)
        assert court_in_db == court

    def test_create_court_with_existing_id(self, court):
        with pytest.raises(IntegrityError):
            Court.objects.create(courtID=1, x=Decimal('11'), y=Decimal('22'),
                                 city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)

    def test_create_valid_court(self):
        Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                             city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30).full_clean()

    def test_create_three_courts_without_id(self):
        court1 = Court.objects.create(x=Decimal('11'), y=Decimal('22'),
                                      city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=30)
        court2 = Court.objects.create(x=Decimal('22'), y=Decimal('33'),
                                      city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=40)
        court3 = Court.objects.create(x=Decimal('33'), y=Decimal('44'),
                                      city='TEST_CITY', neighborhood='TEST_NEIGHBORHOOD', max_players=50)
        first_id = court1.courtID
        assert court1.courtID == first_id
        assert court2.courtID == first_id+1
        assert court3.courtID == first_id+2

    def test_create_court_with_negative_max_players(self):
        with pytest.raises(IntegrityError):
            Court.objects.create(
                x=Decimal('11'),
                y=Decimal('22'),
                city='TEST_CITY',
                neighborhood='TEST_NEIGHBORHOOD',
                max_players=-100
            )

    def test_create_court_with_big_name(self):
        with pytest.raises(ValidationError):
            Court.objects.create(
                x=Decimal('11'),
                y=Decimal('22'),
                city='A' * 63,
                neighborhood='TEST_NEIGHBORHOOD',
                max_players=10
            ).full_clean()

    def test_update_max_players(self, court):
        new_court = court
        assert new_court.max_players != 20
        new_court.max_players = 20
        new_court.save()
        updated_court = Court.objects.get(pk=new_court.pk)
        assert updated_court.max_players == 20

    def test_update_city(self, court):
        new_court = court
        assert new_court.city != 'Hogwarts'
        new_court.city = 'Hogwarts'
        new_court.save()
        updated_court = Court.objects.get(pk=new_court.pk)
        assert updated_court.city == 'Hogwarts'
        assert new_court.courtID == court.courtID

    def test_delete_court(self, court):
        test_court = court
        assert test_court.courtID == Court.objects.get(pk=test_court.pk).courtID

        test_court.delete()
        with pytest.raises(Court.DoesNotExist):
            Court.objects.get(pk=court.pk)

    def test_court_without_x(self):
        with pytest.raises(IntegrityError):
            Court.objects.create(
                y=Decimal('1'),
                city='TEST_CITY',
                neighborhood='TEST_NEIGHBORHOOD',
                max_players=10
            )

    def test_court_without_y(self):
        with pytest.raises(IntegrityError):
            Court.objects.create(
                x=Decimal('1'),
                city='TEST_CITY',
                neighborhood='TEST_NEIGHBORHOOD',
                max_players=10
            )

    def test_court_without_city(self):
        with pytest.raises(ValidationError):
            Court.objects.create(
                x=Decimal('1'),
                y=Decimal('1'),
                neighborhood='TEST_NEIGHBORHOOD',
                max_players=10
            ).full_clean()

    def test_court_without_neighborhood(self):
        with pytest.raises(ValidationError):
            Court.objects.create(
                x=Decimal('1'),
                y=Decimal('1'),
                city='TEST_CITY',
                max_players=10
            ).full_clean()

    def test_court_without_max_players(self):
        with pytest.raises(IntegrityError):
            Court.objects.create(
                x=Decimal('1'),
                y=Decimal('1'),
                city='TEST_CITY',
                neighborhood='TEST_NEIGHBORHOOD'
            )
