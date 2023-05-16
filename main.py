from sqlalchemy import Column, Integer, Float, String, Boolean, Date, \
    ForeignKey, DateTime, create_engine, func, desc
from sqlalchemy.orm import relationship, sessionmaker, backref, joinedload
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, date
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

engine = create_engine('sqlite:///sqlite_python.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    # таблица авторов
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)

    def __repr__(self):
        return self.name + ' ' + self.surname


class Book(Base):
    # таблица книг
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship("Author", backref=backref("books",
                                                    cascade="all, "
                                                            "delete-orphan",
                                                    lazy="select"))

    students = relationship('ReceivingBook', back_populates='book')


class Student(Base):
    # таблица читателей-студентов
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    books = relationship('ReceivingBook', back_populates='student')

    @classmethod
    # - получить список студентов, которые живут в общежитии;
    def get_students_scholarship(cls):
        return session.query(Readers).filter(Readers.scholarship == True).all()

    @classmethod
    # - получить список студентов, у которых средний балл выше, чем тот балл, который будет передан входным параметром в функцию.
    def get_students_score(cls, score):
        return session.query(Readers).filter(Readers.average_score >= score).all()


class ReceivingBook(Base):
    # таблица выдачи книг студентам
    __tablename__ = 'receiving_books'

    book_id = Column(Integer, ForeignKey('books.id'),
                     primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'),
                        primary_key=True)

    date_of_issue = Column(DateTime, default=datetime.now)
    date_of_finish = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="books")
    book = relationship("Book", back_populates="students")

    def hybrid_property(self):
        if self.data_of_return:
            return self.data_of_return - self.data_of_issue
        return self.data_of_return - datetime.now()


def insert_data():
    authors = [Author(name="Александр", surname="Пушкин"),
               Author(name="Лев", surname="Толстой"),
               Author(name="Михаил", surname="Булгаков"),
               ]
    authors[0].books.extend([Book(name="Капитанская дочка",
                                  count=5,
                                  release_date=date(1836, 1, 1)),
                             Book(name="Евгений Онегин",
                                  count=3,
                                  release_date=date(1838, 1, 1))
                             ])
    authors[1].books.extend([Book(name="Война и мир",
                                  count=10,
                                  release_date=date(1867, 1, 1)),
                             Book(name="Анна Каренина",
                                  count=7,
                                  release_date=date(1877, 1, 1))
                             ])
    authors[2].books.extend([Book(name="Морфий",
                                  count=5,
                                  release_date=date(1926, 1, 1)),
                             Book(name="Собачье сердце",
                                  count=3,
                                  release_date=date(1925, 1, 1))
                             ])

    students = [Student(name="Nik", surname="1", phone="2", email="3",
                        average_score=4.5,
                        scholarship=True),
                Student(name="Vlad", surname="1", phone="2", email="3",
                        average_score=4,
                        scholarship=True),
                Student(name="Alex", surname="1", phone="2", email="3",
                        average_score=3,
                        scholarship=False),
                ]
    session.add_all(authors)
    session.add_all(students)
    session.commit()


def give_me_book():
    nikita = session.query(Student).filter(Student.name == 'Nik').one()
    vlad = session.query(Student).filter(Student.name == 'Vlad').one()
    books_to_nik = session.query(Book).filter(Author.surname == 'Толстой',
                                              Author.id == Book.author_id).all()
    books_to_vlad = session.query(Book).filter(Book.id.in_([1, 3, 4])).all()

    for book in books_to_nik:
        receiving_book = ReceivingBook()
        receiving_book.book = book
        receiving_book.student = nikita
        session.add(receiving_book)

    for book in books_to_vlad:
        receiving_book = ReceivingBook()
        receiving_book.book = book
        receiving_book.student = vlad
        session.add(receiving_book)

    session.commit()


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route('/books_by_the_author_ib/<int:id>', methods=['GET'])
def books_by_the_author_ib(id):
    count_books_by_authors = session.query(func.sum(Book.count), Book.author_id). \
        filter(Book.author_id == id).all()[0][0]
    return f'{count_books_by_authors}'


@app.route('/top_ten_reading_students', methods=['GET'])
def top_ten_reading_students():
    # Топ 10 студентов за год, читающих книги (id студента - колличество прочитанных книг за год)
    top_reading_students = reading_student('2023', 0)

    top_reading_students.sort(key=lambda x: x[1])
    top_reading_students.reverse()
    top_reading_students = top_reading_students[:10]

    # Топ 10 студентов за год, читающих книги (имена)
    answer = ''
    for i in top_reading_students:
        answer = f'{answer} {session.query(Student.name).filter(Student.id == i[0]).first()[0]}'
    return answer


@app.route('/top_reading_books', methods=['GET'])
def top_books():
    # Топ самых читаемых книг (индекс книги - колличество раз взятия из библиотеки)
    top_books = []
    count_records = session.query(func.count(Book.id)).scalar()

    for i in range(1, count_records + 1):
        print(i)
        top_books.append(session.query(Book.id).filter_by(id=i).scalar())
        top_books.append(session.query(func.count(ReceivingBook.book_id)).filter(ReceivingBook.book_id == i).scalar())

        if top_books[-1] == 0:
            top_books.pop(-1)
            top_books.pop(-1)

    # Топ книг по названиям
    answer = ''
    for i in range(len(top_books) - 2, -1, -2):
        answer = f'{answer} {session.query(Book.name).filter(Book.id == top_books[i]).all()[0][0]}'
    print(answer)


@app.route('/reading_student_pre_month', methods=['GET'])
def reading_student_pre_month():
    # Среднее кол-во прочитанных книг студентом за месяц
    reading_students_per_month = reading_student('05', 1)
    count_reading_books_pre_month = 0
    for i in range(len(reading_students_per_month)):
        count_reading_books_pre_month += reading_students_per_month[i][1]
    return f'В среднем, 1 студент прочитал книг за месяц: ' \
           f'{count_reading_books_pre_month / len(reading_students_per_month)}'


def reading_student(sort_date, i_date):
    # Cтуденты читающие книги за временной интервал (id студента; колличество прочитанных книг за ...)
    count_student = session.query(func.count(Student.id)).scalar()
    reading_students = []

    for i in range(1, count_student + 1):
        count_reading_books_by_the_student = len(session.query(Student.id).filter(Student.id == i, Student.books).all())

        if count_reading_books_by_the_student != 0:

            year = session.query(ReceivingBook.date_of_issue).filter(ReceivingBook.student_id == i).all()
            for j in range(len(year)):
                check_year = session.query(True).filter(ReceivingBook.student_id == i,
                                                        str(year[j][0]).split('-')[i_date] == sort_date).all()

            # print(f'\nИндекс студента [{i}] - брал книгу(и) в 2023 году')
            # print(check_year, end="\n\n")

            count_books = 0
            for j in check_year:
                if j[0]:
                    count_books += 1
            reading_students.append((i, count_books))
    return reading_students


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    check_exist = session.query(Author).all()
    if not check_exist:
        insert_data()
        give_me_book()
    app.run