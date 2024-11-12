--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Debian 17.0-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public.category (name, decription, id, sa_orm_sentinel) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public."user" (name, email, address, hashed_password, image_url, user_type, user_level, total_spent, is_active, is_superuser, is_verified, verified_at, id, sa_orm_sentinel, created_at, updated_at) FROM stdin;
admin	admin@gmail.com	\N	$argon2id$v=19$m=65536,t=3,p=4$eg9BSIlRilHKGSMkpPQ+Zw$a+WmIOx+9xyZ4A1a9PAytdzXVXkvH6i4NSgyDFqJPJ8	\N	ADMIN	CLASSIC	0.00	t	t	f	\N	1954fe2f-53ec-402e-b707-8f1097fd29b9	\N	2024-11-12 08:15:10.864226+00	2024-11-12 08:15:10.864229+00
\.


--
-- Data for Name: order; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public."order" (user_id, address, total_price, status, id, sa_orm_sentinel, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public.product (name, description, price, discount_percent, image_url, sub_image_url, brand, stock, category_id, id, sa_orm_sentinel) FROM stdin;
\.


--
-- Data for Name: order_product; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public.order_product (product_id, order_id, quantity, price_at_order, id, sa_orm_sentinel, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: product_review; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public.product_review (user_id, product_id, rating, review_text, id, sa_orm_sentinel, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: subcategory; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public.subcategory (name, category_id, id, sa_orm_sentinel) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

