#!/usr/bin/env python
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

"""Run BioSQL tests using SQLite"""
import os
from Bio import MissingExternalDependencyError
from BioSQL import BioSeqDatabase

from common_BioSQL import *

# Constants for the database driver
DBHOST = 'localhost'
DBUSER = 'root'
DBPASSWD = ''

DBDRIVER = 'sqlite3'
DBTYPE = 'sqlite'
TESTDB = os.path.join(os.getcwd(), "BioSQL", "temp_sqlite.db")
# In memory SQLite does not work with current test structure since the tests
# expect databases to be retained between individual tests.
#TESTDB = ':memory:'

#This will abort if driver not installed etc:
check_config(DBDRIVER, DBTYPE, DBHOST, DBUSER, DBPASSWD, TESTDB)

#Some of the unit tests don't create their own database,
#so just in case there is no database already:
create_database()

if False:
    #This is how I generated test file Tests/BioSQL/cor6_6.db
    #which is test cross-checked with the latest bindings to
    #catch any regressions in how we map GenBank entries to
    #the database.
    assert not os.path.isfile("BioSQL/cor6_6.db")
    server = BioSeqDatabase.open_database(driver=DBDRIVER, db="BioSQL/cor6_6.db")
    DBSCHEMA = "biosqldb-" + DBTYPE + ".sql"
    SQL_FILE = os.path.join(os.getcwd(), "BioSQL", DBSCHEMA)
    assert os.path.isfile(SQL_FILE), SQL_FILE
    server.load_database_sql(SQL_FILE)
    server.commit()
    db = server.new_database("OLD")
    count = db.load(SeqIO.parse("GenBank/cor6_6.gb", "gb"))
    assert count == 6
    server.commit()
    assert len(db) == 6
    server.close()

if __name__ == "__main__":
    #Run the test cases
    runner = unittest.TextTestRunner(verbosity = 2)
    unittest.main(testRunner=runner)
