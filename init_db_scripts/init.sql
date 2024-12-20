create table if not exists feedback (
id bigserial,
title TEXT NOT NULL,
text TEXT NOT NULL,
comment_id bigint UNIQUE,
grade int
);

create type feedback_type as (
title text,
text text,
comment_id int,
grade int);