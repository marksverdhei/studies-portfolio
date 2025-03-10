# Info variables
db_name = in5800 #Set the name of your personal DB
db_user = test # Set your personal DB's username
db_password = test # Set your personal DB-user's password
db_host=localhost # Set to dbpg-ifi-kurs01 if on an IFI-machine

export PGPASSWORD = $(db_password)

# Program variables
java = java #                                                              Comment OUT this line if on an IFI-machine
#java = /usr/lib/jvm/java-11-openjdk-11.0.10.0.9-4.el8_3.x86_64/bin/java # Comment INN this line is on an IFI-machine

lutra = $(java) -jar programs/lutra.jar
toko = $(java) -jar programs/Toko.jar -d $(db_name) -U $(db_user) -P $(db_password) -h $(db_host) -v
psql = psql -d $(db_name) -U $(db_user) -h $(db_host) -W


# Setup

programs:
	mkdir -v programs

data:
	mkdir -v data

mappings:
	mkdir -v mappings

templates:
	mkdir -v templates

semantics:
	mkdir -v semantics

folders: programs data mappings templates semantics

programs/lutra.jar: programs
	wget -O programs/lutra.jar https://gitlab.com/ottr/lutra/lutra/-/jobs/artifacts/v0.6.10/raw/lutra.jar?job=release

programs/Toko.jar: programs
	wget -O programs/Toko.jar http://leifhka.org/in5800/Toko.jar

data/organizations.csv: data
	wget -O data/organizations.csv http://leifhka.org/in5800/oblig/organizations.csv

data/urb.sql: data
	wget -O data/urb.sql http://leifhka.org/in5800/oblig/urb.sql

semantics/kiwi-owl.skwrl: semantics
	wget -O semantics/kiwi-owl.skwrl http://leifhka.org/in5800/data/kiwi-owl.skwrl

setup: folders programs/lutra.jar programs/Toko.jar data/organizations.csv data/urb.sql semantics/kiwi-owl.skwrl

clean_setup:
	rm -vf data/organizations.csv
	rm -vf data/urb.sql
	rm -vf programs/Toko.jar
	rm -vf programs/lutra.jar
	rm -vf semtics/kiwi-owl.skwrl


# Data and mappings

kiwi:
	$(toko) -m init

relational_dbs:
	$(psql) -f data/urb.sql

direct_mappings: relational_dbs kiwi
	$(psql) -f mappings/direct_mappings.sql
	$(toko) -m applymappings

organizations: kiwi
	$(lutra) -m expand -I bottr -L stottr -l templates/organizations.stottr -f -O wottr -o data/organizations mappings/organizations-map.ttl
	$(toko) -m load -i data/organizations.ttl

all_data: direct_mappings organizations

# Semantics

urb_ontology: all_data
	$(toko) -m load -i semantics/urb_ontology.ttl
	$(toko) -m loadrules -i semantics/kiwi-owl.skwrl

urb_rules: urb_ontology
	$(toko) -m loadrules -i semantics/urb_rules.skwrl

triplestore: urb_rules

# Querying

query_people:
	$(toko) -m query -i "$$(cat queries/people.sparql)"

query_organizations:
	$(toko) -m query -i "$$(cat queries/organizations.sparql)"

# Clean databases

clean_dbs:
	$(toko) -m clean
	$(psql) -c "DROP SCHEMA IF EXISTS urbania CASCADE; DROP SCHEMA IF EXISTS suburbia CASCADE;"


clean_all: clean_setup clean_dbs

.PHONY: folders setup clean_setup clean_dbs kiwi relational_dbs direct_mappings organizations buildings all_data urb_ontology urb_rules triplestore clean_all
