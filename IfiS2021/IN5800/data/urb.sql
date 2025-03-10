--
-- PostgreSQL database dump
--

-- Dumped from database version 11.10 (Debian 11.10-0+deb10u1)
-- Dumped by pg_dump version 11.10 (Debian 11.10-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY urbania.organization DROP CONSTRAINT IF EXISTS organization_offices_in_fkey;
ALTER TABLE IF EXISTS ONLY urbania.citizen DROP CONSTRAINT IF EXISTS citizen_works_at_fkey;
ALTER TABLE IF EXISTS ONLY urbania.citizen DROP CONSTRAINT IF EXISTS citizen_apartment_building_fkey;
ALTER TABLE IF EXISTS ONLY suburbia.citizen DROP CONSTRAINT IF EXISTS citizen_home_fkey;
ALTER TABLE IF EXISTS ONLY urbania.organization DROP CONSTRAINT IF EXISTS organization_pkey;
ALTER TABLE IF EXISTS ONLY urbania.citizen DROP CONSTRAINT IF EXISTS citizen_urb_id_key;
ALTER TABLE IF EXISTS ONLY urbania.citizen DROP CONSTRAINT IF EXISTS citizen_pkey;
ALTER TABLE IF EXISTS ONLY urbania.building DROP CONSTRAINT IF EXISTS building_pkey;
ALTER TABLE IF EXISTS ONLY suburbia.home DROP CONSTRAINT IF EXISTS home_pkey;
ALTER TABLE IF EXISTS ONLY suburbia.citizen DROP CONSTRAINT IF EXISTS citizen_urb_id_key;
ALTER TABLE IF EXISTS ONLY suburbia.citizen DROP CONSTRAINT IF EXISTS citizen_pkey;
ALTER TABLE IF EXISTS suburbia.home ALTER COLUMN hid DROP DEFAULT;
DROP TABLE IF EXISTS urbania.organization;
DROP TABLE IF EXISTS urbania.citizen;
DROP TABLE IF EXISTS urbania.building;
DROP SEQUENCE IF EXISTS suburbia.home_hid_seq;
DROP TABLE IF EXISTS suburbia.home;
DROP TABLE IF EXISTS suburbia.citizen;
DROP SCHEMA IF EXISTS urbania;
DROP SCHEMA IF EXISTS suburbia;
--
-- Name: suburbia; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA suburbia;


--
-- Name: urbania; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA urbania;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: citizen; Type: TABLE; Schema: suburbia; Owner: -
--

CREATE TABLE suburbia.citizen (
    cid integer NOT NULL,
    urb_id text,
    name text NOT NULL,
    home integer,
    occupation text
);


--
-- Name: home; Type: TABLE; Schema: suburbia; Owner: -
--

CREATE TABLE suburbia.home (
    hid integer NOT NULL,
    home_address text,
    zip_code text
);


--
-- Name: home_hid_seq; Type: SEQUENCE; Schema: suburbia; Owner: -
--

CREATE SEQUENCE suburbia.home_hid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: home_hid_seq; Type: SEQUENCE OWNED BY; Schema: suburbia; Owner: -
--

ALTER SEQUENCE suburbia.home_hid_seq OWNED BY suburbia.home.hid;


--
-- Name: building; Type: TABLE; Schema: urbania; Owner: -
--

CREATE TABLE urbania.building (
    bid integer NOT NULL,
    address text NOT NULL,
    zipcode text NOT NULL
);


--
-- Name: citizen; Type: TABLE; Schema: urbania; Owner: -
--

CREATE TABLE urbania.citizen (
    cid integer NOT NULL,
    urb_id text,
    name text NOT NULL,
    apartment_number integer NOT NULL,
    apartment_building integer,
    works_at integer
);


--
-- Name: organization; Type: TABLE; Schema: urbania; Owner: -
--

CREATE TABLE urbania.organization (
    oid integer NOT NULL,
    name text NOT NULL,
    offices_in integer
);


--
-- Name: home hid; Type: DEFAULT; Schema: suburbia; Owner: -
--

ALTER TABLE ONLY suburbia.home ALTER COLUMN hid SET DEFAULT nextval('suburbia.home_hid_seq'::regclass);


--
-- Data for Name: citizen; Type: TABLE DATA; Schema: suburbia; Owner: -
--

COPY suburbia.citizen (cid, urb_id, name, home, occupation) FROM stdin;
63	s63	Long Baker	83	pupil
140	s140	Yang Stad	76	pupil
173	s173	Fermina Trazin	27	student
2	s2	Peter Stad	40	pupil
32	s32	Pilka Potter	4	farmer
326	s326	Yun East	97	\N
333	s333	Juni Bass	56	fisher
215	s215	Yi Gupta	99	pupil
329	s329	Jing Huzza	69	student
315	s315	Kari Hassana	7	pupil
241	s241	Mundei Huldra	51	farmer
175	s175	Yang Winter	66	fisher
33	s33	Preben Bink	64	student
94	s94	Pinky Mouse	83	student
60	s60	Even Olive	82	student
346	s346	Mary Baker	100	fisher
142	s142	Ole Trazin	43	farmer
156	s156	Haleni King	34	student
187	s187	Gran Kong	83	fisher
89	s89	Yali Hang	72	pupil
146	s146	Prestani East	27	farmer
302	s302	Yulie Dun	33	\N
46	s46	Terry Olsen	29	farmer
273	s273	Collie Olive	4	fisher
220	s220	Che Gupta	64	fisher
256	s256	Okke Erl	83	student
75	s75	Din Trazin	64	student
14	s14	Mundei Stad	35	pupil
153	s153	Norri Spring	31	farmer
342	s342	Polentaz Stone	9	farmer
193	s193	Vali Yun	81	fisher
251	s251	Uri Gupta	54	farmer
57	s57	Mundei Wang	7	pupil
198	s198	Che Wang	27	farmer
229	s229	Odd Din	44	farmer
71	s71	Kari Green	64	farmer
292	s292	Okke Nilsen	29	fisher
26	s26	Yulie Baker	19	pupil
214	s214	Tarud Huldra	24	pupil
338	s338	Pinky Sky	66	student
161	s161	Humazana Quix	85	student
132	s132	Tams Hang	43	fisher
41	s41	Tams Bink	7	pupil
23	s23	Jens Wild	58	farmer
313	s313	Jan Hassana	94	farmer
344	s344	Yufrey Gupta	96	student
168	s168	Derek Yun	91	fisher
265	s265	Fermina Sky	56	farmer
197	s197	Jazzar Olsen	30	fisher
166	s166	Merv Asim	49	farmer
139	s139	Yi Hang	67	fisher
158	s158	Kolena Baker	23	student
136	s136	Gert Baker	5	pupil
135	s135	Sung Stone	96	farmer
217	s217	Prestani Wild	70	pupil
40	s40	Zenita Gupta	22	student
169	s169	Che Olive	40	fisher
15	s15	Nax Wand	37	\N
28	s28	Terry Bakken	15	fisher
248	s248	Hasselina Huldra	11	student
260	s260	Haleni Bakken	50	pupil
101	s101	Olelec Bear	33	pupil
210	s210	Gina Chang	94	fisher
131	s131	Hasselina Bing	1	pupil
165	s165	Vali Bear	46	student
199	s199	Connie West	75	pupil
280	s280	Larry Hassana	10	student
244	s244	Hux Seagull	57	student
72	s72	Okke Smith	51	fisher
267	s267	Anne Dun	99	farmer
68	s68	Nax Hang	94	student
255	s255	Yuel Olsen	3	pupil
330	s330	Olelec Wild	17	fisher
24	s24	Ida Wild	89	fisher
264	s264	Sulfre Hassana	38	farmer
48	s48	Olive Winter	85	pupil
152	s152	Vali Potter	29	pupil
261	s261	Mundei Oneda	23	fisher
108	s108	Pirilill King	83	\N
242	s242	Kolena Bass	65	farmer
52	s52	Hux Bear	21	\N
192	s192	Kolena Dun	72	student
39	s39	Lomer Erdu	49	farmer
163	s163	Xani Bakken	49	farmer
240	s240	Olive Din	69	student
179	s179	Din Hang	22	farmer
211	s211	Preben Oneda	80	student
6	s6	Norri Grass	43	farmer
102	s102	Peter East	42	farmer
288	s288	Tirill Winter	5	pupil
234	s234	Fermina Mouse	13	student
237	s237	Dekk Wild	77	fisher
334	s334	Jens Bass	57	pupil
129	s129	Pilka Baker	15	student
293	s293	Preben Fish	87	fisher
268	s268	Undala Bass	17	fisher
202	s202	Derek Bear	6	fisher
97	s97	Brenda Kong	62	fisher
120	s120	Mundei Hassana	78	pupil
138	s138	Tirill Smith	76	pupil
318	s318	Derek East	19	pupil
309	s309	Yuel Wild	74	pupil
328	s328	Mary Winter	73	pupil
223	s223	Pilka Oneda	8	pupil
145	s145	Zenita Erl	52	fisher
226	s226	Prestani Potter	63	fisher
92	s92	Warren Oneda	67	student
305	s305	Yang Dun	61	\N
278	s278	Preben Olive	12	pupil
336	s336	Anne Summer	24	fisher
291	s291	Hannah Bakken	67	pupil
19	s19	Long Chang	65	fisher
144	s144	Mary King	5	pupil
304	s304	Dumbak Spring	76	fisher
174	s174	Preben Wand	80	fisher
127	s127	Brenda Oneda	43	farmer
203	s203	Polentaz Spring	83	pupil
219	s219	Hux Din	36	fisher
345	s345	Olive Bird	90	pupil
112	s112	Jan Huldra	87	fisher
321	s321	Jens Stone	11	farmer
316	s316	Dong Wand	2	farmer
190	s190	Morta Smith	58	pupil
88	s88	Collie Chang	61	pupil
110	s110	Carl Bink	70	fisher
324	s324	Tirill Dun	4	pupil
105	s105	Jens King	54	student
181	s181	Olelec Mouse	16	fisher
230	s230	Tarud Chang	64	pupil
116	s116	Norri Bear	50	pupil
213	s213	Mank Smith	45	pupil
35	s35	Kolena Wang	48	pupil
216	s216	Dekk Fish	41	fisher
227	s227	Humazana Stad	52	farmer
272	s272	Kari Huzza	36	student
253	s253	Prestani Kong	72	fisher
243	s243	Sung Grass	93	fisher
269	s269	Yufrey Hang	64	pupil
126	s126	Kari Nilsen	64	fisher
231	s231	Olelec Asim	27	farmer
143	s143	Tams Stone	9	pupil
58	s58	Jan Asim	34	farmer
128	s128	Tams Chang	6	pupil
182	s182	Polentaz West	62	pupil
82	s82	San Grass	32	fisher
117	s117	Brenda Huzza	83	fisher
85	s85	Yuel Fall	39	student
224	s224	Sulfre Chang	27	farmer
301	s301	Anne Fish	58	farmer
10	s10	Pinky Olsen	5	farmer
331	s331	Undala Hassana	60	student
246	s246	Gina Oneda	18	fisher
22	s22	Derek Bing	61	fisher
106	s106	Carl Nilsen	25	fisher
76	s76	Gina Hang	99	fisher
50	s50	Olelec Huzza	81	pupil
347	s347	Hannah Winter	3	pupil
281	s281	Ole Bear	34	pupil
200	s200	Phillip Erl	94	pupil
232	s232	Yuel Hassana	41	farmer
194	s194	Yun King	73	pupil
285	s285	Connie Asim	7	pupil
119	s119	Okke Spring	19	student
207	s207	Mary Erl	43	student
113	s113	Glonfrid Din	39	farmer
277	s277	Yufrey Bakken	30	pupil
100	s100	Glonfrid Nilsen	6	farmer
51	s51	Derek Grass	33	fisher
167	s167	Gran Seagull	56	pupil
284	s284	Nax Sky	1	farmer
180	s180	Mank Stone	44	farmer
12	s12	Chi Chang	70	pupil
114	s114	Gina East	29	farmer
228	s228	Yali Seagull	93	fisher
257	s257	Neri Chang	99	farmer
49	s49	Juni Chang	4	fisher
310	s310	Nax Asim	29	fisher
18	s18	Dekk Bink	59	farmer
196	s196	Gert Summer	16	farmer
31	s31	Prestani Wand	72	fisher
81	s81	Odd Wild	98	pupil
122	s122	Gert Winter	19	student
295	s295	Anne Pod	13	pupil
343	s343	Sung Winter	59	student
332	s332	Mary Green	28	farmer
221	s221	Prestani Grass	81	fisher
286	s286	San Olsen	93	farmer
118	s118	Fermina Huldra	8	student
55	s55	Yali Bakken	22	pupil
239	s239	Vali Summer	55	pupil
20	s20	Gert Nilsen	19	farmer
93	s93	Even Winter	33	farmer
21	s21	Yi Seagull	24	fisher
178	s178	Dekk Wang	99	student
325	s325	Preben Wild	51	fisher
341	s341	Neri Trazin	86	pupil
38	s38	Jazzar Winter	73	fisher
160	s160	Pilka Grass	36	pupil
339	s339	Connie Nilsen	45	fisher
311	s311	Derek Nilsen	8	farmer
25	s25	Yi Pod	14	pupil
8	s8	Gina Bakken	45	\N
59	s59	Odd Dun	38	fisher
164	s164	Larry Chang	79	student
141	s141	Dong Summer	42	pupil
5	s5	Zenita Bink	95	fisher
297	s297	Morta Spring	27	student
299	s299	Glonfrid Wang	97	pupil
337	s337	Connie Stad	32	farmer
171	s171	Snafrid Nilsen	27	pupil
95	s95	Snafrid Wang	82	fisher
176	s176	Glonfrid Gupta	51	pupil
91	s91	Morta Fish	5	pupil
319	s319	Glonfrid Huzza	22	student
191	s191	Olive Seagull	86	fisher
185	s185	Yang Bass	30	farmer
13	s13	Connie Potter	81	farmer
54	s54	Okke Wand	69	student
86	s86	Long Grass	8	fisher
64	s64	Dong Stad	82	farmer
258	s258	Mary Huzza	7	fisher
263	s263	Fermina Bass	19	pupil
306	s306	Haleni Green	29	pupil
162	s162	Yi Trazin	15	student
266	s266	Mundei Pod	49	fisher
209	s209	Juni King	84	fisher
147	s147	Sung Bird	98	fisher
323	s323	Gran Bink	53	farmer
42	s42	Ole East	55	farmer
276	s276	Jing Summer	74	student
62	s62	Hasselina Wang	99	pupil
177	s177	Pirilill Bear	38	farmer
235	s235	Dong Wang	81	pupil
29	s29	Yi Summer	100	farmer
104	s104	Yulie Quix	36	student
130	s130	Chi Erdu	73	fisher
66	s66	Even Green	7	fisher
109	s109	Preben Din	5	student
84	s84	Merv Fall	68	fisher
287	s287	Carl Chang	14	pupil
53	s53	Yulie Winter	8	student
90	s90	Yufrey Oneda	97	fisher
254	s254	Even Hang	8	fisher
96	s96	Fermina Quix	7	farmer
99	s99	Din Chang	64	pupil
17	s17	Che King	72	pupil
45	s45	Prestani Asim	61	pupil
4	s4	Peter Nilsen	44	fisher
36	s36	Fermina Baker	47	farmer
150	s150	Jazzar West	93	farmer
1	s1	Yulie Smith	11	pupil
247	s247	Olelec Olive	44	farmer
69	s69	Gina Potter	17	student
134	s134	Ida Yun	68	student
236	s236	Fermina West	85	student
183	s183	Esmeralda Yun	34	pupil
149	s149	Tirill Potter	11	pupil
172	s172	Hannah Bear	17	farmer
340	s340	Yali Din	100	fisher
98	s98	Lomer East	53	farmer
65	s65	Chi Olsen	34	pupil
107	s107	Peter Fish	17	pupil
252	s252	Larry Potter	92	student
121	s121	Muhammad Erl	10	student
30	s30	Olelec Seagull	43	pupil
320	s320	Snafrid Huzza	68	student
155	s155	Odd Stone	43	farmer
56	s56	Brenda Olive	88	student
348	s348	San Bird	29	student
335	s335	Humazana Pod	44	pupil
188	s188	Olive Bink	39	pupil
37	s37	Dumbak Summer	26	pupil
47	s47	Warren Potter	7	fisher
225	s225	Nils Hassana	84	fisher
184	s184	Din Potter	32	fisher
44	s44	Jing Erdu	10	farmer
270	s270	Juni Green	46	student
125	s125	Sulfre Bird	1	\N
201	s201	Olive Wand	22	fisher
249	s249	Yufrey Hassana	72	fisher
9	s9	Pinky Quix	67	\N
16	s16	Jing Stone	51	\N
314	s314	Glari Baker	75	pupil
282	s282	Long Kong	68	fisher
7	s7	Derek Dun	42	student
77	s77	Yi Din	95	farmer
233	s233	Undala Bink	59	farmer
123	s123	Nils Smith	71	student
115	s115	Uri Bass	79	fisher
307	s307	Gran Smith	58	farmer
170	s170	Kolena Spring	66	fisher
222	s222	Merv Olsen	79	pupil
70	s70	Kristian Mouse	42	fisher
271	s271	Kristian Erl	51	fisher
83	s83	Preben Sky	80	pupil
195	s195	Nils Stad	80	student
205	s205	Nils King	64	fisher
238	s238	Pirilill Erdu	84	pupil
218	s218	Gina Wand	45	farmer
67	s67	Merv Chang	28	student
317	s317	Tirill West	8	pupil
154	s154	Prestani Oneda	69	farmer
289	s289	Yufrey Fish	89	pupil
279	s279	Xani Grass	92	student
303	s303	Glonfrid Pod	10	farmer
208	s208	Che Wand	42	student
290	s290	Kristian East	65	pupil
43	s43	Lomer Huzza	72	pupil
312	s312	Nax Grass	48	pupil
103	s103	Yulie Hassana	20	fisher
73	s73	Mary Gupta	37	farmer
133	s133	Yi Potter	20	fisher
322	s322	Dekk Bakken	83	student
274	s274	Jens Stad	96	\N
275	s275	Connie Wild	7	farmer
157	s157	Pilka Smith	83	pupil
74	s74	Snafrid Din	1	fisher
349	s349	Yulie Erl	38	student
151	s151	Derek Bink	88	pupil
204	s204	Carl Spring	13	student
327	s327	Yulie Mouse	12	fisher
186	s186	Kari Potter	17	pupil
137	s137	Haleni Huldra	43	student
298	s298	Mary Pod	56	student
61	s61	Dekk Dun	62	farmer
212	s212	Yang Fall	79	farmer
159	s159	Tirill Hang	33	pupil
259	s259	Warren Bakken	60	farmer
262	s262	Yuel Asim	31	farmer
189	s189	Warren Yun	58	student
80	s80	Even East	49	farmer
294	s294	Jazzar Asim	86	student
78	s78	Muhammad Dun	65	farmer
34	s34	Mank Fish	1	student
245	s245	Mank Fall	33	student
148	s148	Dumbak Smith	58	farmer
27	s27	Humazana Bear	38	farmer
296	s296	Neri Erl	23	pupil
79	s79	Hasselina Potter	17	farmer
300	s300	Lomer Asim	84	farmer
250	s250	Polentaz King	30	farmer
206	s206	Preben Summer	97	pupil
111	s111	Undala Stad	80	farmer
350	s350	Peter Smith	21	student
308	s308	Prestani Mouse	2	farmer
11	s11	Peter Hassana	73	farmer
3	s3	Jens Fall	44	farmer
87	s87	Juni Hassana	61	farmer
283	s283	Jan Winter	68	farmer
124	s124	Zenita Erdu	62	fisher
\.


--
-- Data for Name: home; Type: TABLE DATA; Schema: suburbia; Owner: -
--

COPY suburbia.home (hid, home_address, zip_code) FROM stdin;
1	Blossom street 6	1002
2	Blossom street 7	1002
3	Flower alley 9	1004
4	Flower alley 2	1004
5	Flower alley 14	1004
6	Cow street 11	1003
7	Harbour road 4	1005
8	Walnut road 14	1001
9	Flower alley 1	1004
10	Blossom street 9	1002
11	Grass road 6	1005
12	Harbour road 15	1005
13	Cow street 8	1003
14	Bird alley 3	1002
15	Grass road 15	1005
16	Bird alley 5	1002
17	Grass road 9	1005
18	Harbour road 1	1005
19	Blossom street 11	1002
20	Grass road 10	1005
21	Grass road 11	1005
22	Bird alley 9	1002
23	Grass road 2	1005
24	Bird alley 4	1002
25	Walnut road 4	1001
26	Walnut road 8	1001
27	Cow street 12	1003
28	Cow street 2	1003
29	Walnut road 9	1001
30	Blossom street 10	1002
31	Bird alley 15	1002
32	Grass road 3	1005
33	Bird alley 12	1002
34	Harbour road 6	1005
35	Cow street 5	1003
36	Bird alley 13	1002
37	Blossom street 12	1002
38	Walnut road 3	1001
39	Grass road 14	1005
40	Walnut road 15	1001
41	Harbour road 11	1005
42	Grass road 7	1005
43	Cow street 13	1003
44	Blossom street 14	1002
45	Harbour road 10	1005
46	Blossom street 3	1002
47	Grass road 12	1005
48	Flower alley 10	1004
49	Flower alley 7	1004
50	Harbour road 8	1005
51	Flower alley 8	1004
52	Cow street 4	1003
53	Flower alley 11	1004
54	Walnut road 12	1001
55	Flower alley 6	1004
56	Walnut road 6	1001
57	Bird alley 2	1002
58	Grass road 4	1005
59	Cow street 6	1003
60	Grass road 13	1005
61	Harbour road 13	1005
62	Bird alley 11	1002
63	Blossom street 1	1002
64	Harbour road 5	1005
65	Walnut road 7	1001
66	Walnut road 5	1001
67	Cow street 9	1003
68	Bird alley 7	1002
69	Flower alley 13	1004
70	Harbour road 3	1005
71	Bird alley 6	1002
72	Bird alley 1	1002
73	Cow street 1	1003
74	Cow street 14	1003
75	Flower alley 3	1004
76	Harbour road 12	1005
77	Bird alley 8	1002
78	Grass road 5	1005
79	Cow street 3	1003
80	Flower alley 15	1004
81	Walnut road 11	1001
82	Harbour road 7	1005
83	Blossom street 8	1002
84	Blossom street 4	1002
85	Harbour road 2	1005
86	Bird alley 14	1002
87	Bird alley 10	1002
88	Flower alley 5	1004
89	Blossom street 13	1002
90	Blossom street 5	1002
91	Grass road 1	1005
92	Walnut road 1	1001
93	Flower alley 12	1004
94	Walnut road 13	1001
95	Blossom street 2	1002
96	Cow street 7	1003
97	Harbour road 14	1005
98	Walnut road 10	1001
99	Walnut road 2	1001
100	Cow street 15	1003
\.


--
-- Data for Name: building; Type: TABLE DATA; Schema: urbania; Owner: -
--

COPY urbania.building (bid, address, zipcode) FROM stdin;
38	Yellow street 1	0101
13	Purple street 3	0103
18	Busy road 6	0106
40	Market alley 8	0105
35	West street 10	0107
29	Blue road 8	0101
1	West street 7	0107
34	Economy road 4	0104
12	West street 5	0107
33	Yellow street 6	0101
5	Purple street 10	0103
32	Green alley 5	0102
8	Market street 4	0104
9	Red road 8	0103
11	Market alley 2	0105
36	Busy road 7	0106
21	West street 4	0107
30	Dove corner 3	0105
31	Blue road 3	0101
15	Economy road 5	0104
28	Dove corner 10	0105
39	Green alley 1	0102
27	West street 1	0107
22	Busy road 1	0106
26	Red road 3	0103
3	West street 8	0107
6	Purple street 4	0103
14	Blue road 6	0101
2	West street 3	0107
24	West street 9	0107
20	Green alley 7	0102
37	East road 2	0106
19	Market street 6	0104
17	East road 7	0106
4	Economy road 7	0104
25	Economy road 2	0104
23	Yellow street 7	0101
7	Economy road 10	0104
10	Red road 6	0103
16	Yellow street 2	0101
\.


--
-- Data for Name: citizen; Type: TABLE DATA; Schema: urbania; Owner: -
--

COPY urbania.citizen (cid, urb_id, name, apartment_number, apartment_building, works_at) FROM stdin;
106	u106	Dong West	8	15	5
332	u332	Even Wild	1	2	2
374	u374	Pirilill Spring	8	38	13
636	u636	Larry Gupta	1	6	10
559	u559	Warren East	1	2	5
443	u443	Pirilill Grass	7	9	3
586	u586	Peter Gupta	8	1	1
530	u530	Unni Winter	8	13	7
634	u634	Polentaz Summer	4	34	7
254	u254	Kolena Potter	3	18	\N
562	u562	Yi Stone	6	2	2
649	u649	Phillip Quix	2	16	13
10	u10	Glonfrid Grass	6	25	13
384	u384	Carl East	7	26	\N
45	u45	Tirill Bakken	6	20	10
227	u227	Undala Kong	6	20	13
544	u544	Yi Bink	2	17	12
158	u158	Morta Winter	2	28	13
459	u459	Olive Wang	9	24	6
463	u463	Hannah Sky	8	30	12
355	u355	Gran Seagull	8	26	8
274	u274	Unni Ona	8	26	6
193	u193	Kolena Erl	1	4	11
322	u322	Phillip Potter	6	30	5
41	u41	Zenita Seagull	10	30	2
153	u153	Tams Huldra	10	13	10
601	u601	Merv Fish	8	32	4
171	u171	Brenda Mouse	5	9	5
303	u303	Ole Wild	9	32	6
96	u96	Peter Bing	9	12	\N
205	u205	Long Pod	7	36	7
326	u326	Haleni East	4	3	4
198	u198	Olelec Summer	6	37	4
512	u512	Warren Olive	10	12	3
518	u518	Che Gupta	6	14	6
145	u145	Norri Potter	9	21	7
324	u324	Tams Winter	6	24	1
444	u444	Jing Stad	3	15	13
626	u626	Esmeralda King	8	18	7
246	u246	Jazzar Potter	3	38	9
248	u248	Dumbak Green	4	24	13
177	u177	Even Asim	10	31	2
312	u312	Odd Green	4	11	6
598	u598	Jens Smith	9	33	7
306	u306	Tarud Bink	10	27	6
131	u131	Pinky Bird	6	25	7
607	u607	Gran Asim	3	27	4
62	u62	Tarud Spring	4	14	7
215	u215	Odd Din	1	15	3
509	u509	Odd Erl	9	26	12
213	u213	Pirilill Fall	3	3	5
91	u91	Tirill King	3	34	12
373	u373	Glonfrid Smith	9	37	8
566	u566	Fermina Hang	3	38	8
14	u14	Yufrey Din	2	32	10
160	u160	Din Bass	7	9	1
340	u340	Vali Bear	2	7	8
441	u441	Uri Wang	10	22	3
65	u65	Jan Chang	6	11	7
525	u525	Sung Trazin	3	16	8
21	u21	Yufrey Asim	5	4	12
400	u400	Okke Bass	4	22	1
27	u27	Prestani Quix	6	39	7
1	u1	Chi Summer	4	37	6
545	u545	Brenda West	8	35	7
425	u425	Jan Bink	3	11	7
347	u347	Pirilill Yun	7	19	4
88	u88	Jazzar Oneda	1	10	9
24	u24	Uri Nilsen	8	13	9
18	u18	Odd Nilsen	1	11	5
99	u99	Dumbak Bakken	1	31	6
629	u629	Okke Wang	6	19	5
593	u593	Nax Trazin	2	22	12
471	u471	Snafrid Trazin	5	27	11
412	u412	Okke Potter	9	17	2
43	u43	Carl King	5	1	\N
346	u346	Sung Wild	7	15	13
377	u377	Haleni West	9	38	10
301	u301	Prestani Green	10	28	4
446	u446	Kolena Wand	6	13	10
499	u499	Larry Potter	7	9	12
26	u26	Glonfrid Yun	10	12	13
393	u393	Even Trazin	1	23	8
494	u494	Pilka Fall	2	29	2
302	u302	Dekk Fish	2	14	11
157	u157	Hux Bear	3	38	7
492	u492	Yang Huzza	4	18	7
319	u319	Long Ona	9	40	5
360	u360	Norri Kong	5	21	2
46	u46	Collie Trazin	8	31	\N
363	u363	Vali Hang	10	15	3
166	u166	Long Potter	10	38	12
642	u642	Yi Quix	8	20	9
94	u94	Long Huldra	3	38	6
343	u343	Xani East	5	14	4
505	u505	Terry Summer	1	14	9
225	u225	Prestani Potter	1	9	13
220	u220	Pirilill Seagull	1	27	7
484	u484	Gina Seagull	1	18	3
632	u632	San Bear	5	4	9
286	u286	Mank Erdu	2	6	\N
164	u164	Gert Winter	2	35	12
292	u292	Hannah Bing	9	1	10
497	u497	Olelec Chang	1	4	12
423	u423	San Wand	9	17	6
202	u202	Che Winter	7	33	6
437	u437	Prestani Grass	3	29	1
52	u52	Prestani Yun	9	9	\N
420	u420	Vali Asim	9	14	12
490	u490	Odd Chang	1	17	\N
398	u398	Esmeralda Potter	4	30	5
58	u58	Nax Baker	3	10	1
184	u184	Even Wang	8	25	7
578	u578	Larry Grass	8	4	\N
196	u196	Haleni Stone	8	36	2
78	u78	Prestani Bakken	6	17	5
282	u282	Mundei Wild	8	12	6
47	u47	Ida Erl	4	28	6
482	u482	Yi Potter	1	14	10
469	u469	Esmeralda Ona	5	14	1
522	u522	Esmeralda Baker	10	24	3
64	u64	Hannah Trazin	7	21	\N
421	u421	Lomer Olive	9	26	12
76	u76	Ida Fall	3	30	10
109	u109	Olive Bing	2	17	13
258	u258	Xani West	3	2	13
276	u276	Sulfre Trazin	8	25	2
434	u434	Hasselina Huzza	7	3	\N
251	u251	Brenda Smith	4	16	1
238	u238	Olive Bakken	10	39	4
273	u273	Nils Grass	4	39	12
354	u354	Xani Potter	9	24	9
38	u38	Yun Bink	3	38	2
297	u297	Anne Asim	2	5	4
587	u587	Undala Potter	3	8	9
275	u275	Connie Fish	5	31	13
321	u321	Olelec Ona	3	6	9
643	u643	Jing Baker	10	36	2
53	u53	Zenita Wang	9	25	2
479	u479	Hannah Bear	2	5	4
17	u17	Tams Trazin	6	7	5
551	u551	Gran Stad	3	34	3
216	u216	Jazzar Stad	10	27	1
350	u350	Ida Quix	5	30	2
222	u222	Sulfre Olsen	10	7	6
85	u85	Brenda Bink	1	35	5
406	u406	Kari Summer	10	9	13
279	u279	Kolena Winter	6	3	2
624	u624	Dong Summer	6	14	10
114	u114	Uri Olive	2	22	1
357	u357	Tams Bass	10	27	12
536	u536	Sulfre West	3	32	11
353	u353	Yulie Kong	2	14	12
197	u197	Zenita Huzza	6	23	3
60	u60	Derek King	3	24	4
396	u396	Chi Chang	10	23	2
341	u341	Hux Oneda	8	5	10
496	u496	Haleni Bakken	4	24	3
452	u452	Juni Din	5	7	9
426	u426	Hux Kong	10	12	9
61	u61	Collie Baker	1	21	5
488	u488	Okke Trazin	8	39	\N
269	u269	Gran Summer	4	20	9
641	u641	Hasselina Olive	6	34	9
451	u451	Haleni Bird	1	17	1
136	u136	Juni Bakken	5	17	3
260	u260	Snafrid Spring	5	29	11
501	u501	Jens Bing	8	37	5
20	u20	Nax Huzza	4	1	4
534	u534	Kristian Spring	8	35	10
519	u519	Dekk Kong	5	22	2
117	u117	Long Mouse	1	29	\N
9	u9	Dumbak Stone	6	35	2
172	u172	Phillip Hang	5	16	12
623	u623	Yi Smith	8	16	11
502	u502	Dumbak Nilsen	3	35	13
69	u69	Din Summer	3	2	2
648	u648	Din Bear	2	2	12
565	u565	Connie Ona	10	37	4
25	u25	Kari Dun	4	24	8
154	u154	Connie Wild	5	19	12
486	u486	Yun Seagull	6	11	8
234	u234	Esmeralda Bass	4	31	11
584	u584	Tirill Baker	1	21	11
176	u176	Haleni Hang	6	12	10
3	u3	Derek Bink	4	29	2
210	u210	Tarud Quix	5	10	9
265	u265	Jens Hang	8	10	13
418	u418	Jing Fish	9	24	5
211	u211	Gran Wang	9	28	5
239	u239	Hasselina Grass	9	12	6
556	u556	Merv Sky	6	16	4
336	u336	Brenda Hassana	4	35	1
498	u498	Phillip Oneda	1	15	1
563	u563	Sung Quix	4	7	3
348	u348	Muhammad Bear	7	14	11
267	u267	Yulie Bing	3	39	4
16	u16	Mary Dun	6	22	1
305	u305	Kristian Oneda	2	13	1
433	u433	Tirill Bird	2	8	\N
33	u33	Kristian Bear	5	19	9
83	u83	Glari Huldra	3	17	13
435	u435	Jan Winter	4	2	2
105	u105	Ida Bing	4	18	12
331	u331	Gert Hassana	1	3	5
231	u231	Even Kong	4	2	11
49	u49	Humazana Green	4	4	6
155	u155	Yi Olsen	7	33	8
532	u532	Dekk Bear	10	4	8
573	u573	Esmeralda Quix	4	32	11
592	u592	Gina Stone	5	31	9
81	u81	Jazzar Gupta	3	7	4
633	u633	Even Din	6	5	1
427	u427	Gran Hassana	2	33	2
165	u165	Ole Dun	9	6	10
404	u404	Sulfre Bass	6	16	2
135	u135	Connie Olive	1	31	13
138	u138	Connie Summer	6	10	4
208	u208	Jazzar Bird	5	12	8
561	u561	Warren Wand	5	30	3
528	u528	Esmeralda Gupta	1	36	11
365	u365	Peter Pod	3	19	2
464	u464	Olive Gupta	9	32	5
631	u631	Norri Bird	10	32	8
507	u507	Anne Potter	7	14	\N
462	u462	Uri King	8	12	4
457	u457	Tirill Winter	1	33	2
614	u614	Vali Dun	9	16	10
299	u299	Zenita Pod	7	12	6
552	u552	Haleni Asim	2	39	4
334	u334	Yun Sky	1	17	4
320	u320	Derek Hang	2	19	12
470	u470	Mank Dun	8	17	7
580	u580	Gran Bakken	3	8	3
364	u364	Tarud Nilsen	3	34	8
431	u431	Dong Asim	1	5	1
440	u440	Yulie King	4	28	2
170	u170	Glari Spring	7	15	8
511	u511	Yun Fall	4	19	1
129	u129	Nils Wand	5	19	4
361	u361	Derek Trazin	5	3	10
375	u375	Vali Kong	6	19	7
391	u391	Yulie Spring	10	7	4
262	u262	Din West	10	14	10
228	u228	Mank Bear	9	5	13
417	u417	Yulie Bird	6	17	5
504	u504	Hannah Huldra	2	26	7
466	u466	Jazzar Huzza	10	15	6
121	u121	Long Huzza	10	4	11
615	u615	Sulfre Asim	7	5	12
102	u102	Hux Hassana	2	37	6
151	u151	San Hassana	9	9	7
50	u50	Glonfrid Bear	9	21	9
280	u280	Jan Fall	9	1	1
618	u618	Yun Wild	8	22	10
161	u161	Derek Sky	3	8	13
192	u192	Mary Wang	4	36	6
103	u103	Mary Seagull	7	12	12
75	u75	Yulie Olive	7	18	8
554	u554	Che Wand	9	38	11
650	u650	Zenita Baker	9	34	7
13	u13	Chi Bear	5	4	3
169	u169	Olive East	5	23	11
143	u143	Derek Winter	4	24	6
316	u316	Dumbak Grass	9	7	3
115	u115	Phillip Stone	6	5	2
407	u407	Connie Bink	2	13	10
87	u87	Hasselina Mouse	7	21	5
640	u640	Jing Bass	3	30	8
455	u455	Yali Stad	4	24	5
609	u609	Prestani Smith	10	15	9
542	u542	Pilka Bear	9	19	1
337	u337	Olive Dun	3	3	8
189	u189	Tirill Dun	5	33	\N
313	u313	Peter Hassana	1	25	11
576	u576	Esmeralda Pod	5	18	6
585	u585	Connie Mouse	7	24	4
5	u5	Gert Gupta	7	20	12
577	u577	Carl Nilsen	10	12	11
240	u240	Neri Hang	6	26	8
613	u613	Neri East	6	20	8
439	u439	Yuel Grass	10	17	10
485	u485	Xani Nilsen	9	11	11
120	u120	Tirill Huldra	1	10	9
369	u369	Carl Seagull	9	17	13
456	u456	Peter Oneda	9	20	13
296	u296	Sung Din	8	12	5
510	u510	Kristian Smith	2	19	6
226	u226	Polentaz West	1	8	2
201	u201	Connie Huzza	4	29	2
82	u82	Din Erl	4	21	3
647	u647	Pilka Chang	8	27	9
134	u134	Che Smith	4	38	10
460	u460	Xani Huldra	2	30	13
415	u415	Odd Stad	1	30	3
395	u395	Jazzar Grass	4	25	5
405	u405	Carl Sky	8	30	5
408	u408	Gina Bakken	3	13	2
142	u142	Ida Huldra	9	15	5
23	u23	Larry Huldra	8	7	10
531	u531	Pinky Fish	5	18	2
39	u39	Polentaz Erdu	2	16	4
392	u392	Gert Spring	1	5	13
345	u345	Unni Sky	8	30	13
378	u378	Peter Sky	10	18	2
574	u574	Kolena Summer	3	29	1
430	u430	Fermina Spring	10	28	5
144	u144	Gina Huzza	6	39	13
557	u557	Terry Din	8	39	8
89	u89	Kari Olive	1	35	10
187	u187	San Hang	5	29	6
474	u474	Gran Huzza	8	21	5
445	u445	Dekk Trazin	9	12	5
229	u229	Neri Green	10	14	13
589	u589	Tirill Bink	6	26	5
645	u645	Muhammad Trazin	9	6	4
477	u477	Polentaz Oneda	5	32	7
610	u610	Ida Bear	3	1	3
327	u327	Dumbak Fall	4	36	5
207	u207	Derek Bakken	5	2	12
549	u549	Prestani Baker	8	31	7
241	u241	Lomer Ona	5	19	5
308	u308	Nils Wild	8	37	8
370	u370	Yufrey Stone	2	13	10
611	u611	Gina Din	5	11	12
191	u191	Olelec Hang	8	33	4
162	u162	Even Olive	3	30	7
323	u323	Prestani Spring	9	14	3
183	u183	Long Hassana	3	8	13
140	u140	Tarud Erl	1	37	5
271	u271	Derek Bird	1	2	9
358	u358	Xani Kong	8	28	11
429	u429	Humazana Bird	6	37	9
250	u250	Humazana Quix	9	4	1
300	u300	Juni Winter	5	28	3
217	u217	Tams Spring	6	29	5
245	u245	Glonfrid Wand	7	22	1
289	u289	Mundei King	5	24	7
141	u141	Fermina Huzza	5	27	8
523	u523	Larry Spring	9	16	2
295	u295	Tams Summer	5	11	12
403	u403	Yulie Quix	8	5	8
454	u454	Collie Dun	1	3	\N
206	u206	Jens Huldra	8	37	1
500	u500	Unni Stad	1	11	1
223	u223	Jazzar Baker	10	37	11
571	u571	Lomer Kong	8	14	4
86	u86	Yali Spring	4	1	2
620	u620	Olive Trazin	6	26	4
97	u97	Snafrid Winter	6	20	\N
376	u376	Pirilill Summer	2	28	6
212	u212	Yuel Pod	10	11	8
558	u558	Gina Asim	6	4	7
150	u150	Gina Huldra	6	8	5
382	u382	Yun Gupta	1	18	10
100	u100	Warren Ona	3	38	1
517	u517	Warren Bakken	7	31	4
428	u428	Che West	6	7	8
487	u487	Glonfrid Hang	9	19	1
483	u483	Dumbak Mouse	2	22	3
290	u290	Mary Summer	2	17	11
533	u533	Long West	4	16	\N
174	u174	Snafrid East	6	11	2
342	u342	Pirilill Din	10	27	9
540	u540	Olive Seagull	5	10	7
458	u458	Collie Bear	3	9	4
90	u90	Sulfre Huzza	7	4	6
424	u424	Polentaz East	2	17	3
604	u604	Gert Olive	4	2	8
244	u244	Gert Wild	2	34	4
294	u294	Mary Asim	6	3	3
553	u553	Yufrey Smith	1	36	8
113	u113	Carl Olive	9	20	4
40	u40	Esmeralda Mouse	3	23	5
411	u411	Nils Erl	5	34	1
272	u272	San Mouse	6	31	5
110	u110	Tirill East	6	22	10
209	u209	Uri Dun	8	27	11
182	u182	Yun Wand	3	25	11
44	u44	Pirilill Huzza	9	30	1
277	u277	Pilka Quix	2	1	13
73	u73	Juni Spring	7	13	11
167	u167	Juni Fish	1	37	2
402	u402	Juni Bird	10	20	4
583	u583	Preben Kong	10	30	7
325	u325	Xani Quix	4	10	7
256	u256	Odd Grass	8	32	11
107	u107	Jing King	3	19	7
521	u521	Yulie Summer	10	14	12
646	u646	Zenita Bass	10	39	13
263	u263	Unni Fall	9	18	1
432	u432	Humazana Stad	7	31	11
338	u338	Mary Huzza	9	27	13
188	u188	Preben Grass	10	5	13
259	u259	Pilka Wang	5	30	9
480	u480	Yun Oneda	6	10	5
628	u628	Pinky Quix	6	39	9
422	u422	Connie Sky	5	40	6
185	u185	Yun Bird	7	10	5
133	u133	Hannah Potter	4	35	6
242	u242	Kristian Din	7	11	10
608	u608	Larry Fall	8	32	3
409	u409	Glonfrid Hassana	9	17	9
639	u639	Yulie Yun	5	35	2
630	u630	Sulfre Wang	7	33	7
264	u264	Merv Baker	2	22	5
149	u149	Carl Bear	8	26	13
36	u36	Polentaz Hang	4	4	11
414	u414	Phillip Stad	10	14	\N
310	u310	Undala Hang	7	4	1
318	u318	Pinky Din	5	3	4
119	u119	Olelec Winter	5	15	9
603	u603	Lomer Din	6	40	13
104	u104	Hasselina King	4	1	5
146	u146	Warren Erdu	9	40	7
309	u309	Mundei Quix	10	20	3
526	u526	Kristian Gupta	1	37	5
595	u595	Ida Wand	7	22	9
359	u359	Haleni Gupta	2	24	2
605	u605	Jazzar Yun	10	19	12
152	u152	Muhammad Potter	4	20	\N
491	u491	Yi Olive	3	16	8
438	u438	Kari Wand	3	22	11
513	u513	Zenita West	6	33	10
287	u287	Yuel Fish	6	1	7
48	u48	Yuel Stone	6	36	5
54	u54	Derek Huldra	3	8	8
537	u537	Anne Dun	3	29	3
261	u261	Juni Wild	10	40	8
126	u126	Merv East	5	7	11
344	u344	Collie Smith	9	36	12
351	u351	Gran Nilsen	4	5	11
367	u367	Tams Dun	8	2	11
168	u168	Chi Oneda	2	26	2
564	u564	Tirill Wand	1	27	13
235	u235	Merv Kong	10	3	5
527	u527	Ida Nilsen	5	31	6
372	u372	Dumbak Erl	1	29	1
304	u304	Yufrey Bass	3	6	9
95	u95	Long Smith	2	20	12
335	u335	Din Bing	5	33	5
28	u28	Mundei Huzza	3	11	5
622	u622	Pirilill Quix	3	21	4
644	u644	Kari Fall	9	14	7
635	u635	Dong Wild	3	40	6
288	u288	Derek Dun	4	1	2
602	u602	Yang Potter	9	31	13
381	u381	Connie Bass	8	28	3
219	u219	Morta Dun	10	16	12
130	u130	Dong Erdu	10	39	6
476	u476	Olelec Seagull	7	25	7
506	u506	Ole Huldra	8	3	6
108	u108	Jens Huzza	7	26	13
255	u255	Chi Olsen	2	1	6
524	u524	Uri Summer	1	14	6
599	u599	Yuel Yun	8	34	3
22	u22	Dumbak Huldra	3	32	13
278	u278	Long Trazin	6	38	13
600	u600	Hannah Green	3	35	1
84	u84	Din Bink	5	20	13
204	u204	Gert Summer	1	14	4
453	u453	Gert Huzza	9	7	7
311	u311	Dong Kong	9	13	4
616	u616	Tirill Sky	8	6	13
92	u92	Unni Quix	4	11	13
588	u588	Hux Grass	6	7	12
591	u591	Haleni Nilsen	3	23	8
122	u122	Hasselina Wild	8	38	2
71	u71	Undala Summer	5	31	10
253	u253	Yali Erdu	2	26	13
37	u37	Warren Erl	9	28	5
386	u386	Yulie Hang	8	18	10
252	u252	Tarud Bird	5	20	8
590	u590	Haleni Olive	5	18	10
594	u594	Xani Fish	4	24	4
181	u181	Hannah Olive	4	32	8
175	u175	Nils East	4	40	2
270	u270	Jan Trazin	8	4	3
4	u4	Peter Mouse	8	21	1
596	u596	Vali Summer	6	19	\N
349	u349	Jing East	5	10	5
535	u535	Jing Bird	1	19	3
42	u42	Mary Grass	5	33	7
199	u199	Mary Olive	8	11	13
35	u35	Din Trazin	9	20	1
449	u449	Ole Baker	5	16	\N
394	u394	Long Nilsen	1	23	6
638	u638	Juni Gupta	9	40	3
230	u230	Pilka Summer	4	7	5
79	u79	Vali Gupta	7	36	7
51	u51	Pirilill Chang	6	11	1
368	u368	Hannah West	2	7	5
137	u137	Yi Wild	8	12	12
281	u281	Yun Huldra	3	32	5
159	u159	Sung King	1	2	4
612	u612	Uri Din	4	3	3
617	u617	Gran Quix	2	3	4
419	u419	Sulfre Huldra	2	5	13
529	u529	Yali Trazin	8	32	4
127	u127	Zenita Potter	3	2	10
597	u597	Pinky Sky	2	27	4
247	u247	Fermina Fish	1	22	5
328	u328	Olelec Spring	2	20	7
178	u178	Hux Huldra	6	15	9
473	u473	Carl Summer	9	6	13
29	u29	Lomer Gupta	9	21	8
186	u186	Nax Ona	10	22	11
399	u399	Anne Oneda	2	6	3
625	u625	Vali Seagull	2	14	3
339	u339	Lomer East	4	7	1
388	u388	Yang Oneda	7	34	11
125	u125	Sulfre Yun	10	4	9
221	u221	Yi East	2	10	11
8	u8	Phillip Bing	4	6	3
416	u416	Ole Stad	8	1	2
7	u7	Jing Winter	4	5	12
461	u461	Humazana Olsen	2	38	8
366	u366	Merv Din	10	13	10
413	u413	Norri Dun	1	4	9
401	u401	Prestani Wand	1	23	2
93	u93	Phillip Asim	5	4	6
11	u11	Tirill Fish	4	9	\N
293	u293	Muhammad Quix	8	36	3
317	u317	Chi West	7	4	8
6	u6	Preben Erl	2	34	5
298	u298	Pinky Bear	6	18	8
237	u237	Polentaz Bing	2	4	12
560	u560	Dumbak Erdu	8	5	9
516	u516	Larry Bass	10	39	1
472	u472	Odd Olsen	7	37	9
70	u70	Norri Olsen	2	16	1
224	u224	San Nilsen	10	1	8
383	u383	Hux Bass	3	10	11
465	u465	Yali Hang	3	33	6
356	u356	Yuel Potter	7	10	10
67	u67	Hux Ona	2	13	3
582	u582	Derek Wild	5	4	12
481	u481	Collie Winter	4	30	8
520	u520	Uri Fall	3	29	10
330	u330	Nils Gupta	9	23	11
371	u371	Muhammad Green	2	20	1
55	u55	Jan Summer	8	20	7
387	u387	Yang Stone	8	4	12
379	u379	Xani Bass	7	7	5
2	u2	Olive Summer	10	18	11
380	u380	Polentaz Stad	4	1	12
218	u218	Yulie West	5	31	10
19	u19	Larry Seagull	7	3	4
139	u139	Olelec Green	1	40	9
447	u447	Even Stad	1	29	7
579	u579	Phillip Nilsen	6	21	2
508	u508	Morta Pod	2	6	2
329	u329	Snafrid Bass	2	12	13
257	u257	Unni Nilsen	3	28	7
489	u489	Yang Smith	9	40	3
627	u627	Brenda Pod	5	30	9
173	u173	Olive Nilsen	7	32	10
32	u32	Che Baker	5	34	1
291	u291	Chi Dun	5	16	9
621	u621	San Fish	3	25	6
31	u31	Dong Ona	9	7	11
555	u555	Tams Olive	6	12	2
111	u111	Juni Green	9	24	13
538	u538	Olelec Sky	4	7	11
467	u467	Norri Hang	4	32	\N
101	u101	Dekk Pod	6	13	3
163	u163	Chi Seagull	4	12	\N
116	u116	Derek Bass	5	14	1
147	u147	San Yun	5	14	13
214	u214	Glonfrid Stad	6	3	12
30	u30	Mank Wand	5	4	11
390	u390	Yali Bakken	9	34	\N
15	u15	Haleni Winter	8	38	\N
493	u493	Olive Hassana	8	7	3
307	u307	Terry Yun	1	31	10
515	u515	Phillip Fish	5	34	4
194	u194	Larry Smith	4	34	8
442	u442	Brenda Bing	2	37	13
268	u268	Nax Bird	1	33	\N
503	u503	Tarud Olive	8	22	3
195	u195	Yali Gupta	6	10	6
570	u570	Xani Summer	10	30	10
314	u314	Nax Wand	1	40	4
266	u266	Derek Bear	4	23	13
397	u397	Che Chang	1	33	\N
98	u98	Polentaz Fish	4	19	6
233	u233	Chi Pod	7	14	12
283	u283	Collie Fall	5	17	6
547	u547	Tarud Mouse	3	38	1
285	u285	Sulfre Bakken	1	30	1
72	u72	Morta Ona	4	25	1
475	u475	Morta Oneda	3	21	6
56	u56	Xani Spring	4	26	\N
249	u249	Che Green	5	24	12
123	u123	Jens Chang	5	38	1
567	u567	Glari King	6	20	7
581	u581	Anne Sky	10	20	2
548	u548	Carl Bing	10	9	11
200	u200	Yulie Din	1	9	13
132	u132	Yun Potter	10	36	7
190	u190	Okke Summer	8	38	7
546	u546	Sulfre Gupta	4	18	1
450	u450	Odd King	8	1	6
572	u572	Sung Hang	8	3	6
543	u543	Din Ona	10	6	9
232	u232	Pirilill King	3	7	9
619	u619	Jing Chang	6	31	1
57	u57	Gina Gupta	5	14	6
148	u148	Long King	7	21	11
74	u74	Dekk Baker	3	12	6
448	u448	Anne Winter	6	9	9
128	u128	Glonfrid Kong	9	40	7
63	u63	Dumbak Olive	7	3	9
495	u495	Ida Erdu	8	18	6
180	u180	Ida Trazin	7	28	10
112	u112	Okke Erdu	7	27	7
575	u575	Glari Bird	8	26	7
179	u179	Olive Chang	9	14	7
236	u236	Mank Huldra	4	13	3
124	u124	Collie Stone	6	15	9
410	u410	Unni East	4	12	13
468	u468	Yulie Fall	2	4	1
541	u541	Mundei Erl	1	5	9
385	u385	Kolena Oneda	9	22	5
66	u66	Ida Smith	3	13	7
59	u59	Sung Seagull	8	29	9
550	u550	Preben Bear	4	5	4
352	u352	Yi Spring	2	15	8
203	u203	Vali Bakken	7	13	12
539	u539	Preben Hassana	6	10	12
568	u568	Pilka Asim	8	39	4
315	u315	Yuel Bing	3	14	13
436	u436	Lomer Wand	10	16	6
118	u118	Vali Trazin	7	11	2
478	u478	Esmeralda Sky	10	12	8
569	u569	Uri Huldra	1	31	6
77	u77	Dumbak Asim	6	3	10
284	u284	Sulfre Winter	8	11	7
68	u68	Zenita Mouse	1	37	13
12	u12	Mundei Wang	10	19	12
362	u362	Collie Sky	6	34	2
243	u243	Odd Yun	1	16	9
606	u606	Gert Dun	4	27	6
156	u156	Norri Summer	8	4	11
333	u333	Olelec West	2	5	5
34	u34	Xani Baker	2	33	7
80	u80	Tams Huzza	1	29	2
637	u637	Okke Grass	9	4	8
389	u389	Din Mouse	3	39	2
514	u514	Terry Fall	8	3	6
\.


--
-- Data for Name: organization; Type: TABLE DATA; Schema: urbania; Owner: -
--

COPY urbania.organization (oid, name, offices_in) FROM stdin;
4	Gregor Inc.	15
12	Library	31
3	Hospital	26
11	Theater	33
8	Curly burly	14
13	School	\N
5	Products and wares	7
6	Nelson Corporation	4
9	Brad Analytics	28
10	University	39
2	Food market	19
1	Traders	27
7	Nikea	14
\.


--
-- Name: home_hid_seq; Type: SEQUENCE SET; Schema: suburbia; Owner: -
--

SELECT pg_catalog.setval('suburbia.home_hid_seq', 100, true);


--
-- Name: citizen citizen_pkey; Type: CONSTRAINT; Schema: suburbia; Owner: -
--

ALTER TABLE ONLY suburbia.citizen
    ADD CONSTRAINT citizen_pkey PRIMARY KEY (cid);


--
-- Name: citizen citizen_urb_id_key; Type: CONSTRAINT; Schema: suburbia; Owner: -
--

ALTER TABLE ONLY suburbia.citizen
    ADD CONSTRAINT citizen_urb_id_key UNIQUE (urb_id);


--
-- Name: home home_pkey; Type: CONSTRAINT; Schema: suburbia; Owner: -
--

ALTER TABLE ONLY suburbia.home
    ADD CONSTRAINT home_pkey PRIMARY KEY (hid);


--
-- Name: building building_pkey; Type: CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.building
    ADD CONSTRAINT building_pkey PRIMARY KEY (bid);


--
-- Name: citizen citizen_pkey; Type: CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.citizen
    ADD CONSTRAINT citizen_pkey PRIMARY KEY (cid);


--
-- Name: citizen citizen_urb_id_key; Type: CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.citizen
    ADD CONSTRAINT citizen_urb_id_key UNIQUE (urb_id);


--
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (oid);


--
-- Name: citizen citizen_home_fkey; Type: FK CONSTRAINT; Schema: suburbia; Owner: -
--

ALTER TABLE ONLY suburbia.citizen
    ADD CONSTRAINT citizen_home_fkey FOREIGN KEY (home) REFERENCES suburbia.home(hid);


--
-- Name: citizen citizen_apartment_building_fkey; Type: FK CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.citizen
    ADD CONSTRAINT citizen_apartment_building_fkey FOREIGN KEY (apartment_building) REFERENCES urbania.building(bid);


--
-- Name: citizen citizen_works_at_fkey; Type: FK CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.citizen
    ADD CONSTRAINT citizen_works_at_fkey FOREIGN KEY (works_at) REFERENCES urbania.organization(oid);


--
-- Name: organization organization_offices_in_fkey; Type: FK CONSTRAINT; Schema: urbania; Owner: -
--

ALTER TABLE ONLY urbania.organization
    ADD CONSTRAINT organization_offices_in_fkey FOREIGN KEY (offices_in) REFERENCES urbania.building(bid);


--
-- PostgreSQL database dump complete
--

