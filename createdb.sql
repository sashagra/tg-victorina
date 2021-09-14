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
    id varchar(255) primary key,
    answer_text varchar(255),
    question_id integer,
    is_right boolean,
    FOREIGN KEY(question_id) REFERENCES questions(id)

);

create table user_answers(
    id integer primary key,
    user_id integer,
    answer varchar(255),
    answered datetime,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
