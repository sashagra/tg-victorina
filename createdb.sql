create table users(
    id integer primary key,
    firstname varchar(255),
    lastname varchar(255),
    login varchar(255),
    phone varchar(255)
);

create table questions(
    id integer primary key,
    question_text varchar(max)
    day date
);

create table answers(
    id varchar(255) primary key,
    answer_text varchar(255),
    question_id integer
    is_right boolean
    FOREIGN KEY(question_id) REFERENCES questions(id)

);

create table user_answers(
    id integer primary key,
    user_id integer,
    answer varchar(255),
    answered datetime
    FOREIGN KEY(user_id) REFERENCES users(id)
);


-- insert into category (codename, name, is_base_expense, aliases)
-- values
--     ("products", "продукты", true, "еда"),
--     ("coffee", "кофе", true, ""),
--     ("dinner", "обед", true, "столовая, ланч, бизнес-ланч, бизнес ланч"),
--     ("cafe", "кафе", true, "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
--     ("transport", "общ. транспорт", false, "метро, автобус, metro"),
--     ("taxi", "такси", false, "яндекс такси, yandex taxi"),
--     ("phone", "телефон", false, "теле2, связь"),
--     ("books", "книги", false, "литература, литра, лит-ра"),
--     ("internet", "интернет", false, "инет, inet"),
--     ("subscriptions", "подписки", false, "подписка"),
--     ("other", "прочее", true, "");

-- insert into budget(codename, daily_limit) values ('base', 500);