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
CPU	\N	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	\N
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: heinmin2maw
--

COPY public."user" (name, email, address, hashed_password, image_url, user_type, user_level, total_spent, is_active, is_superuser, is_verified, verified_at, id, sa_orm_sentinel, created_at, updated_at) FROM stdin;
swan	adminswan@gmail.com	\N	$argon2id$v=19$m=65536,t=3,p=4$NYZQ6t1bizFGiDEmZIzx3g$7PEJXTd+rR4vV42aGQGrcitmgQ/0yXXYfrli1rF2d8o	\N	ADMIN	CLASSIC	0.00	t	t	f	\N	bee49ca0-cb1d-4cb4-9f3b-a3eeb16258cb	\N	2024-11-12 08:58:14.2812+00	2024-11-12 08:58:14.281204+00
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
CPU1	Testing	500.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	5	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	6aa78709-8cab-471a-9aa2-0d39e97f744f	\N
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
Intel	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	333fc789-2534-4040-b669-98ec9d65c183	\N
AMD	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	8af6f52a-52dd-4724-842a-1f27a62a1488	\N
\.


--
-- PostgreSQL database dump complete
--

