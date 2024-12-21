create table if not exists feedback (
    id bigserial,
    title TEXT NOT NULL,
    text TEXT NOT NULL,
    comment_id bigint not null UNIQUE,
    grade int not null,
    is_new boolean not null default true,
    is_quailfied boolean not null default false,
    feedback_type integer,
    is_finance boolean,
    subcategory_type integer,
    created_at timestamptz not null default NOW(),
    updated_at timestamptz not null default NOW()
);

create type feedback_type as (
    title text,
    text text,
    comment_id int,
    grade int
);
