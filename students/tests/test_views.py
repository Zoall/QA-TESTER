import pytest
from django.urls import reverse
from students.models import Student


@pytest.mark.django_db
def test_create_student(client):
    response = client.post(reverse('student_create'), {
        'name': 'Test Student',
        'age': 20
    })
    assert response.status_code == 302  # Ensure it redirects
    assert Student.objects.filter(name='Test Student').exists()


@pytest.mark.django_db
def test_student_list_view(client):
    student1 = Student.objects.create(name='Alice', age=21)
    student2 = Student.objects.create(name='Bob', age=22)

    response = client.get(reverse('student_list'))
    assert response.status_code == 200
    assert b'Alice' in response.content
    assert b'Bob' in response.content


@pytest.mark.django_db
def test_update_student(client):
    student = Student.objects.create(name='Old Name', age=18)
    response = client.post(reverse('student_update', args=[student.student_id]), {  # Use student_id here
        'name': 'New Name',
        'age': 19
    })
    assert response.status_code == 302  # Ensure it redirects after update
    student.refresh_from_db()
    assert student.name == 'New Name'
    assert student.age == 19


@pytest.mark.django_db
def test_delete_student(client):
    student = Student.objects.create(name='Delete Me', age=23)
    response = client.post(reverse('student_delete', args=[
                           student.student_id]))  # Use student_id here
    assert response.status_code == 302  # Ensure it redirects after deletion
    assert not Student.objects.filter(
        student_id=student.student_id).exists()  # Use student_id here
