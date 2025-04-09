import pytest
from django.urls import reverse
from students.models import Student


@pytest.mark.django_db
def test_create_student(client):
    response = client.post(reverse('student_create'), {
        'name': 'Test Student',
        'age': 20
    })
    assert response.status_code == 302
    assert Student.objects.filter(name='Test Student').exists()


@pytest.mark.django_db
def test_create_student_missing_fields(client):
    # Missing age
    response = client.post(reverse('student_create'), {
        'name': 'Incomplete'
    })
    assert response.status_code == 200  # Form should return with errors
    assert not Student.objects.filter(name='Incomplete').exists()

@pytest.mark.django_db
def test_create_duplicate_student(client):
    Student.objects.create(name='Duplicate', age=20)
    response = client.post(reverse('student_create'), {
        'name': 'Duplicate',
        'age': 21
    })
    # Depending on how your model handles it (e.g., unique constraints), adjust this
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_student_list_view(client):
    Student.objects.create(name='Alice', age=21)
    Student.objects.create(name='Bob', age=22)
    response = client.get(reverse('student_list'))
    assert response.status_code == 200
    assert b'Alice' in response.content
    assert b'Bob' in response.content


@pytest.mark.django_db
def test_update_student(client):
    student = Student.objects.create(name='Old Name', age=18)
    response = client.post(reverse('student_update', args=[student.student_id]), {
        'name': 'New Name',
        'age': 19
    })
    assert response.status_code == 302
    student.refresh_from_db()
    assert student.name == 'New Name'
    assert student.age == 19


@pytest.mark.django_db
def test_update_student_invalid_data(client):
    student = Student.objects.create(name='Old Name', age=18)
    response = client.post(reverse('student_update', args=[student.student_id]), {
        'name': '',
        'age': 'not a number'
    })
    assert response.status_code == 200
    student.refresh_from_db()
    assert student.name == 'Old Name'


@pytest.mark.django_db
def test_delete_student(client):
    student = Student.objects.create(name='Delete Me', age=23)
    response = client.post(
        reverse('student_delete', args=[student.student_id]))
    assert response.status_code == 302
    assert not Student.objects.filter(student_id=student.student_id).exists()


@pytest.mark.django_db
def test_get_delete_should_not_work(client):
    student = Student.objects.create(name='No GET Delete', age=24)
    response = client.get(reverse('student_delete', args=[student.student_id]))
    # Typically should not allow GET to delete
    assert response.status_code in [405, 200]
    assert Student.objects.filter(student_id=student.student_id).exists()


@pytest.mark.django_db
def test_create_student_extreme_age(client):
    response = client.post(reverse('student_create'), {
        'name': 'Too Old',
        'age': 150
    })
    assert response.status_code in [200, 302]
    # Adjust according to model validation; if valid:
    assert Student.objects.filter(name='Too Old').exists()


@pytest.mark.django_db
def test_create_student_empty_name(client):
    response = client.post(reverse('student_create'), {
        'name': '',
        'age': 25
    })
    assert response.status_code == 200
    assert not Student.objects.filter(age=25).exists()
