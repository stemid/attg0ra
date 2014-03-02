CREATE TABLE todo (
    id integer NOT NULL,
    data text NOT NULL
);

CREATE SEQUENCE items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE items_id_seq OWNED BY todo.id;
ALTER TABLE ONLY todo ALTER COLUMN id SET DEFAULT nextval('items_id_seq'::regclass);

ALTER TABLE ONLY todo
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);
