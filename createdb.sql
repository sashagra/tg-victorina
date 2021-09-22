create table users(
    id integer primary key,
    firstname varchar(255),
    lastname varchar(255),
    login varchar(255),
    phone varchar(255)
);

create table questions(
    id integer primary key,
    question_text text,
    day date
);

create table answers(
    id integer primary key,
    answer_text varchar(255),
    question_id integer,
    is_right boolean,
    FOREIGN KEY(question_id) REFERENCES questions(id)

);

create table user_answers(
    id integer primary key,
    user_id integer,
    question_id integer,
    answers varchar(255),
    answered datetime,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(question_id) REFERENCES questions(id),
    FOREIGN KEY(answer_id) REFERENCES answers(id)
);
