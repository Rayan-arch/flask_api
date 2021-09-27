import requests

def test_get_books():
    responce = requests.get('http://localhost:5000/books')
    assert responce.status_code == 200

def test_add_book():
    # given
    payload = {
        'title': 'Calineczka',
        'author_id': 1,
        'description': 'Najmniejsza kobieta na świecie i jej przygody w ogrodzie.'
    }
    # when
    responce = requests.post('http://localhost:5000/books/add', json=payload)
    # then
    assert responce.status_code == 201
    responce = requests.get('http://localhost:5000/books')
    data = responce.json()
    assert data[-1]['title'] == 'Calineczka'
    assert data[-1]['author_id'] == 1

def test_delete_book():
    # given
    responce = requests.get('http://localhost:5000/books')
    data = responce.json()
    count_old = len(data)
    book_id= data[-1]['id']
    # when
    responce = requests.delete(f'http://localhost:5000/books/{book_id}')
    # then
    assert responce.status_code == 200

    responce = requests.get('http://localhost:5000/books')
    data = responce.json()
    count_new = len(data)
    assert count_new + 1 == count_old