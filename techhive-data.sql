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
Motherboard	\N	da4be9a4-891d-439a-ade4-aa719f92fe69	\N
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
AMD Ryzen 5	A mid-range processor with up to 6 cores and 12 threads, built on the Zen architecture. Ryzen 5 processors are considered to be some of the fastest available, and are good for gaming and other intense workloads.	540.00	4.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	20	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	2e2a77d5-2681-47b4-b483-bf9b11a81997	\N
Ryzen 9 7950X	High-end performance for gaming, content creation, and multitasking. Suitable for enthusiasts, professional video editors, and software developers who require high computing power.	750.00	20.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	34	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	c6a69c77-e7a0-4b4f-9e64-cb28243d4a38	\N
Ryzen 7 7800X3D	Mid-to-high performance for gaming and productivity. Ideal for gamers and streamers who need strong multi-core performance.	550.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	52	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	fff9f15f-c93c-4fee-8572-bf8398e1bd94	\N
Ryzen Threadripper PRO 5995WX	High-performance CPUs for professional workloads like 3D rendering, simulations, video editing, and data analysis. Designed for workstations and high-performance desktops (HEDT).	6550.00	30.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	25	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	14bba65a-51a9-4d14-9f6f-bfdbb60bd95e	\N
Athlon 3000G	Budget-friendly processors for basic computing needs such as web browsing, office work, and light multimedia usage. Ideal for entry-level desktop systems or home office PCs	70.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	90	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	b233aa7e-a661-4a43-94d1-a19f3f105ab4	\N
Intel Core i9-13900K	High-end CPUs with up to 24 cores (8 Performance + 16 Efficiency), ideal for gaming, content creation, and multitasking.	690.00	10.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	45	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	2953a7d5-29a2-43d5-8819-1b66e6d93229	\N
Intel Core i7-13700K	Mid-range CPUs with up to 16 cores (8P + 8E), providing excellent performance for gaming and productivity tasks.	430.00	10.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	52	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	f8ed57bc-0d3f-42bd-8d45-dee92879c1ea	\N
Intel Core i5-13600K	Balanced CPUs with up to 14 cores (6P + 8E), offering great performance for gaming and everyday use at an affordable price.	300.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	99	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	0019496a-4f66-4b95-a6fb-4313f7bddc58	\N
Intel Xeon W-3400	Workstation and server CPUs with high core counts, designed for professional workloads like 3D rendering and data processing.	1000.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	20	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	b016cb69-f9d8-4cdd-9f36-dd2bae9bfd2d	\N
Intel Pentium Gold G7400	Budget-friendly, entry-level CPUs with 2 cores, suitable for basic tasks like web browsing and office applications.	80.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	50	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	222256e1-51ee-47dc-8371-dfdcd6bbd4ae	\N
Intel Pentium Gold G7400	Budget-friendly, entry-level CPUs with 2 cores, suitable for basic tasks like web browsing and office applications.	80.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	50	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	64cf37af-00fa-47a6-9293-c159c429728a	\N
Intel Pentium Gold G7400	Budget-friendly, entry-level CPUs with 2 cores, suitable for basic tasks like web browsing and office applications.	80.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	50	ef296e7a-7f6d-4b97-bd1f-ab881ba98ce4	349f3012-faf3-485a-b785-041e33876042	\N
ASUS ROG Strix Z790-E	High-end motherboard for Intel's 13th and 14th Gen CPUs, supports overclocking, PCIe 5.0, and DDR5 RAM.	550.00	20.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	10	da4be9a4-891d-439a-ade4-aa719f92fe69	4399e73f-3a21-41a7-8b9e-18e0ba250337	\N
MSI PRO B760M-A WiFi	Mid-range board for 13th/12th Gen CPUs, supports PCIe 4.0, great for gaming and productivity without overclocking.	220.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	2	da4be9a4-891d-439a-ade4-aa719f92fe69	ddc0dade-0582-434d-91f6-675600c075c7	\N
GIGABYTE H610M S2H	Entry-level motherboard for 12th/13th Gen CPUs, supports basic features like DDR4 RAM, good for budget builds.	80.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Intel	5	da4be9a4-891d-439a-ade4-aa719f92fe69	dd30fc2d-23da-4bd1-b969-ef69b7af7bd1	\N
H570 Motherboard	Mid-range board for 11th/10th Gen CPUs, supports PCIe 4.0 and Intel Optane Memory, suitable for light gaming and general use.	200.00	5.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Asus	10	da4be9a4-891d-439a-ade4-aa719f92fe69	1aa2097a-25b2-4c29-9513-6677f5af9bb5	\N
X299 Motherboard	High-performance motherboard for Intel Core X-series (HEDT) processors, ideal for workstations and content creators.	300.00	4.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	Asus	5	da4be9a4-891d-439a-ade4-aa719f92fe69	1a9eb66d-78aa-43d9-99cf-b1631327754a	\N
ASUS ROG Crosshair X670E Hero	High-end motherboard for Ryzen 7000 series (AM5), supports PCIe 5.0, DDR5 RAM, designed for overclocking and gaming enthusiasts.	650.00	5.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	45	da4be9a4-891d-439a-ade4-aa719f92fe69	4cf36231-34a3-4a22-a12d-6f9a860379e1	\N
MSI MPG B650 TOMAHAWK WiFi	Mid-range board for Ryzen 7000 series (AM5), offers PCIe 4.0 support, good for gaming and productivity builds.	300.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	5	da4be9a4-891d-439a-ade4-aa719f92fe69	7aa72cdc-b32e-4284-a8a8-54d1afe4126b	\N
ASUS TUF Gaming B550-PLUS	Popular mid-range motherboard for Ryzen 3000 and 5000 series (AM4), supports PCIe 4.0, suitable for mainstream gaming builds.	150.00	7.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	10	da4be9a4-891d-439a-ade4-aa719f92fe69	eaf36102-519d-4558-844f-b0b565cf4215	\N
GIGABYTE A520M S2H	Budget-friendly motherboard for Ryzen 3000 and 5000 series (AM4), lacks PCIe 4.0 but offers good basic features for everyday use.	60.00	0.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	10	da4be9a4-891d-439a-ade4-aa719f92fe69	33394290-6d7b-444b-9aa8-589847c22977	\N
ASRock X570 Phantom Gaming X	High-performance motherboard for Ryzen 3000 and 5000 series (AM4), supports PCIe 4.0 and advanced cooling features, ideal for enthusiasts.	400.00	5.00	images/f07f9df0-8262-44fc-a75a-6ba6c462ba3c_Screenshot 2024-08-02 114819.png	{}	AMD	10	da4be9a4-891d-439a-ade4-aa719f92fe69	e184a2a3-7fec-4234-ba40-f2553dc34d3a	\N
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
string	da4be9a4-891d-439a-ade4-aa719f92fe69	7429bf60-d1f6-4e83-aec8-740a14ec4366	\N
\.


--
-- PostgreSQL database dump complete
--

