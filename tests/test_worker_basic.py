
import unittest
import codecs
import os

from workers.basic_worker import BasicUserParseWorker


class TestWorkerBasic(unittest.TestCase):

    def test_basic_worker_connection(self):
        """
        Purpose: Test regular running of worker
        Expectation: startup system, hit the reddit user and parse the data, fail to send to mothership (exception)

        :precondition: Mothership server not running
        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        # Can't connect to mother, so should raise ConnectionRefusedError, but should run everything else
        self.assertRaises(ConnectionRefusedError, worker.run)

    def test_worker_parsing(self):
        """
        Purpose: Test regular parsing mechanisms of worker
        Expectation: Load html file, send it to worker to parse, should return list of results

        :return:
        """
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        file_path = '%s/%s' % (os.path.dirname(os.path.realpath(__file__)), 'test_resources/sample_GET_response.html')

        with codecs.open(file_path, encoding='utf-8') as f:
            text = f.read()

        results, next_page = worker.parse_text(str(text).strip().replace('\r\n', ''))

        self.assertGreater(len(results), 0)     # Check that results are returned
        self.assertEqual(len(results[0]), 3)    # Check that results are in triplets (check formatting)

    def test_worker_add_links_max_limit(self):
        worker = None
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        worker.max_links = 0
        len_to_crawl_before = len(worker.to_crawl)
        worker.add_links("test.com")
        len_to_crawl_after = len(worker.to_crawl)

        self.assertEqual(len_to_crawl_after, len_to_crawl_before)

    # def test_worker_add_links_in_crawled(self):
        # worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")
        # worker.crawled = []

        # len_to_crawl_before = len(worker.to_crawl)
        # worker.add_links(["https://www.reddit.com/user/Chrikelnel"])
        # len_to_crawl_after = len(worker.to_crawl)

        # self.assertEqual(len_to_crawl_after, len_to_crawl_before)

    # def test_worker_link_delay(self):
    # 	"""
    # 	Purpose: Test to verify link delay does not change.
    # 	Expectation: Change the link delay but it should not change

    # 	:return:
    # 	"""
    # 	worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

    # 	self.assertEqual(worker.link_delay, 0.25)
    # 	worker.link_delay = 0.5
    # 	self.assertEqual(worker.link_delay, 0.5)

    def test_worker_adding_duplicate_links(self):
    	"""
    	Purpose: Test adding duplicate links to the to_crawl list. (Fixed version of above code provided by Caleb Shortt)
    	Expectation: Link is not added to to_crawl list and length of list remains the same. 

    	:return:
    	"""
    	worker = None
    	worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

    	len_before = len(worker.to_crawl)
    	self.assertEqual(len_before, 1)
    	worker.run()
    	worker.add_links("https://www.reddit.com/user/Chrikelnel")
    	self.assertEqual(len(worker.to_crawl), len_before)

    def test_worker_adding_new_links(self):
    	"""
    	Purpose: Test adding new links to the to_crawl list.
    	Expectations: New link is added to to_crawl list and length of list increases.

    	:return:
    	"""
    	worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

    	len_before = len(worker.to_crawl)
    	worker.add_links("https://www.reddit.com/user/Groggen2")
    	self.assertGreater(len(worker.to_crawl), len_before)





