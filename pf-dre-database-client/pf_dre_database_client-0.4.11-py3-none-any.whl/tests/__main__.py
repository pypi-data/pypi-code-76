# tests/runner.py
import unittest

# import your tests modules
import tests.test_devices as devices
import tests.test_configuration as config
import tests.ts_reads.test_data_reads as data_reads
import tests.ts_reads.json_reads as json_reads
import tests.ts_reads.narrow_reads as narrow_reads
import tests.ts_writes.json_writes as json_writes
import tests.ts_writes.narrow_writes as narrow_writes

# initialize the tests suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(devices))
suite.addTests(loader.loadTestsFromModule(config))

suite.addTests(loader.loadTestsFromModule(data_reads))
suite.addTests(loader.loadTestsFromModule(json_reads))
suite.addTests(loader.loadTestsFromModule(narrow_reads))

suite.addTests(loader.loadTestsFromModule(narrow_writes))
suite.addTests(loader.loadTestsFromModule(json_writes))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
