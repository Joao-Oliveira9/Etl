-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.tb_aluno
(
    aluno_id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    nome character varying(255) COLLATE pg_catalog."default" NOT NULL,
    updated_at timestamp(6) without time zone,
    curso_id uuid NOT NULL,
    matricula_id uuid NOT NULL,
    CONSTRAINT tb_aluno_pkey PRIMARY KEY (aluno_id),
    CONSTRAINT uk6qm83mo05oc3cvtt363xdyj8i UNIQUE (matricula_id)
);

CREATE TABLE IF NOT EXISTS public.tb_aluno_disciplina
(
    id uuid NOT NULL,
    nota real,
    aluno_id uuid,
    disciplina_id uuid,
    CONSTRAINT tb_aluno_disciplina_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.tb_curso
(
    id_curso uuid NOT NULL,
    nome character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    CONSTRAINT tb_curso_pkey PRIMARY KEY (id_curso),
    CONSTRAINT ukeeqdia4j9kbt06r928dqw72ai UNIQUE (nome)
);

CREATE TABLE IF NOT EXISTS public.tb_curso_disciplina
(
    curso_id uuid NOT NULL,
    disciplina_id uuid NOT NULL,
    CONSTRAINT tb_curso_disciplina_pkey PRIMARY KEY (curso_id, disciplina_id)
);

CREATE TABLE IF NOT EXISTS public.tb_disciplina
(
    id uuid NOT NULL,
    nome character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(6) without time zone,
    updated_at timestamp(6) without time zone,
    CONSTRAINT tb_disciplina_pkey PRIMARY KEY (id),
    CONSTRAINT ukh2kwc5wv58l0dvthqwofpullv UNIQUE (nome)
);

CREATE TABLE IF NOT EXISTS public.tb_documento_matricula
(
    id uuid NOT NULL,
    created_at timestamp(6) without time zone,
    numero_documento integer NOT NULL,
    updated_at timestamp(6) without time zone,
    CONSTRAINT tb_documento_matricula_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.tb_aluno
    ADD CONSTRAINT fkb8vtie9hke28gaidoqeq8cwx3 FOREIGN KEY (curso_id)
    REFERENCES public.tb_curso (id_curso) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.tb_aluno
    ADD CONSTRAINT fklyvvifwm5irqvuqo0j2alleu7 FOREIGN KEY (matricula_id)
    REFERENCES public.tb_documento_matricula (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS uk6qm83mo05oc3cvtt363xdyj8i
    ON public.tb_aluno(matricula_id);


ALTER TABLE IF EXISTS public.tb_aluno_disciplina
    ADD CONSTRAINT fkgdm6lth0nl66k446f50igrvow FOREIGN KEY (aluno_id)
    REFERENCES public.tb_aluno (aluno_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.tb_aluno_disciplina
    ADD CONSTRAINT fkjg1a3j9trhylk1xn4micadftm FOREIGN KEY (disciplina_id)
    REFERENCES public.tb_disciplina (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.tb_curso_disciplina
    ADD CONSTRAINT fkber569xlcq5il3ldc8u3q4gad FOREIGN KEY (disciplina_id)
    REFERENCES public.tb_disciplina (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.tb_curso_disciplina
    ADD CONSTRAINT fkdsrug7qpvg38uwxqx1jbprmbk FOREIGN KEY (curso_id)
    REFERENCES public.tb_curso (id_curso) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;