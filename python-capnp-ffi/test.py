import unittest
import capnp_ffi
import os
import date_example
date_example = date_example.DateLibInterface()

class TestCapnp(unittest.TestCase):
	def setUp(self):
		pass
		
	def test_date_example(self):
		d = date_example.Date(year=2015, month=2, day=5)
		# call to rust function!
		result = date_example.change_date(d)
		self.assertEqual( 
			result.to_dict(), 
			date_example.Date(year=2016, month=2, day=1).to_dict()
		)
		
if __name__ == '__main__':
	unittest.main()
