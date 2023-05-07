from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

engine = create_engine('sqlite:///sqlite_python.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class LibraryStorage(BaseModel):
    __tablename__ = 'LibraryStorage'
    name = Column(String(16), nullable=False)
    count = Column(Integer, nullable=False, default=1)
    release_date = Column(DateTime, nullable=False)
    author_id = Column(Integer, nullable=False)


class Authors(BaseModel):
    __tablename__ = 'Authors'
    name = Column(String(16), nullable=False)
    surname = Column(String(16), nullable=False)


class Readers(BaseModel):
    __tablename__ = 'Readers'
    name = Column(String(16), nullable=False)
    surname = Column(String(16), nullable=False)
    phone = Column(String(11), nullable=False)
    email = Column(String(16), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    # - получить список студентов, которые живут в общежитии;
    def get_students_scholarship(cls):
        return session.query(Readers).filter(Readers.scholarship == True).all()

    @classmethod
    # - получить список студентов, у которых средний балл выше, чем тот балл, который будет передан входным параметром в функцию.
    def get_students_score(cls, score):
        return session.query(Readers).filter(Readers.average_score >= score).all()


class IssuedBooks(BaseModel):
    __tablename__ = 'IssuedBooks'
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    data_of_issue = Column(DateTime, nullable=False)
    data_of_return = Column(DateTime)

    def hybrid_property(self):
        if self.data_of_return:
            return self.data_of_return - self.data_of_issue
        return self.data_of_return - datetime.now()


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


# - получить все книги в библиотеке (GET);
@app.route('/all_books', methods=['GET'])
def get_all_books_in_library():
    books = session.query(LibraryStorage).all()
    books_list = []
    for i_book in books:
        book_as_dict = books.to_json()
        books_list.append(book_as_dict)
    return jsonify(books_list=books_list), 200


# - получить список должников, которые держат книги у себя более 14 дней (GET);
@app.route('/all_books', methods=['GET'])
def debtors():
    debtors = session.query(IssuedBooks).filter(
        IssuedBooks.data_of_return - IssuedBooks.data_of_issue > data(0, 0, 14)).all()
    debtors_id = []
    debtors_list = []

    for i_debtor in debtors:
        debtor_as_id = debtors.to_json()
        debtors_id.append(debtor_as_id)

    for i_debtors in debtors_id:
        debtor = session.query(Readers.id, Readers.name, Readers.surname).filter(Readers.id == i_debtors[student_id]).all()
        debtors_list.append(debtor)

    if len(debtors_list) > 0:
        return jsonify(debtors_list=debtors_list), 200
    return f'Все книги зданы вовремя!'


# - выдать книгу студенту (POST — входные параметры ID книги и ID студента);
@app.route('/issue_books', methods=['POST'])
def issue_books():
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('student_id', type=int)
    data_of_issue: datetime = datetime.now()
    data_of_return: datetime = datetime.now() + data(0, 0, 14)
    issue_book = IssuedBooks(book_id=book_id, student_id=student_id, data_of_issue=data_of_issue, data_of_return=data_of_return)
    session.add(issue_book)
    session.commit()
    return f'Книга выдана читателю!'


# сдать книгу в библиотеку (POST — входные параметры ID книги
# и ID студента, если такой связки нет, выдать ошибку).
@app.route('/issue_books', methods=['POST'])
def return_book():
    book_id = request.form.get('book_id', type=int)
    student_id = request.form.get('book_id', type=int)

    try:
        archive_entry = session.query(IssuedBooks).filter(
            IssuedBooks.book_id == book_id and IssuedBooks.student_id == student_id).one()
        archive_entry.data_of_return = datetime.now()
        return 'Вы успешно сдали книгу!'
    except NoResultFound:
        return f'Проверте коректность введенных данных!'


if __name__ == '__main__':
   app.run()