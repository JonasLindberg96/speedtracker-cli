import argparse
import datetime
import speedtest
import time

now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

class SpeedObj():
	def __init__(self):
		self.performance_down = []
		self.performance_up = []
		self.timemark = []

	def update(self, results_dict):
		self.performance_down.append(results_dict["download"])
		self.performance_up.append(results_dict["upload"])
		self.timemark.append(datetime.datetime.now)

	def retrieve(self):
		return self.performance_down, self.performance_up, self.timemark


def perform_check():
	time = datetime.datetime.now()
	print("Performing network speedtest, time is: ")
	print (now.strftime("%H:%M:%S"))

	servers = []
	# If you want to test against a specific server
	# servers = [1234]

	threads = None
	# If you want to use a single threaded test
	# threads = 1

	s = speedtest.Speedtest(secure=True)
	s.get_servers(servers)
	s.get_best_server()
	s.download(threads=threads)
	s.upload(threads=threads)
	s.results.share()

	return s.results.dict()


def arg_parser():
	parser = argparse.ArgumentParser()

	parser.add_argument('--duration',
						default=1,
						help='The duration in hours in which the check should be carried out.',
						dest='duration',
						type=int)
	parser.add_argument('--interval',
						default=1,
						help='The interval in minutes in which check should be carried out.',
						dest='interval',
						type=int)
	return parser.parse_args()
	
def main():
	args = arg_parser()

	print(f"Check will be carried out for {args.duration}h in {args.interval} min intervals.")

	speed = SpeedObj()

	start_time = datetime.datetime.now()
	end_time = start_time + datetime.timedelta(hours=args.duration)

	while datetime.datetime.now() < end_time:
		result_dict = perform_check()
		speed.update(result_dict)
		time.sleep(args.interval * 60)

	down, up, _ = speed.retrieve()
	print("Download speeds:")
	print(down)
	print("Upload speeds:")
	print(up)

if __name__ == "__main__":

	# https://stackoverflow.com/questions/56326644/python-speedtest-facing-problems-with-certification-ssl-c1056
	main()