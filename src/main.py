import argparse
import datetime
import speedtest

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))


def arg_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument('--duration',
						default=1,
						help='The duration in hours in which the check should be carried out.',
						dest='duration')
	parser.add_argument('--interval',
						default=1,
						help='The interval in minutes in which check should be carried out.',
						dest='interval')
	return parser.parse_args()
	
def main():
	args = arg_parser()

	print(f"Check will be carried out for {args.duration}h in {args.interval} min intervals.")

	servers = []
	# If you want to test against a specific server
	# servers = [1234]

	threads = None
	# If you want to use a single threaded test
	# threads = 1

	s = speedtest.Speedtest()
	s.get_servers(servers)
	s.get_best_server()
	s.download(threads=threads)
	s.upload(threads=threads)
	s.results.share()

	results_dict = s.results.dict()
	print(results_dict)


if __name__ == "__main__":
	main()